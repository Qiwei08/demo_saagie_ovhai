import argparse
import logging

import boto3
import datasets
import evaluate
import numpy as np
import pandas as pd
import torch
import transformers
from datasets import Dataset, load_dataset
from huggingface_hub import logging
from huggingface_hub import login
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
from transformers import DataCollatorWithPadding
from transformers import TrainingArguments, Trainer
import mlflow


def main():
    # Retrieving arguments
    parser = argparse.ArgumentParser(
        description='Fine-tune a pretrained Hugging Face model for sentiment classification.')
    parser.add_argument("--hf_model", type=str,
                        help="Hugging Face id of the pretrained model", required=True)
    # Using a dataset saved on hugging face
    parser.add_argument("--hf_ds", type=str,
                        help='Hugging Face dataset', required=False, default="")
    # Using a dataset saved on S3
    parser.add_argument("--train_ds", type=str,
                        help='training dataset', required=False, default="")
    parser.add_argument("--valid_ds", type=str,
                        help='validation dataset', required=False, default="")
    parser.add_argument("--url", type=str,
                        help='endpoint url of s3', required=False, default="")
    parser.add_argument("--keyid", type=str,
                        help='aws_access_key_id', required=False, default="")
    parser.add_argument("--secretkey", type=str,
                        help='aws_secret_access_key', required=False, default="")
    parser.add_argument("--region", type=str,
                        help='region name', required=False, default="")
    parser.add_argument("--bucket", type=str,
                        help='bucket', required=False, default="")
    # Training arguments
    parser.add_argument("--randomstate", type=int,
                        help='rng seed', required=False, default=42)
    parser.add_argument("--train_subset", type=int,
                        help='train_subset', required=False, default=3000)
    parser.add_argument("--eval_subset", type=int,
                        help='eval_subset', required=False, default=300)
    parser.add_argument("--epochs", type=int,
                        help='epochs number', required=False, default=4)
    parser.add_argument("--token", type=str,
                        help='huggingface token', required=True, default="")
    parser.add_argument("--repo_name", type=str,
                        help='huggingface repository name', required=True, default="")
    parser.add_argument("--device", help="Device where is computed Deep learning, 'cpu' or 'cuda'", default='cuda',
                        required=False)
    parser.add_argument("--tracking", type=str,
                        help='mlflow server url', required=True, default="")

    args = parser.parse_args()

    # Load datasets
    if args.hf_ds != "":
        dataset = load_dataset(args.hf_ds)
        train = dataset['train']
        valid = dataset['validation']
        dataset_name = args.hf_ds
    else:
        cl = boto3.client(endpoint_url=args.url,
                          aws_access_key_id=args.keyid,
                          aws_secret_access_key=args.secretkey,
                          service_name="s3", region_name=args.region)
        response = cl.get_object(Bucket=args.bucket, Key=args.train_ds)
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if status == 200:
            logging.info(
                f"Successful S3 get_object response. Status - {status}")
            train_ds = pd.read_csv(response.get("Body"))
        else:
            logging.info(
                f"Unsuccessful S3 get_object response. Status - {status}")
            exit()
        response = cl.get_object(Bucket=args.bucket, Key=args.valid_ds)
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if status == 200:
            logging.info(
                f"Successful S3 get_object response. Status - {status}")
            valid_ds = pd.read_csv(response.get("Body"))
        else:
            logging.info(
                f"Unsuccessful S3 get_object response. Status - {status}")
            exit()
        train = Dataset.from_pandas(train_ds)
        valid = Dataset.from_pandas(valid_ds)
        dataset_name = args.train_ds + ', ' + args.valid_ds

    # Dataset preparation
    tokenizer = AutoTokenizer.from_pretrained(args.hf_model)

    def tokenize_function(examples):
        return tokenizer(examples["sentence"], padding="max_length", truncation=True)

    tokenized_train = train.map(tokenize_function, batched=True)
    tokenized_valid = valid.map(tokenize_function, batched=True)
    small_train_dataset = tokenized_train.shuffle(
        seed=args.randomstate).select(range(args.train_subset))
    small_eval_dataset = tokenized_valid.shuffle(
        seed=args.randomstate).select(range(args.eval_subset))
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    # Pretrained model & trainer preparation
    ## Define the device to use by torch
    device = torch.device(args.device)
    model = AutoModelForSequenceClassification.from_pretrained(
        args.hf_model, num_labels=2).to(device)
    metric = evaluate.load("accuracy")

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        return metric.compute(predictions=predictions, references=labels)

    hf_token = args.token
    login(hf_token)

    repo_name = args.repo_name

    training_args = TrainingArguments(
        output_dir=repo_name,
        overwrite_output_dir=True,
        num_train_epochs=args.epochs,
        logging_strategy="epoch",
        evaluation_strategy="epoch",
        save_strategy="no",
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=small_train_dataset,
        eval_dataset=small_eval_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics
    )

    # Fine-tuning
    trainer.train()
    # Push the fine-tuned model to huggingface & log metrics to MLflow
    commit_url = trainer.push_to_hub()
    url_split = commit_url.split('/')
    metrics = trainer.evaluate()
    mlflow.end_run()  # To avoid conflict with Trainer class
    mlflow.set_tracking_uri(args.tracking)
    mlflow.set_registry_uri(args.tracking)
    mlflow.set_experiment('movie-sentiment-classification')
    with mlflow.start_run() as run:
        # Log parameters
        mlflow.log_param('train_subset_size', args.train_subset)
        mlflow.log_param('eval_subset_size', args.eval_subset)
        mlflow.log_param('rng_seed', args.randomstate)
        mlflow.set_tag('commit.id', url_split[-1])
        mlflow.set_tag('commit.url', commit_url)
        mlflow.set_tag(
            'model_dir', url_split[-4]+'/'+url_split[-3]+':'+url_split[-1])
        mlflow.set_tag('training.dataset', dataset_name)
        # Log metrics
        for metric in metrics:
            mlflow.log_metric(key=metric, value=metrics[metric])
        print(run.info)


if __name__ == "__main__":
    datasets.logging.set_verbosity(30)
    logging.set_verbosity_warning()
    main()

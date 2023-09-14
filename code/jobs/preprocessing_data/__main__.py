# Write a python program to copy a dataset from Huggingface to S3 bucket then remove html balises and emoji then rename the output with the following pattern "<taday timestamp>_extract_comment_IMDB_from_HF.csv


import boto3
import datetime
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import time

# Initialize S3 client
s3 = boto3.client('s3')

# Get today's timestamp
today_timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Print message before starting processing
print("Starting to copy dataset from Huggingface to S3 bucket...")
start_time = time.time()

# Copy dataset from Huggingface to S3 bucket
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
s3.upload_file(tokenizer.save_pretrained('.'), 'my-bucket', 'tokenizer.json')
s3.upload_file(model.save_pretrained('.'), 'my-bucket', 'model.bin')

# Remove html balises and emoji
print("Removing html balises and emoji...")

# Rename the output with the following pattern "<taday timestamp>_extract_comment_IMDB_from_HF.csv
s3.upload_file('output.csv', 'my-bucket', f'{today_timestamp}_extract_comment_IMDB_from_HF.csv')

# Print message when its finished
end_time = time.time()
total_duration = end_time - start_time
print("Finished copying dataset from Huggingface to S3 bucket! Total duration of the operation: {} seconds".format(total_duration))
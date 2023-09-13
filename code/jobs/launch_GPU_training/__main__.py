import logging
import os
import sys

from requests import ConnectionError as requestsConnectionError
from requests import HTTPError, RequestException, Timeout
from time import sleep
import requests
import argparse
import swiftclient
from swiftclient.exceptions import ClientException
from utils import ovh_token_data


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def upload_file_swift(url, token, file_path, bucket_name, name):
    """

    :param url: string, Swift bucket endpoint
    :param file_path: string, path of file to upload
    :param token: string, Openstack token, you can create when visit OVH
                            -> Users & Roles -> Choose an user -> Generate OpenStack token
    :param bucket_name: string, Bucket to upload to
    :param name: string, S3 object name
    :return:
    """
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
        swiftclient.client.put_object(url=url, token=token, container=bucket_name, name=name, contents=file_data)
    except ClientException as e:
        logging.error(e)
        raise
    return True


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
    parser.add_argument("--repo_name", type=str,
                        help='huggingface repository name', required=True, default="")
    parser.add_argument("--device", help="Device where is computed Deep learning, 'cpu' or 'cuda'", default='cuda',
                        required=False)
    parser.add_argument("--tracking", type=str,
                        help='mlflow server url', required=True, default="")

    args = parser.parse_args()

    # Configuration
    logging.info("Put code to OVH")
    s3_bucket_name = os.environ["TRAINING_BUCKET_NAME"]
    bucket_endpoint = os.environ["BUCKET_ENDPOINT_URL"]
    res_get_token = requests.post(url = "https://auth.cloud.ovh.net/v3/auth/tokens",
                                  json = ovh_token_data,
                                  headers={"Content-Type": "application/json"}
                                  )
    openstack_token = res_get_token.headers["x-subject-token"]
    upload_file_swift(bucket_endpoint, openstack_token, "./ressources/__main__.py", s3_bucket_name, "__main__.py")
    upload_file_swift(bucket_endpoint, openstack_token, "./ressources/requirements.txt",
                      s3_bucket_name, "requirements.txt")

    logging.info("Code on OVH")

    ovh_token_gra = os.environ["OVH_TOKEN"]

    if args.hf_ds != "":
        command_line = f"""python ~/sample_project/__main__.py --hf_model {args.hf_model} --hf_ds {args.hf_ds}  --randomstate {args.randomstate} --train_subset {args.train_subset} --eval_subset {args.eval_subset} --epochs {args.epochs} --token $HUGGINGFACE_TOKEN --device {args.device} --repo_name {args.repo_name} --tracking {args.tracking}"""
    else:
        command_line = f"""python ~/sample_project/__main__.py --hf_model {args.hf_model}  --train_ds {args.train_ds} --valid_ds {args.valid_ds} --url {args.url} --keyid {args.keyid} --secretkey {args.secretkey} --region {args.region} --bucket {args.bucket} --randomstate {args.randomstate} --train_subset {args.train_subset} --eval_subset {args.eval_subset} --epochs {args.epochs} --token $HUGGINGFACE_TOKEN --device {args.device} --repo_name {args.repo_name} --tracking {args.tracking}"""

    ovh_new_job = {
        "image": "qiwei1000/ovh_test:1.4",
        "region": "GRA",
        "volumes": [
            {
                "dataStore": {
                    "alias": "GRA",
                    "container": s3_bucket_name,
                    "prefix": ""
                },
                "mountPath": "/workspace/sample_project",
                "permission": "RW",
                "cache": False
            }
        ],
        "name": "test-sample-project-movie-review",
        "unsecureHttp": False,
        "resources": {
            "gpu": 1,
            "flavor": "ai1-1-gpu"
        },
        "command": [
            "bash",
            "-c",
            command_line
        ],
        "envVars": [
            {
                "name": "HUGGINGFACE_TOKEN",
                "value": os.environ['HUGGINGFACE_TOKEN']
            },
            {
                "name": "REALM",
                "value": os.environ["SAAGIE_REALM"]
            },
            {
                "name": "SAAGIE_URL",
                "value": os.environ["SAAGIE_URL"]
            },
            {
                "name": "PLATFORM_ID",
                "value": os.environ["SAAGIE_PLATFORM_ID"]
            },
            {
                "name": "SAAGIE_LOGIN",
                "value": os.environ["SAAGIE_LOGIN"]
            },
            {
                "name": "SAAGIE_PASSWORD",
                "value": os.environ["SAAGIE_PASSWORD"]
            },

        ],
        "sshPublicKeys": []
    }

    # Create new AI training job
    try:
        response_create_job = requests.post("https://gra.training.ai.cloud.ovh.net/v1/job",
                                            auth=BearerAuth(ovh_token_gra),
                                            json=ovh_new_job)
        response_create_job.raise_for_status()
        logging.info("OVH training Job started")
    except (HTTPError, requestsConnectionError, Timeout, RequestException) as err:
        logging.error(err)
        raise

    # Get job status
    logging.info("Getting job status ...")
    try:
        response_job = requests.get(f"https://gra.training.ai.cloud.ovh.net/v1/job/{response_create_job.json()['id']}",
                                    auth=BearerAuth(ovh_token_gra))
        response_job.raise_for_status()
        logging.info("Get job status")
        id_job = response_create_job.json()['id']
    except (HTTPError, requestsConnectionError, Timeout, RequestException) as err:
        logging.error(err)
        raise

    finished = False
    last_status = ""
    while not finished:
        logging.info("Job not finished, wait 20 s ....")
        sleep(20)
        response_job = requests.get(f"https://gra.training.ai.cloud.ovh.net/v1/job/{id_job}",
                                    auth=BearerAuth(ovh_token_gra))
        logging.info("Get job status again")
        finished = response_job.json()["status"]["finalizedAt"] is not None
        last_status = response_job.json()["status"]["state"]

    # Get job log
    logging.info("Starting to get logs ... ")
    sleep(20)
    response_job_logs = requests.get(f"https://gra.training.ai.cloud.ovh.net/v1/job/{id_job}/log",
                                     auth=BearerAuth(ovh_token_gra)).text

    for line in response_job_logs.splitlines():
        print(line, flush=True)

    if last_status == "FAILED":
        logging.error("Job failed on OVH")
        exit(1)
    else:
        logging.info("Job finished on OVH")
        

    


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        datefmt="%d/%m/%Y %H:%M:%S")
    main()



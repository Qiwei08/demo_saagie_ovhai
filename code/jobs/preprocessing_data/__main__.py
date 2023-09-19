# Write a python program to copy a dataset for the tiny-bert model from Huggingface to S3 bucket,
# remove html balises and emoji 
# rename the output with the following pattern "<timestamp>_extract_comment_IMDB_from_HF.csv.
# Display a message  before starting processing and when it's finished plus the total duration of the operation


import boto3
import datetime
import pandas as pd
import re
import requests

def copy_dataset_to_s3():
    # Display a message before starting processing
    print("Copying dataset to S3 bucket...")

    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Download the dataset from Huggingface
    url = "https://path/to/dataset.csv"
    response = requests.get(url)
    dataset = response.text

    # Remove HTML tags using regular expressions
    dataset = re.sub("<.*?>", "", dataset)

    # Remove emojis using regular expressions
    dataset = re.sub("[^\u0000-\uFFFF]", "", dataset)

    # Save the processed dataset to a file
    output_filename = f"{timestamp}_extract_comment_IMDB_from_HF.csv"
    with open(output_filename, "w") as file:
        file.write(dataset)

    # Upload the file to S3 bucket
    s3 = boto3.client("s3")
    s3.upload_file(output_filename, "your-s3-bucket", output_filename)

    # Display a message when finished
    print("Dataset copied to S3 bucket successfully.")

if __name__ == "__main__":
    # Start measuring the time
    start_time = datetime.datetime.now()

    # Call the function to copy the dataset to S3 bucket
    copy_dataset_to_s3()

    # Calculate the total duration of the operation
    end_time = datetime.datetime.now()
    duration = end_time - start_time

    # Display the total duration
    print(f"Total duration: {duration}")

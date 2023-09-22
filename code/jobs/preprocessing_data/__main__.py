# Write a python program to copy a dataset for the tiny-bert model from Huggingface to S3 bucket,
# remove html balises and emoji 
# rename the output with the following pattern "<timestamp>_extract_comment_IMDB_from_HF.csv.
# Display a message  before starting processing and when it's finished plus the total duration of the operation



import boto3
import pandas as pd
from bs4 import BeautifulSoup
import re
import datetime
import time

def copy_dataset_to_s3():
    # Display message before starting processing
    print("//.")

    # Copy dataset from Huggingface to S3 bucket
    s3 = boto3.client('s3')
    s3.copy_object(
        Bucket='your-s3-bucket',
        CopySource='huggingface-dataset-path',
        Key='dataset.csv'
    )

    # Read dataset from S3 bucket
    df = pd.read_csv('s3://your-s3-bucket/dataset.csv')

    # Remove HTML tags and emojis from comments
    df['comment'] = df['comment'].apply(lambda x: BeautifulSoup(x, 'html.parser').get_text())
    df['comment'] = df['comment'].apply(lambda x: re.sub(r'[^\x00-\x7F]+', '', x))

    # Generate timestamp for renaming output file
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Rename output file with timestamp
    output_filename = f"{timestamp}_extract_comment_IMDB_from_HF.csv"
    df.to_csv(output_filename, index=False)

    # Display message after finishing processing
    print("Dataset copied and processed successfully!")

# Start timer
start_time = time.time()

# Call the function to copy dataset to S3 bucket and process it
copy_dataset_to_s3()

# Calculate total duration of operation
end_time = time.time()
duration = end_time - start_time

# Display total duration of operation
print(f"Total duration: {duration} seconds")

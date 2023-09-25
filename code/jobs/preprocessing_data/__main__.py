# Write a python program to copy a dataset for the tiny-bert model from Huggingface to S3 bucket,
# remove html balises and emoji 
# rename the output with the following pattern "<timestamp>_extract_comment_IMDB_from_HF.csv.
# Display a message  before starting processing and when it's finished plus the total duration of the operation


import boto3
import pandas as pd
from bs4 import BeautifulSoup
import re
import emoji
import datetime

def copy_dataset_to_s3():
    # Display message before starting processing
    print("Copying dataset to S3 bucket...")

    # Copy dataset from Huggingface to S3 bucket
    # Replace 'your_huggingface_dataset' with the actual dataset name
    s3 = boto3.client('s3')
    s3.copy_object(
        Bucket='your_s3_bucket',
        CopySource={
            'Bucket': 'huggingface_datasets',
            'Key': 'your_huggingface_dataset'
        },
        Key='your_output_path'
    )
    
    # Load the copied dataset into a DataFrame
    # Replace 'your_output_path' with the actual output path in your S3 bucket
    df = pd.read_csv('your_output_path')

    # Remove HTML tags using BeautifulSoup
    df['text'] = df['text'].apply(lambda x: BeautifulSoup(x, 'html.parser').get_text())

    # Remove emojis using regex
    df['text'] = df['text'].apply(lambda x: re.sub(emoji.get_emoji_regexp(), '', x))

    # Rename the output file with the specified pattern
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_filename = f"{timestamp}_extract_comment_IMDB_from_HF.csv"
    df.to_csv(output_filename, index=False)

    # Display message when finished processing
    print("Dataset processing finished.")
    print(f"Total duration: {datetime.datetime.now() - start_time}")

# Start time of the operation
start_time = datetime.datetime.now()

# Call the function to copy the dataset and perform the required operations
copy_dataset_to_s3()

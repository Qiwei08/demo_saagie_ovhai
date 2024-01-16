import pandas as pd
from datetime import datetime
import boto3
import re

def copy_dataset_to_s3():
    # Display message before starting processing
    print("Copying dataset to S3 bucket...")

    # Copy dataset for tiny-bert model from Huggingface to S3 bucket
    # Replace <your_huggingface_dataset> with the actual dataset name
    s3 = boto3.client('s3')
    s3.upload_file('<your_huggingface_dataset>', '<your_s3_bucket>', '<timestamp>_extract_IMDB_comments_from_HF.csv')

    # Display message when finished copying
    print("Dataset copied successfully!")

def remove_html_balises_and_emoji():
    # Read the dataset from S3 bucket
    # Replace <your_s3_bucket> and <timestamp>_extract_IMDB_comments_from_HF.csv with the actual values
    df = pd.read_csv('s3://<your_s3_bucket>/<timestamp>_extract_IMDB_comments_from_HF.csv')

    # Remove HTML balises using regular expressions
    df['text'] = df['text'].apply(lambda x: re.sub('<.*?>', '', x))

    # Remove emojis using regular expressions
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    df['text'] = df['text'].apply(lambda x: emoji_pattern.sub(r'', x))

    # Save the modified dataset back to S3 bucket
    df.to_csv('s3://<your_s3_bucket>/<timestamp>_extract_IMDB_comments_from_HF.csv', index=False)

def display_file_info():
    # Read the modified dataset from S3 bucket
    # Replace <your_s3_bucket> and <timestamp>_extract_IMDB_comments_from_HF.csv with the actual values
    df = pd.read_csv('s3://<your_s3_bucket>/<timestamp>_extract_IMDB_comments_from_HF.csv')

    # Display number of rows and columns
    num_rows = df.shape[0]
    num_cols = df.shape[1]
    print(f"Number of rows: {num_rows}")
    print(f"Number of columns: {num_cols}")

    # Display first 5 rows
    print("First 5 rows:")
    print(df.head(5))

def main():
    start_time = datetime.now()

    copy_dataset_to_s3()
    remove_html_balises_and_emoji()
    display_file_info()

    end_time = datetime.now()
    duration = end_time - start_time

    print(f"Total duration: {duration}")

if __name__ == "__main__":
    main()



# Write a python program to copy a dataset for the tiny-bert model from Huggingface to S3 bucket,
# remove html balises and emoji 
# rename the output with the following pattern "<timestamp>_extract_IMDB_comments_from_HF.csv"
# Display a message  before starting processing and when it's finished plus the total duration of the operation
# Display the number of rows and columns of the output file
# Display the first 5 rows of the output file


import time
import re
import pandas as pd
from datasets import load_dataset
import boto3
from datetime import datetime

def remove_html_tags_and_emoji(text):
    clean_text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    clean_text = emoji_pattern.sub(r'', clean_text)  # Remove emojis
    return clean_text

def main():
    print("Starting the dataset processing...")

    start_time = time.time()

    # Load the dataset from Huggingface
    dataset = load_dataset("imdb")

    # Convert to pandas dataframe
    df = pd.DataFrame(dataset['train'])

    # Remove HTML tags and emojis from the 'text' column
    df['text'] = df['text'].apply(remove_html_tags_and_emoji)

    # Get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Rename the output file
    output_filename = f"{timestamp}_extract_IMDB_comments_from_HF.csv"

    # Save the dataframe to a CSV file
    df.to_csv(output_filename, index=False)

    # Upload to S3 bucket
    s3_client = boto3.client('s3')
    s3_bucket_name = 'your-s3-bucket-name'
    s3_client.upload_file(output_filename, s3_bucket_name, output_filename)

    end_time = time.time()
    duration = end_time - start_time

    print(f"Dataset processing finished in {duration:.2f} seconds.")
    print(f"Output file has {df.shape[0]} rows and {df.shape[1]} columns.")

    # Display first 5 rows of the dataframe
    print(df.head())

if __name__ == "__main__":
    main()
    

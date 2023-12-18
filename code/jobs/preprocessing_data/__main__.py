# Write a python program to copy a dataset for the tiny-bert model from Huggingface to S3 bucket,
# remove html balises and emoji 
# rename the output with the following pattern "<timestamp>_extract_IMDB_comments_from_HF.csv"
# Display a message  before starting processing and when it's finished plus the total duration of the operation
# Display the number of rows and columns of the output file
# Display the first 5 rows of the output file

import time
import pandas as pd
import re
from datasets import load_dataset
import boto3
from datetime import datetime

# Function to remove HTML tags and Emojis from text
def clean_text(text):
    # Remove HTML tags using regex
    clean_html = re.compile('<.*?>')
    text_without_html = re.sub(clean_html, '', text)
    
    # Remove Emojis
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    text_cleaned = emoji_pattern.sub(r'', text_without_html)
    
    return text_cleaned

# AWS S3 bucket details
s3_bucket_name = 'your-s3-bucket-name'
s3_client = boto3.client('s3')

def main():
    start_time = time.time()
    print("Starting the processing...")

    # Load dataset from Huggingface
    dataset = load_dataset("imdb")

    # Process the dataset: remove html balises and emojis
    df = pd.DataFrame(dataset['train'])
    df['text'] = df['text'].apply(clean_text)

    # Get current timestamp for file naming
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    output_filename = f"{timestamp}_extract_IMDB_comments_from_HF.csv"

    # Save dataframe to CSV
    df.to_csv(output_filename, index=False)

    # Upload to S3 bucket
    s3_client.upload_file(output_filename, s3_bucket_name, output_filename)

    end_time = time.time()
    duration = end_time - start_time
    print(f"Finished processing. Total duration: {duration:.2f} seconds.")
    
    # Display number of rows and columns
    num_rows, num_cols = df.shape
    print(f"Number of rows: {num_rows}")
    print(f"Number of columns: {num_cols}")

    # Display the first 5 rows of the output file
    print("First 5 rows of the output file:")
    print(df.head())

if __name__ == "__main__":
    main()

# Write a python program to copy a dataset for the tiny-bert model from Huggingface to S3 bucket,
# remove html balises and emoji 
# rename the output with the following pattern "<timestamp>_extract_comment_IMDB_from_HF.csv.
# Display a message  before starting processing and when it's finished plus the total duration of the operation

import datetime
import boto3
import pandas as pd
import re
from bs4 import BeautifulSoup
import emoji

def remove_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(r'', text)

# Copy dataset from Huggingface to S3 bucket
def copy_dataset_to_s3():
    # Code to copy the dataset to S3 bucket goes here
    pass

# Process the dataset
def process_dataset():
    # Load the dataset
    dataset = pd.read_csv("dataset.csv")

    # Remove HTML tags
    dataset['text'] = dataset['text'].apply(remove_html_tags)

    # Remove emojis
    dataset['text'] = dataset['text'].apply(remove_emoji)

    # Rename the output file
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_filename = f"{timestamp}_extract_comment_IMDB_from_HF.csv"

    # Save the processed dataset to the output file
    dataset.to_csv(output_filename, index=False)

    return output_filename

# Main function
def main():
    print("Starting dataset processing...")
    
    start_time = datetime.datetime.now()
    
    # Copy dataset from Huggingface to S3 bucket
    copy_dataset_to_s3()
    
    # Process the dataset and get the output filename
    output_filename = process_dataset()
    
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    
    print(f"Dataset processing finished. Total duration: {duration}")

if __name__ == "__main__":
    main()

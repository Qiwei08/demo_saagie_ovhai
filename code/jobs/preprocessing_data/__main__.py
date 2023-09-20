# Write a python program to copy a dataset for the tiny-bert model from Huggingface to S3 bucket,
# remove html balises and emoji 
# rename the output with the following pattern "<timestamp>_extract_comment_IMDB_from_HF.csv.
# Display a message  before starting processing and when it's finished plus the total duration of the operation


import time
import boto3
import pandas as pd
from bs4 import BeautifulSoup
import re

# Copy dataset from Huggingface to S3 bucket
def copy_dataset_to_s3():
    # Code to copy dataset from Huggingface to S3 bucket goes here
    pass

# Remove HTML tags from text
def remove_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

# Remove emoji from text
def remove_emoji(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# Rename output file with timestamp and description
def rename_output_file(filename):
    timestamp = time.strftime("%Y%m%d%H%M%S")
    new_filename = f"{timestamp}_extract_comment_IMDB_from_HF.csv"
    # Code to rename the file goes here
    pass

# Main function
def main():
    # Display message before starting processing
    print("Starting data processing...")
    
    # Copy dataset to S3 bucket
    copy_dataset_to_s3()
    
    # Read dataset from S3 bucket into pandas DataFrame
    df = pd.read_csv("s3://your-bucket-name/dataset.csv")
    
    # Remove HTML tags and emoji from comments
    df["comment"] = df["comment"].apply(remove_html_tags)
    df["comment"] = df["comment"].apply(remove_emoji)
    
    # Rename output file
    rename_output_file("dataset.csv")
    
    # Display message after finishing processing
    print("Data processing finished.")
    
# Run the main function
start_time = time.time()
main()
end_time = time.time()
duration = end_time - start_time
print(f"Total duration: {duration} seconds.")


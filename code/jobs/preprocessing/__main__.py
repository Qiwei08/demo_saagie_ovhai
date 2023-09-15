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
    print("Copying dataset to S3 bucket...")
    
    # Copying dataset from Huggingface to S3 bucket
    # Replace 'input_dataset_path' with the actual path of the dataset on Huggingface
    input_dataset_path = "huggingface_dataset_path"
    s3_bucket_name = "your_s3_bucket_name"
    output_dataset_key = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_extract_comment_IMDB_from_HF.csv"
    
    s3 = boto3.client('s3')
    s3.upload_file(input_dataset_path, s3_bucket_name, output_dataset_key)
    
    # Display message after finishing processing
    print("Dataset copied to S3 bucket successfully!")
    
    return output_dataset_key

def remove_html_tags_and_emoji(input_file_path, output_file_path):
    # Display message before starting processing
    print("Removing HTML tags and emojis...")
    
    # Read the dataset file using pandas
    df = pd.read_csv(input_file_path)
    
    # Remove HTML tags using BeautifulSoup
    df['comment'] = df['comment'].apply(lambda x: BeautifulSoup(x, "html.parser").get_text())
    
    # Remove emojis using regex
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    
    df['comment'] = df['comment'].apply(lambda x: emoji_pattern.sub(r'', x))
    
    # Save the modified dataset to a new file
    df.to_csv(output_file_path, index=False)
    
    # Display message after finishing processing
    print("HTML tags and emojis removed successfully!")

def main():
    # Copy dataset to S3 bucket
    output_dataset_key = copy_dataset_to_s3()
    
    # Remove HTML tags and emojis from the copied dataset
    input_file_path = f"s3://{your_s3_bucket_name}/{output_dataset_key}"
    output_file_path = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_extract_comment_IMDB_from_HF_cleaned.csv"
    remove_html_tags_and_emoji(input_file_path, output_file_path)
    
    # Calculate the total duration of the operation
    end_time = time.time()
    duration = end_time - start_time
    
    # Display message with total duration of the operation
    print(f"Processing completed in {duration} seconds.")

if __name__ == "__main__":
    main()



print("Processing ...")
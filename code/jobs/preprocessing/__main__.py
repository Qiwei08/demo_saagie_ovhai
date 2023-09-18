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

# Function to remove HTML tags from text
def remove_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

# Function to remove emojis from text
def remove_emojis(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# Function to copy dataset from Huggingface to S3 bucket
def copy_dataset_to_s3():
    # Copying dataset code here
    pass

# Function to process the dataset
def process_dataset(dataset_path):
    # Read the dataset into a pandas DataFrame
    df = pd.read_csv(dataset_path)

    # Remove HTML tags and emojis from the 'comment' column
    df['comment'] = df['comment'].apply(remove_html_tags)
    df['comment'] = df['comment'].apply(remove_emojis)

    # Generate timestamp for renaming output file
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Rename the output file
    output_filename = f"{timestamp}_extract_comment_IMDB_from_HF.csv"
    df.to_csv(output_filename, index=False)

    return output_filename

# Start of the program
start_time = time.time()

# Display a message before starting processing
print("Starting dataset processing...")

# Copy dataset from Huggingface to S3 bucket
copy_dataset_to_s3()

# Process the dataset and get the output filename
output_filename = process_dataset("path/to/dataset.csv")

# Display a message when finished processing
print(f"Dataset processing finished. Output file: {output_filename}")

# Calculate and display the total duration of the operation
end_time = time.time()
duration = end_time - start_time
print(f"Total duration: {duration} seconds")

print("toto")

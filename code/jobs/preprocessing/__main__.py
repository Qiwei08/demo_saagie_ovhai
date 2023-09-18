# Write a python program to copy a dataset for the tiny-bert model from Huggingface to S3 bucket,
# remove html balises and emoji 
# rename the output with the following pattern "<timestamp>_extract_comment_IMDB_from_HF.csv.
# Display a message  before starting processing and when it's finished plus the total duration of the operation

import boto3
import re
import time
import pandas as pd

# Function to remove HTML tags from a string
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# Function to remove emojis from a string
def remove_emojis(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# Function to copy the dataset to S3 bucket and perform required operations
def process_dataset():
    # Start time
    start_time = time.time()

    # Display message before starting processing
    print("Starting dataset processing...")

    # Copy the dataset to S3 bucket
    s3 = boto3.client('s3')
    s3.download_file('huggingface-datasets', 'tiny-bert-dataset.csv', 'dataset.csv')

    # Read the dataset into a pandas DataFrame
    df = pd.read_csv('dataset.csv')

    # Remove HTML tags and emojis from the 'comment' column
    df['comment'] = df['comment'].apply(remove_html_tags)
    df['comment'] = df['comment'].apply(remove_emojis)

    # Rename the output file with the specified pattern
    timestamp = time.strftime("%Y%m%d%H%M%S")
    output_filename = f"{timestamp}_extract_comment_IMDB_from_HF.csv"
    df.to_csv(output_filename, index=False)

    # Display message after finishing processing
    print("Dataset processing completed!")

    # Calculate total duration of the operation
    duration = time.time() - start_time
    print(f"Total duration: {duration} seconds")

# Call the function to process the dataset
process_dataset()

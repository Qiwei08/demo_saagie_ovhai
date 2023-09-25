# Write a python program to copy a dataset for the tiny-bert model from Huggingface to S3 bucket,
# remove html balises and emoji 
# rename the output with the following pattern "<timestamp>_extract_comment_IMDB_from_HF.csv.
# Display a message  before starting processing and when it's finished plus the total duration of the operation


import boto3
import pandas as pd
import re
from datetime import datetime
import time

# Function to remove HTML tags from text
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

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

# Get current timestamp
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Display message before starting processing
print("Starting data processing...")

# Read dataset from Huggingface
df = pd.read_csv("https://huggingface.co/datasets/prajjwal1/bert-tiny-random/raw/main/train.csv")

# Remove HTML tags and emojis from comments
df['comment'] = df['comment'].apply(remove_html_tags)
df['comment'] = df['comment'].apply(remove_emojis)

# Generate output filename
output_filename = f"{timestamp}_extract_comment_IMDB_from_HF.csv"

# Save processed dataset to S3 bucket
s3 = boto3.client('s3')
df.to_csv(output_filename, index=False)
s3.upload_file(output_filename, 'your-s3-bucket', output_filename)

# Display message after finishing processing
print("Data processing finished.")

# Calculate total duration of the operation
end_time = time.time()
duration = end_time - start_time
print(f"Total duration: {duration} seconds")

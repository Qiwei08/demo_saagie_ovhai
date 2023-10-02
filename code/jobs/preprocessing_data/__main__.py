# Write a python program to copy a dataset for the tiny-bert model from Huggingface to S3 bucket,
# remove html balises and emoji 
# rename the output with the following pattern "<timestamp>_extract_comment_IMDB_from_HF.csv.
# Display a message  before starting processing and when it's finished plus the total duration of the operation


import boto3
import datetime
import re
import emoji
import pandas as pd

# Function to remove HTML tags from text
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# Function to remove emojis from text
def remove_emojis(text):
    return emoji.get_emoji_regexp().sub(r'', text)

# Function to copy dataset to S3 bucket and process it
def copy_dataset_to_s3():
    # Display message before starting processing
    print("Starting data processing...")

    # Copy dataset from Huggingface to S3 bucket
    # Replace 'YOUR_DATASET_URL' with the actual URL of the dataset
    # Replace 'YOUR_BUCKET_NAME' with the name of your S3 bucket
    s3 = boto3.client('s3')
    s3.download_file('YOUR_DATASET_URL', 'dataset.csv', 'YOUR_BUCKET_NAME/dataset.csv')

    # Read dataset into pandas DataFrame
    df = pd.read_csv('dataset.csv')

    # Remove HTML tags and emojis from comments column
    df['comment'] = df['comment'].apply(remove_html_tags)
    df['comment'] = df['comment'].apply(remove_emojis)

    # Rename output file with timestamp and description
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_filename = f"{timestamp}_extract_comment_IMDB_from_HF.csv"
    df.to_csv(output_filename, index=False)

    # Display message after finishing processing
    print("Data processing completed!")

    # Calculate total duration of the operation
    duration = datetime.datetime.now() - start_time
    print(f"Total duration: {duration}")

# Call the function to start processing
start_time = datetime.datetime.now()
copy_dataset_to_s3()

# Write a python program to copy a dataset for the tiny-bert model from Huggingface to S3 bucket,
# remove html balises and emoji 
# rename the output with the following pattern "<timestamp>_extract_IMDB_comments_from_HF.csv"
# Display a message  before starting processing and when it's finished plus the total duration of the operation

import time
import re
import boto3
from datasets import load_dataset
from datetime import datetime

# Function to remove HTML tags and Emojis from text
def clean_text(text):
    # Remove HTML tags using regex
    clean_html = re.sub(r'<.*?>', '', text)
    # Remove Emojis and other unicode characters not in the ASCII range
    clean_emoji = re.sub(r'[^\x00-\x7F]+', '', clean_html)
    return clean_emoji

# Main function to process the dataset and upload it to S3
def main():
    print("Starting the data processing...")

    start_time = time.time()

    # Load dataset from Huggingface
    dataset = load_dataset('imdb')

    # Clean the dataset by removing html tags and emojis
    dataset_cleaned = dataset.map(lambda example: {'text': clean_text(example['text'])})

    # Convert to pandas dataframe
    df = dataset_cleaned['train'].to_pandas()

    # Get current timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # Define the output filename
    output_filename = f"{timestamp}_extract_IMDB_comments_from_HF.csv"

    # Save the dataframe to a CSV file
    df.to_csv(output_filename, index=False)

    # Initialize boto3 S3 client
    s3_client = boto3.client('s3')

    # Define your bucket name here
    bucket_name = 'your-bucket-name'

    # Upload the CSV file to S3 bucket
    s3_client.upload_file(output_filename, bucket_name, output_filename)

    end_time = time.time()
    duration = end_time - start_time

    print(f"Data processing completed. The file has been saved to S3 as {output_filename}")
    print(f"Total duration of operation: {duration:.2f} seconds.")

# Run the main function
if __name__ == '__main__':
    main()

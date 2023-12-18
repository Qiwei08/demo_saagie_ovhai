# Write a python program to copy a dataset for the tiny-bert model from Huggingface to S3 bucket,
# remove html balises and emoji 
# rename the output with the following pattern "<timestamp>_extract_IMDB_comments_from_HF.csv"
# Display a message  before starting processing and when it's finished plus the total duration of the operation
# Display the number of rows and columns of the output file
# Display the first 5 rows of the output file


import time
import pandas as pd
import boto3
from datasets import load_dataset
import re
from datetime import datetime

# Function to remove HTML tags and Emojis
def clean_text(text):
    # Remove HTML tags using regex
    clean_html = re.sub(r'<.*?>', '', text)
    # Remove Emojis using regex
    clean_text = re.sub(r'[^\w\s,]', '', clean_html)
    return clean_text

def main():
    print("Starting the dataset processing...")

    start_time = time.time()

    # Load the dataset from Huggingface
    dataset = load_dataset('imdb', split='train')

    # Convert the dataset to pandas dataframe
    df = pd.DataFrame(dataset)

    # Apply the cleaning function to reviews
    df['text'] = df['text'].apply(clean_text)

    # Get current timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # Define the output filename
    output_filename = f"{timestamp}_extract_IMDB_comments_from_HF.csv"

    # Save the cleaned data to a csv file
    df.to_csv(output_filename, index=False)

    # Upload the file to S3 bucket
    s3_client = boto3.client('s3')
    bucket_name = 'your-bucket-name'  # Replace with your bucket name
    s3_client.upload_file(output_filename, bucket_name, output_filename)

    end_time = time.time()
    duration = end_time - start_time

    print(f"Finished processing. The operation took {duration:.2f} seconds.")
    print(f"Number of rows: {df.shape[0]}")
    print(f"Number of columns: {df.shape[1]}")
    print("First 5 rows of the output file:")
    print(df.head())

if __name__ == "__main__":
    main()

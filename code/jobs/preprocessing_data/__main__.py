# Write a python program to copy a dataset for the tiny-bert model from Huggingface to S3 bucket,
# remove html balises and emoji 
# rename the output with the following pattern "<timestamp>_extract_comment_IMDB_from_HF.csv.
# Display a message  before starting processing and when it's finished plus the total duration of the operation

import time
import re
from datasets import load_dataset
import boto3
from datetime import datetime

# Function to remove HTML tags and emojis from text
def clean_text(text):
    clean_html = re.compile('<.*?>')
    clean_emoji = re.compile("["
                             u"\U0001F600-\U0001F64F"  # emoticons
                             u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                             u"\U0001F680-\U0001F6FF"  # transport & map symbols
                             u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                             u"\U00002702-\U000027B0"
                             u"\U000024C2-\U0001F251"
                             "]+", flags=re.UNICODE)
    return re.sub(clean_emoji, '', re.sub(clean_html, '', text))

def main():
    print("Starting the data processing...")

    start_time = time.time()

    # Load dataset from Huggingface
    dataset = load_dataset("imdb")

    # Perform cleaning operation on the dataset
    cleaned_dataset = dataset.map(lambda x: {'text': clean_text(x['text'])})

    # Convert the cleaned dataset to pandas dataframe
    df = cleaned_dataset['train'].to_pandas()

    # Get current timestamp for file naming
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Define the output filename pattern
    output_filename = f"{timestamp}_extract_comment_IMDB_from_HF.csv"

    # Save the dataframe to a CSV file
    df.to_csv(output_filename, index=False)

    # Upload the CSV file to S3 bucket
    s3_client = boto3.client('s3')
    s3_client.upload_file(output_filename, 'your-bucket-name', output_filename)

    end_time = time.time()
    duration = end_time - start_time

    print(f"Data processing completed. Total duration: {duration:.2f} seconds.")

if __name__ == "__main__":
    main()


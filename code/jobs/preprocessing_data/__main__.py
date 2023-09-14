import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime
import boto3

# Copy dataset from Huggingface to S3 bucket
def copy_dataset_to_s3():
    # Your code to copy the dataset from Huggingface to S3 bucket goes here
    pass

# Remove HTML tags and emojis from dataset
def remove_html_and_emoji(text):
    # Remove HTML tags
    soup = BeautifulSoup(text, "html.parser")
    text_without_html = soup.get_text()
    
    # Remove emojis
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    text_without_html_and_emoji = emoji_pattern.sub(r'', text_without_html)

    return text_without_html_and_emoji

# Rename output file with the specified pattern
def rename_output_file(output_file_path):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    new_filename = f"{timestamp}_extract_comment_IMDB_from_HF.csv"
    
    # Rename the file using the new filename
    # Make sure to provide the appropriate path, including the bucket name, if applicable
    s3 = boto3.client('s3')
    s3.copy_object(Bucket='your-bucket-name', CopySource=output_file_path, Key=new_filename)
    s3.delete_object(Bucket='your-bucket-name', Key=output_file_path)

# Main execution
def main():
    # Copy dataset from Huggingface to S3 bucket
    copy_dataset_to_s3()
    
    # Remove HTML tags and emojis from dataset
    df = pd.read_csv('path-to-input-file.csv')  # Replace with the path to your input file
    df['text'] = df['text'].apply(remove_html_and_emoji)
    
    # Save cleaned dataset to a new file
    output_file_path = 'path-to-output-file.csv'  # Replace with the desired path for the output file
    df.to_csv(output_file_path, index=False)
    
    # Rename the output file
    rename_output_file(output_file_path)

if __name__ == "__main__":
    main()



import os
import tiktoken
from docx import Document
import pdfplumber
import sys
from pathlib import Path

def count_tokens_in_text(text):
    """Count tokens in text using tiktoken."""
    enc = tiktoken.get_encoding("o200k_base")
    
    return len(enc.encode(text))

def extract_text_from_docx(file_path):
    """Extract text from .docx file."""
    doc = Document(file_path)
    return " ".join([paragraph.text for paragraph in doc.paragraphs])

def extract_text_from_pdf(file_path):
    """Extract text from PDF file."""
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def main():
    print("\n\n TOKEN COUNTER(tm) - (c) 1984 Madssoft Inc.\n-All your base are belong to us!\n----------------------------------\nPress Ctrl+C to exit\n")
    while True:
        try:
            # Get folder path from user and normalize it
            folder_path = input("Please enter the absolute path to the folder: ").strip()
            
            # Convert the string path to a Path object and resolve it
            folder_path = Path(folder_path).resolve()
            
            # Verify folder exists
            if not folder_path.is_dir():
                print("Error: The specified folder does not exist.")
                return

            total_tokens = 0
            file_count = 0

            # Process each file in the folder
            for file_path in folder_path.iterdir():
                # Skip if not a file
                if not file_path.is_file():
                    continue

                # Get file extension
                ext = file_path.suffix.lower()

                # Process only specific file types
                if ext not in ['.txt', '.docx', '.pdf']:
                    continue

                try:
                    # Extract text based on file type
                    if ext == '.txt':
                        text = file_path.read_text(encoding='utf-8')
                    elif ext == '.docx':
                        text = extract_text_from_docx(file_path)
                    elif ext == '.pdf':
                        text = extract_text_from_pdf(file_path)

                    # Count tokens
                    token_count = count_tokens_in_text(text)
                    total_tokens += token_count
                    file_count += 1

                    # Print results for this file
                    print(f"{file_path.name}: {token_count} tokens")

                except Exception as e:
                    print(f"Error processing {file_path.name}: {str(e)}")

            # Print total
            if file_count > 0:
                print("\nTotal number of tokens across all files:", total_tokens)
            else:
                print("\nNo compatible files found in the specified folder.")


        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
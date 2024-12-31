import os
import csv
import requests
from urllib.parse import urlparse, quote
from pathlib import Path

def sanitize_filename(url):
    parsed_url = urlparse(url)
    filename = quote(parsed_url.path.strip('/').replace('/', '-')).replace('%', '_')
    return filename or "unnamed.mp3"

def download_mp3s_from_csv(csv_file_path):
    output_folder = "audio"
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)

        if "Audio URL" not in headers:
            print("Error: 'Audio URL' column not found in the CSV file.")
            return

        url_column_index = headers.index("Audio URL")

        for row in reader:
            if len(row) > url_column_index:
                url = row[url_column_index]
                if url:
                    try:
                        response = requests.get(url, stream=True)
                        response.raise_for_status()

                        filename = sanitize_filename(url)
                        output_path = os.path.join(output_folder, filename)

                        with open(output_path, 'wb') as audio_file:
                            for chunk in response.iter_content(chunk_size=8192):
                                audio_file.write(chunk)

                        print(f"Downloaded: {filename}")
                    except requests.exceptions.RequestException as e:
                        print(f"Error downloading {url}: {e}")

if __name__ == "__main__":
    language_code = input("What the language code? It can be found at the end of the URL (i.e. Marathi is 'mr' in https://www.50languages.com/em/learn/phrasebook-lessons/162/mr): \n")
    csv_file = language_code + "_language_flashcards.csv"  # Replace with your CSV file path
    download_mp3s_from_csv(csv_file)
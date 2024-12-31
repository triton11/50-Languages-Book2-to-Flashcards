import requests
from bs4 import BeautifulSoup
import csv
import re
from urllib.parse import urlparse, quote

def anki_file(filename):
    return "[sound:" + filename + "]"

def scrape_lesson_data(start_lesson, end_lesson, output_file, language_code):
    # Define the base URL and the headers for the CSV
    # Replace with your language URL 
    base_url = "https://www.50languages.com/em/learn/phrasebook-lessons/{}/" + language_code
    headers = ["Index", "Lesson Title", "English text", "Phonetic translation", "Original language translation", "Audio File Name", "Audio URL"]

    # Open the CSV file for writing
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        index_count = 0

        # Loop through each lesson page
        for lesson in range(start_lesson, end_lesson + 1):
            url = base_url.format(lesson)
            response = requests.get(url)
            
            if response.status_code != 200:
                print(f"Failed to retrieve lesson {lesson} (status code: {response.status_code})")
                continue

            soup = BeautifulSoup(response.content, "html.parser")

            # Extract lesson number and name information
            lesson_div = soup.find("div", class_="flex-row text-center bg-default no_print phrasebook_lesson_mainn_img")
            if lesson_div:
                # Lesson number English text
                lesson_number_english = lesson_div.find("h3", class_="bold mt80 text_lineheight")
                lesson_number_english_text = lesson_number_english.get_text(strip=True) if lesson_number_english else ""

                # Lesson number phonetic translation
                lesson_number_phonetic = lesson_div.find("div", class_="lessonhfive").find("h3", class_="not-in-bold font-weight-normal")
                lesson_number_phonetic_text = lesson_number_phonetic.get_text(strip=True) if lesson_number_phonetic else ""

                # Lesson number original language translation
                lesson_number_original = lesson_div.find("div", class_="lessonhfive").find("h3", class_="text_lineheight text-blue")
                lesson_number_original_text = lesson_number_original.get_text(strip=True) if lesson_number_original else ""

                # Lesson number pronunciation URL
                lesson_number_audio = lesson_div.find("div", class_="lessonhfive").find("div", class_="d-flex").find_all("audio")[-1]
                lesson_number_audio_url = lesson_number_audio.find("source")["src"] if lesson_number_audio and lesson_number_audio.find("source") else ""
                lesson_number_audio_url_parsed = urlparse(lesson_number_audio_url)
                lesson_number_audio_file = anki_file(quote(lesson_number_audio_url_parsed.path.strip('/').replace('/', '-')).replace('%', '_'))

                # Lesson title English text
                lesson_title_english = lesson_div.find("div", class_="col-sm-4 lesson-title").find_all("h3", class_="text_lineheight")[-1]
                lesson_title_english_text = lesson_title_english.get_text(strip=True) if lesson_title_english else ""

                # Lesson title phonetic translation
                lesson_title_phonetic = lesson_div.find("div", class_="linetext-height").find("h3", class_="not-in-bold font-weight-normal")
                lesson_title_phonetic_text = lesson_title_phonetic.get_text(strip=True) if lesson_title_phonetic else ""

                # Lesson title original language translation
                lesson_title_original = lesson_div.find("div", class_="linetext-height").find("h3", class_="text_lineheight text-blue")
                lesson_title_original_text = lesson_title_original.get_text(strip=True) if lesson_title_original else ""

                # Lesson title pronunciation URL
                lesson_title_audio = lesson_div.find("div", class_="lesson-titldivv").find_all("audio")[-1]
                lesson_title_audio_url = lesson_title_audio.find_all("source")[-1]["src"] if lesson_title_audio and lesson_title_audio.find("source") else ""
                lesson_title_audio_url_parsed = urlparse(lesson_title_audio_url)
                lesson_title_audio_file = anki_file(quote(lesson_title_audio_url_parsed.path.strip('/').replace('/', '-')).replace('%', '_'))

                # Write lesson number row to CSV
                index_count += 1
                writer.writerow([
                    index_count,
                    lesson_number_english_text + " " + lesson_title_english_text,
                    lesson_number_english_text,
                    lesson_number_phonetic_text,
                    lesson_number_original_text,
                    lesson_number_audio_file,
                    lesson_number_audio_url
                ])

                # Write lesson title row to CSV
                index_count += 1
                writer.writerow([
                    index_count,
                    lesson_number_english_text + " " + lesson_title_english_text,
                    lesson_title_english_text,
                    lesson_title_phonetic_text,
                    lesson_title_original_text,
                    lesson_title_audio_file,
                    lesson_title_audio_url
                ])

            # Find the table with the translations
            table = soup.find("table", id="table1")
            if not table:
                print(f"Table not found in lesson {lesson}")
                continue

            # Process each row in the table
            for row in table.find_all("tr"):  # Skip header row
                try:
                    # Extract English text
                    english_cell = row.find("td", class_="nativee_txtt mb-mob-0")
                    english_text = english_cell.get_text(strip=True) if english_cell else ""

                    # Extract phonetic translation and original language translation
                    translation_cell = row.find("td", class_="left-dr target-phrase")
                    phonetic_span = translation_cell.find("span", class_="transliteration-text", id=re.compile(r"^visible_\d+")) if translation_cell else None
                    original_span = translation_cell.find("span", class_="text-blue", id=re.compile(r"^visible_\d+")) if translation_cell else None

                    phonetic_translation = phonetic_span.get_text(strip=True) if phonetic_span else ""
                    original_translation = original_span.get_text(strip=True) if original_span else ""

                    # Extract audio URL
                    audio_cell = row.find("td", class_="justify-content-center-mob")
                    audio_source = audio_cell.find_all("source")[-1] if audio_cell else None
                    audio_url = audio_source["src"] if audio_source else ""
                    audio_url_parsed = urlparse(audio_url)
                    audio_file = anki_file(quote(audio_url_parsed.path.strip('/').replace('/', '-')).replace('%', '_'))

                    # Write row to CSV
                    index_count += 1
                    writer.writerow([
                        index_count,
                        lesson_number_english_text + " " + lesson_title_english_text,
                        english_text, 
                        phonetic_translation, 
                        original_translation,
                        audio_file,
                        audio_url
                    ])
                except Exception as e:
                    print(f"Error processing row: {e}")

if __name__ == "__main__":
    # Define the lesson range and output file name
    language_code = input("What the language code? It can be found at the end of the URL (i.e. Marathi is 'mr' in https://www.50languages.com/em/learn/phrasebook-lessons/162/mr):\n")
    start_lesson = int(input("What is the index of the first page of the phrase book? It is the number in the URL of the first chapter (i.e. Marathi is '162' from https://www.50languages.com/em/learn/phrasebook-lessons/162/mr):\n"))
    end_lesson = int(input("What is the index of the last page of the phrase book? It is the number in the URL of the last chapter (i.e. Marathi is '261' from https://www.50languages.com/em/learn/phrasebook-lessons/261/mr):\n"))


    output_file = language_code + "_language_flashcards.csv"

    # Run the scraper
    scrape_lesson_data(start_lesson, end_lesson, output_file, language_code)
    print(f"Data scraping complete. Output saved to {output_file}")

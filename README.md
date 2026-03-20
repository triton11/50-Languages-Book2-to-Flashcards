# 50-Languages-Book2-to-Flashcards

Scripts to create Anki flashcards with audio from any [50languages.com](https://www.50languages.com) phrasebook.

## Prerequisites

- Python 3.6+
- Required packages:
  ```bash
  pip install cloudscraper beautifulsoup4 requests
  ```

## Overview

This project includes two scripts:

1. **`scraper.py`** - Scrapes phrase data (English, transliteration, target language, audio URLs) from 50languages.com
2. **`language_downloader.py`** - Downloads all MP3 audio files from the generated CSV

## Step 1: Find Your Language Parameters

1. Go to [50languages.com](https://www.50languages.com)
2. Navigate to a phrasebook for your target language
3. From the URL, note:
   - **Language code**: The 2-letter code at the end (e.g., `el` for Greek, `mr` for Marathi)
   - **First lesson number**: The number in the URL of the first lesson
   - **Last lesson number**: The number in the URL of the last lesson

Example URL: `https://www.50languages.com/em/learn/phrasebook-lessons/162/el`
- Language code: `el`
- Lesson number: `162`

## Step 2: Run the Scraper

```bash
python3 scraper.py
```

You'll be prompted to enter:
- Language code (e.g., `el`)
- First lesson index (e.g., `162`)
- Last lesson index (e.g., `261`)

This creates a CSV file named `{language_code}_language_flashcards.csv` with columns:
- Index
- Lesson Title
- English text
- Phonetic translation
- Original language translation
- Audio File Name
- Audio URL

## Step 3: Download Audio Files

```bash
python3 language_downloader.py
```

Enter the same language code when prompted. Audio files will be downloaded to the `audio/` folder.

## Step 4: Import into Anki

1. Open Anki and create a new deck
2. Go to **File > Import**
3. Select your CSV file (`{language_code}_language_flashcards.csv`)
4. Configure the field mapping:
   - Map "English text" to Front
   - Map "Original language translation" and/or "Phonetic translation" to Back
   - Map "Audio File Name" to a field that supports audio
5. Copy all files from the `audio/` folder to your Anki media folder:
   - **Mac**: `~/Library/Application Support/Anki2/{profile}/collection.media/`
   - **Windows**: `%APPDATA%\Anki2\{profile}\collection.media\`
   - **Linux**: `~/.local/share/Anki2/{profile}/collection.media/`

## Example: Greek

```bash
# Scrape Greek phrasebook (lessons 162-261)
python3 scraper.py
# Enter: el, 162, 261

# Download audio
python3 language_downloader.py
# Enter: el
```

## Troubleshooting

- **403 errors**: The scraper uses `cloudscraper` to bypass Cloudflare protection. Ensure it's installed.
- **Missing data**: The website structure may change. Check that the CSS selectors in `scraper.py` still match.
- **Encoding issues**: The scraper uses UTF-8 encoding to handle non-Latin scripts.

## Credits

Based on content from [50languages.com](https://www.50languages.com) / [book2](https://www.book2.nl).

See the [detailed tutorial on Medium](https://tristrumtuttle.medium.com/creating-anki-flashcards-with-audio-from-any-book2-50languages-phrasebook-7714f93ba6ca) for more information.

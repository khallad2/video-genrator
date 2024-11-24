import os
import logging
import requests
from dotenv import load_dotenv
from datetime import date

# Set up logging to a file
logging.basicConfig(filename='voiceover_generation.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

# Set up Elevenlabs API key
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Set up Elevenlabs VOICE_ID
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

# Elevenlabs API endpoint
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech/" + ELEVENLABS_VOICE_ID


# Function to read the script from a text file in chunks
def read_script_in_chunks(script_filename, chunk_size=1000):
    try:
        with open(script_filename, "r", encoding="utf-8") as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                yield chunk
    except FileNotFoundError:
        logging.error(f"Script file '{script_filename}' not found.")
        exit(1)
    except Exception as e:
        logging.error(f"Error reading script file: {e}")
        exit(1)


# Function to generate voiceover using Elevenlabs API in chunks
def generate_voiceover(script_filename, output_filename):
    headers = {
        'xi-api-key': ELEVENLABS_API_KEY,
        'Accept': 'audio/mpeg',
        'Content-Type': 'application/json'
    }

    voice_id = os.getenv("ELEVENLABS_VOICE_ID", "Brian")
    url = ELEVENLABS_API_URL.format(voice_id=voice_id)

    try:
        with open(output_filename, 'wb') as audio_file:
            for script_chunk in read_script_in_chunks(script_filename):
                payload = {
                    "text": script_chunk,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.5
                    }
                }
                response = requests.post(url, headers=headers, json=payload, stream=True)
                response.raise_for_status()
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        audio_file.write(chunk)
        logging.info(f"Voiceover generated and saved to '{output_filename}' successfully.")
        print(f"Voiceover generated and saved to '{output_filename}' successfully.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error generating voiceover: {e}")
        print(f"Error generating voiceover. Please check the logs.")
        exit(1)


# Main script
def main():
    # Define the script file and output file names
    today = date.today().strftime("%Y-%m-%d")
    script_filename = f"war_news_script_{today}.txt"
    output_filename = f"war_news_voiceover_{today}.mp3"

    # Generate the voiceover using Elevenlabs API
    logging.info("Generating voiceover from the script.")
    generate_voiceover(script_filename, output_filename)


# Run the script
if __name__ == "__main__":
    main()

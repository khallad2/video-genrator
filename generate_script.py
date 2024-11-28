import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')

try:
    import requests
    import google.generativeai as genai
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Import error: {e}. Please make sure all dependencies are installed in your virtual environment.")
    exit(1)

import datetime
from datetime import date
import os
import logging

# Set up logging to a file
logging.basicConfig(filename='script_generation.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

# Set up Gemini API key
API_KEY = os.getenv("API_KEY")

# Configure the Google Generative AI library
genai.configure(api_key=API_KEY)

# Set the desired video length in minutes
video_length_minutes = 1

# Function to create an attractive script from the news
def create_script(news_items, regions, video_length_minutes, prompt, intro, sub_intro, outro):
    script_lines = []
    script_lines.append(intro)
    script_lines.append("\n")
    script_lines.append(sub_intro)
    script_lines.append("\n")

    item_count = 0
    total_seconds = video_length_minutes * 60
    estimated_time_per_item = 20  # Assuming each news item takes roughly 20 seconds to present

    for item in news_items:
        if any(region in item.get('title', '') or region in item.get('description', '') for region in regions):
            title = item.get('title', 'No Title')
            description = item.get('description', 'No Description')
            url = item.get('url', 'No URL')
            script_lines.append(f"• {title} - {description} Source: {url}")
            script_lines.append("\n")
            item_count += 1

    # Add filler content if there are not enough news items to reach the desired video length
    model = genai.GenerativeModel("gemini-1.5-flash")
    keywords = []
    while item_count * estimated_time_per_item < total_seconds:
        try:
            filler_content = model.generate_content(
                prompt
            )
            response_text = filler_content.text
            script_part, keyword_part = response_text.split('keyWordsForImages', 1)
            script_lines.append("\n")
            script_lines.append(script_part.strip())
            keywords.extend(keyword_part.strip().split('\n'))
        except Exception as e:
            logging.error(f"Error generating filler content: {e}")
            script_lines.append("\nError generating filler content. Please check the logs.\n")
        item_count += 1

    script_lines.append("\n")
    script_lines.append(
        outro)

    return "\n".join(script_lines), keywords


# Function to save keywords to a text file
def save_keywords(keywords, filename):
    unique_keywords = set(keywords)
    with open(filename, "w", encoding="utf-8") as file:
        for keyword in unique_keywords:
            words = keyword.split()[:3]  # Limit to three words per line
            if len(words) > 0:
                file.write(" ".join(words) + "\n")


# Function to translate script to Arabic
def translate_script_to_arabic(script_content):
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        translation_content = model.generate_content(
            f"Translate the following English text to Egyptian Arabic:\n{script_content}"
            "Critical:  Make sure that there is no '*' in the script and only arabic is allowed."
        )
        return translation_content.text.strip()
    except Exception as e:
        logging.error(f"Error generating Arabic translation: {e}")
        return "Error generating Arabic translation. Please check the logs."

# Function to translate script to German
def translate_script_to_german(script_content):
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        translation_content = model.generate_content(
            f"Translate the following English text to German:\n{script_content}"
            "Critical:  Make sure that there is no '*' in the script and only german is allowed."
        )
        return translation_content.text.strip()
    except Exception as e:
        logging.error(f"Error generating German translation: {e}")
        return "Error generating Arabic translation. Please check the logs."

# Main script
def main():
    # prompt = "Provide a concise and informative summary of maximum 2 lines about the current European conflict developments without repeating introductory phrases. Focus on war and conflict events in Europe, key updates, and notable diplomatic activities, ensuring a continuous and engaging flow throughout the segment. The tone should be authoritative and engaging. Include a few keywords at the end under the title 'keyWordsForImages'."
    # prompt = "Create a concise and informative 3-line motivational text aimed at professionals, for a viral Instagram and YouTube video that motivates professionals to stop procrastinating and become more active. Start with a compelling hook to grab attention instantly, followed by relatable examples, quick actionable tips, and an energetic tone. Conclude with a strong call-to-action to inspire viewers to take immediate steps and share the video. The tone should be authoritative and engaging. Ensure that the response does not include any special characters except for ?, !, and. Make sure that there is no * in the script. Include keywords at the end under the title 'keyWordsForImages' every keyword in separate line without any special character."
    prompt = ("Summarize atomic Habits book in maximum 10 lines, in a professional and engaging way, highlighting the main points, key techniques, and central topics covered. Provide clear explanations of the concepts and actionable takeaways where applicable. Ensure the summary captures the essence of the book while maintaining an authoritative and captivating tone suitable for professional readers."
              "The tone should be authoritative and engaging. "
              "Ensure that the response does not include any special characters like '*'."
              "Critical:  Make sure that there is no '*' in the script."
              "Include number of keywords for the most relevant image search in bing at the end under the title 'keyWordsForImages' every keyword in separate line without any special character."
              )
    intro = "" #"Welcome to today's motivational guide on breaking free from procrastination and taking charge of your professional life!"
    sub_intro = "" #"practical strategies, actionable advice, and inspiring examples to help you stay active and achieve your goals."
    outro = ""
    logging.info("We are writing the script. It can take up to 3 minutes!")
    # Create the script
    script_content, keywords = create_script([], [], video_length_minutes, prompt, intro, sub_intro, outro)
    logging.info("We are creating the script file. It can take up to 1 minute!")
    # Save the script to a .txt file with today's date
    today = date.today().strftime("%Y-%m-%d")
    script_filename = f"book_summary_script_{today}.txt"

    with open(script_filename, "w", encoding="utf-8") as file:
        file.write(script_content)

    logging.info(f"The script file '{script_filename}' has been created and is ready!")
    print(f"The script file '{script_filename}' has been created and is ready!")

    # Save keywords to a separate file
    keywords_filename = f"image_search_{today}.txt"
    save_keywords(keywords, keywords_filename)
    logging.info(f"The keywords file '{keywords_filename}' has been created and is ready!")
    print(f"The keywords file '{keywords_filename}' has been created and is ready!")

    # Generate Arabic translation of the script
    logging.info("Translating the script to Arabic.")
    arabic_translation = translate_script_to_arabic(script_content)
    translation_filename = f"book_summary_script_arabic_{today}.txt"

    with open(translation_filename, "w", encoding="utf-8") as file:
        file.write(arabic_translation)

    logging.info(f"The Arabic translation file '{translation_filename}' has been created and is ready!")
    print(f"The Arabic translation file '{translation_filename}' has been created and is ready!")

    # Generate German translation of the script
    logging.info("Translating the script to German.")
    german_translation = translate_script_to_german(script_content)
    german_translation_filename = f"book_summary_script_german_{today}.txt"

    with open(german_translation_filename, "w", encoding="utf-8") as file:
        file.write(german_translation)

    logging.info(f"The German translation file '{german_translation_filename}' has been created and is ready!")
    print(f"The German translation file '{german_translation_filename}' has been created and is ready!")


# Run the script
if __name__ == "__main__":
    main()

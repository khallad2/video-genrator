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

# Specify the regions for war news coverage
regions = ["Europe", "Middle East"]

# Set the desired video length in minutes
video_length_minutes = 1


# Function to create an attractive script from the news
def create_script(news_items, regions, video_length_minutes):
    script_lines = []
    script_lines.append("Welcome to today's in-depth coverage of the ongoing global conflicts and important updates!")
    script_lines.append("\n")
    script_lines.append(
        "Here are the top developments in Europe and the Middle East, providing you with all the critical updates from the front lines and diplomatic tables around the world:")
    script_lines.append("\n")

    item_count = 0
    total_seconds = video_length_minutes * 60
    estimated_time_per_item = 20  # Assuming each news item takes roughly 20 seconds to present

    for item in news_items:
        if any(region in item.get('title', '') or region in item.get('description', '') for region in regions):
            script_lines.append(
                f"• {item.get('title', 'No Title')} - {item.get('description', 'No Description')} Source: {item.get('url', 'No URL')}")
            script_lines.append("\n")
            item_count += 1

    # Add filler content if there are not enough news items to reach the desired video length
    model = genai.GenerativeModel("gemini-1.5-flash")
    while item_count * estimated_time_per_item < total_seconds:
        try:
            filler_content = model.generate_content(
                "Provide a concise and informative summary of the current global conflict developments without repeating introductory phrases. Focus on war and conflict events in MiddleEast and Europe, key updates, and notable diplomatic activities, ensuring a continuous and engaging flow throughout the segment. The tone should be authoritative and engaging."
            )
            script_lines.append("\n")
            script_lines.append(filler_content.text)
        except Exception as e:
            logging.error(f"Error generating filler content: {e}")
            script_lines.append("\nError generating filler content. Please check the logs.\n")
        item_count += 1

    script_lines.append("\n")
    script_lines.append(
        "That's all for today on the major conflicts and diplomatic efforts unfolding globally. Stay informed by subscribing to our channel and turning on notifications for daily updates!")

    return "\n".join(script_lines)


# Main script
def main():
    logging.info("We are writing the script. It can take up to 3 minutes!")
    # Create the script
    script_content = create_script([], regions, video_length_minutes)
    logging.info("We are creating the script file. It can take up to 1 minute!")
    # Save the script to a .txt file with today's date
    today = date.today().strftime("%Y-%m-%d")
    filename = f"war_news_script_{today}.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(script_content)

    logging.info(f"The script file '{filename}' has been created and is ready!")
    print(f"The script file '{filename}' has been created and is ready!")


# Run the script
if __name__ == "__main__":
    main()

import os
import requests
from bs4 import BeautifulSoup
from datetime import date
import logging
import re

# Set up logging to a file
logging.basicConfig(filename='visuals_download.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Function to search Bing for images using web scraping
def bing_search(query, search_type="images"):
    if search_type == "images":
        search_url = f"https://www.bing.com/images/search?q={query.replace(' ', '+')}&form=HDRSC2"
    else:
        logging.error(f"Invalid search type: {search_type}")
        return []

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        media_urls = []

        # Extract image URLs from the search results
        image_elements = soup.find_all('a', {'class': 'iusc'})
        for element in image_elements:
            m = re.search(r'murl":"(https://.*?)"', str(element))
            if m:
                media_urls.append(m.group(1))

        return media_urls
    except requests.exceptions.RequestException as e:
        logging.error(f"Error performing Bing search: {e}")
        return []


# Function to download media from a URL
def download_media(url, output_folder, media_type="image"):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        file_extension = "jpg" if media_type == "image" else "mp4"
        file_name = os.path.join(output_folder, f"{media_type}_{os.path.basename(url).split('?')[0]}.{file_extension}")
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        logging.info(f"{media_type.capitalize()} downloaded successfully: {file_name}")
        print(f"{media_type.capitalize()} downloaded successfully: {file_name}")
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading {media_type} from {url}: {e}")
        print(f"Error downloading {media_type} from {url}. Please check the logs.")
        return False


# Main script to perform Bing searches and download related visuals
def main():
    today = date.today().strftime("%Y-%m-%d")
    # Read keywords from image_search.txt
    keywords_file = f"image_search_{today}.txt"
    output_folder = "visuals"

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Check if keywords file exists
    if not os.path.exists(keywords_file):
        logging.error(f"Keywords file '{keywords_file}' not found.")
        print(f"Keywords file '{keywords_file}' not found.")
        return

    with open(keywords_file, "r", encoding="utf-8") as file:
        keywords = [line.strip() for line in file.readlines()]

    # Perform Bing search for images related to the keywords
    logging.info("Performing Bing search for visuals related to the keywords.")
    total_images_downloaded = 0
    max_images_per_keyword = 1

    for keyword in keywords:
        logging.info(f"Searching for visuals related to: {keyword}")
        search_results_images = bing_search(keyword, search_type="images")

        # Extract and download images
        images_downloaded = 0
        for url in search_results_images:
            if images_downloaded >= max_images_per_keyword:
                break
            if download_media(url, output_folder, media_type="image"):
                images_downloaded += 1
                total_images_downloaded += 1

    logging.info(f"Total images downloaded: {total_images_downloaded}")
    print(f"Total images downloaded: {total_images_downloaded}")


# Run the script
if __name__ == "__main__":
    main()

# Foundational prompt:
# Code to parse selection.html, extract image URLs, and save them to a local folder.
# Add a function to save the array of image URLs to a JSON file.

import os
import requests
from bs4 import BeautifulSoup
import json  # Import json module

# Define the local HTML file and the output directory
html_file = 'selection.html'
output_dir = 'downloaded_images'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Ensure the HTML file exists
if not os.path.exists(html_file):
    print(f"Error: The file {html_file} does not exist.")
    exit(1)

# Read and parse the HTML file
try:
    with open(html_file, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
except Exception as e:
    print(f"Error reading {html_file}: {e}")
    exit(1)

# Base URL for relative paths
base_url = 'https://www.wwf-climaterealism.com/sequence/sequence05/img/'

# Extract image URLs
image_urls = []
for img in soup.find_all('img'):
    src = img.get('src')
    if src:
        print(f"Found image src: {src}")  # Debugging: Print each found src
    if src and src.startswith('./sequence/sequence05/img/'):
        src = base_url + src[len('./sequence/sequence05/img/'):]
    if src and src.startswith('https://www.wwf-climaterealism.com/sequence/sequence05/img/'):
        image_urls.append(src)

# Define the JSON output file
json_output_file = 'image_urls.json'

# Function to save image URLs to a JSON file with local paths
def save_image_urls_to_json(image_urls, json_file, output_dir):
    local_image_urls = [os.path.join(output_dir, url.split('/')[-1]) for url in image_urls]
    try:
        with open(json_file, 'w') as file:
            json.dump(local_image_urls, file, indent=4)
        print(f"Image URLs saved to {json_file}")
    except Exception as e:
        print(f"Error saving image URLs to JSON file: {e}")

# Debugging: Print the extracted image URLs
if not image_urls:
    print("No image URLs found. Please check the HTML file and the URL pattern.")
else:
    print("Extracted image URLs:", image_urls)
    save_image_urls_to_json(image_urls, json_output_file, output_dir)  # Save image URLs to JSON file with local paths

# Download and save each image
for url in image_urls:
    print(f"Attempting to download {url}")  # Debugging: Print URL before downloading
    image_name = url.split('/')[-1]
    image_path = os.path.join(output_dir, image_name)
    response = requests.get(url)
    if response.status_code == 200:
        with open(image_path, 'wb') as file:
            file.write(response.content)
        # Debugging: Confirm the image was saved
        print(f"Downloaded and saved {url} to {image_path}")
    else:
        print(f"Failed to download {url}, status code: {response.status_code}")


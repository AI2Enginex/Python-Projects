import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Class to handle directory creation
class MakeDirectory:
    def __init__(self, directory=None):
        # Directory to save downloaded images
        self.save_dir = directory
        # Create the directory if it doesn't exist
        os.makedirs(self.save_dir, exist_ok=True)

# Class to scrape images, inherits from MakeDirectory
class ScrapeImages(MakeDirectory):
    def __init__(self, dir_name=None, url=None):
        # Initialize the parent class with the directory name
        super().__init__(directory=dir_name)
        # Store the URL to scrape
        self.url = url

    # Function to download an image
    def download_image(self, image_url=None):
        try:
            # Send a GET request to the image URL
            response = requests.get(image_url)
            # Raise an error if the request failed
            response.raise_for_status()

            # Extract image file name from the URL
            image_name = os.path.basename(image_url)
            if not image_name:
                # If the URL ends with a slash or has no filename, generate a unique name
                image_name = f'image_{hash(image_url)}.jpg'

            # Create the full path to save the image
            image_path = os.path.join(self.save_dir, image_name)

            # Write the image data to the file
            with open(image_path, 'wb') as f:
                f.write(response.content)

            print(f"Downloaded {image_url} to {image_path}")

        except Exception as e:
            print(f"Failed to download {image_url}: {e}")

    # Function to scrape and save images
    def save_images(self, total=None):
        try:
            # Send a GET request to the webpage
            response = requests.get(self.url)
            # Raise an error if the request failed
            response.raise_for_status()

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all image tags
            img_tags = soup.find_all('img')

            # Extract and download images up to the specified total
            image_count = 0
            for img in img_tags:
                if image_count >= total:
                    break
                # Get the image URL from the src attribute
                img_url = img.get('src')
                if not img_url:
                    # Skip if the image tag doesn't have a src attribute
                    continue
                # Resolve relative URLs
                img_url = urljoin(self.url, img_url)
                # Download the image
                self.download_image(image_url=img_url)
                image_count += 1
        except Exception as e:
            # Return the exception if one occurs
            return e

# Main block to run the script
if __name__ == '__main__':
    # Create an instance of ScrapeImages with the specified directory and URL
    si = ScrapeImages(dir_name='images1', url='https://www.bkbirlacollegekalyan.com/')
    # Call save_images to scrape and save up to 10 images
    si.save_images(total=10)

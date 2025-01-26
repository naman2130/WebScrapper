import os
import json
import requests, uuid
from typing import List, Dict

class ScraperStorage:
    """Handles saving scraped data and images."""

    def __init__(self, output_file: str = "scraped_data.json", image_dir: str = "images"):
        self.output_file = output_file
        self.image_dir = image_dir
        os.makedirs(image_dir, exist_ok=True)
    
    def get_unique_filename(self) -> str:
        """Generates a unique filename."""
        return str(uuid.uuid4())  # Generates a unique filename using UUID

    def save_image(self, image_url: str) -> str:
        """Downloads image if it's not a data URL."""
        # Check if the URL is a data URL (e.g., data:image/svg+xml,...)
        if image_url.startswith('data:image/'):
            # Handle the data URL (you can skip, or save the image as an SVG or PNG, depending on format)
            file_extension = 'svg'  # Assuming it's SVG here, adjust based on actual format
            image_data = image_url.split(',')[1]  # Get the base64-encoded data after the comma
            image_path = f"images/{self.get_unique_filename()}.{file_extension}"
            with open(image_path, "wb") as f:
                f.write(bytes(image_data, 'utf-8'))  # Write the base64-encoded data as bytes
            return image_path
        
        # Otherwise, handle the normal image URL (e.g., from an external server)
        try:
            # Download the image using requests
            response = requests.get(image_url)
            response.raise_for_status()
            image_path = f"images/{self.get_unique_filename()}.jpg"  # Save as .jpg, adjust as needed
            with open(image_path, 'wb') as f:
                f.write(response.content)
            return image_path
        except requests.exceptions.RequestException as e:
            print(f"Failed to download image from {image_url}: {e}")
            return None

    def save_to_file(self, data: List[Dict]):
        """Saves the scraped product data to a JSON file."""
        with open(self.output_file, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Saved {len(data)} products to {self.output_file}")

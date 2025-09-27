import requests
import os
from urllib.parse import urlparse
import hashlib

def sanitize_filename(url):
    """
    Extracting a filename from the URL or generate a unique one if missing.
    """
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename:  # If URL ends with /
        # Use a hash to avoid collisions
        filename = hashlib.md5(url.encode()).hexdigest() + ".jpg"
    return filename

def fetch_image(url, folder="Fetched_Images"):
    """
    Download an image from a given URL into the specified folder.
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(folder, exist_ok=True)

        # Fetch the image
        headers = {"User-Agent": "UbuntuFetcher/1.0"}  # Respectful request
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()

        # Basic header check (safety)
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"✗ Skipped (not an image): {url}")
            return None

        # Create filename
        filename = sanitize_filename(url)
        filepath = os.path.join(folder, filename)

        # Prevent duplicate downloads
        if os.path.exists(filepath):
            print(f"⚠ Duplicate skipped: {filename}")
            return filepath

        # Save the image
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
        return filepath

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for {url}: {e}")
    except Exception as e:
        print(f"✗ An error occurred for {url}: {e}")
    return None

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    urls = input("Please enter one or more image URLs (comma separated): ").split(",")
    urls = [u.strip() for u in urls if u.strip()]  # Clean whitespace

    if not urls:
        print("No URLs provided. Exiting.")
        return

    for url in urls:
        fetch_image(url)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()

import os
import json
import re

from reddit_scraper.scraper import get_user_data
from save_data import save_user_data
from persona_extractor.persona_builder import extract_persona, save_persona


def extract_username_from_url(url):
    """Extracts Reddit username from profile URL."""
    pattern = r"reddit\.com\/user\/([A-Za-z0-9_-]+)\/?$"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        print("[ERROR] Invalid Reddit profile URL.")
        return None


def main():
    """Main function to scrape Reddit data, extract persona, and save both."""
    url = input("Enter Reddit Profile URL: ").strip()
    username = extract_username_from_url(url)
    if not username:
        return

    print(f"[INFO] Scraping and saving data for user: {username}")
    save_user_data(username)

    input_file = f"sample_data/{username}_data.json"
    if not os.path.exists(input_file):
        print(f"[ERROR] Could not find saved data at {input_file}")
        return

    with open(input_file, "r") as f:
        data = json.load(f)

    print(f"[INFO] Extracting persona for user: {username}")
    persona = extract_persona(data, username)
    if not persona:
        print("[ERROR] Persona extraction failed.")
        return

    save_persona(persona, username)

    print(f"[SUCCESS] Complete persona build for user '{username}'.")
    print(f" - Raw Data saved in 'sample_data/{username}_data.json'")
    print(f" - Persona saved in 'output/{username}_persona.txt'")


if __name__ == "__main__":
    main()

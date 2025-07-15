import json
import os
from main import extract_username_from_url
from save_data import save_user_data
from persona_extractor.persona_builder import extract_persona, save_persona

# --------- List of test URLs ---------
test_urls = [
    "https://www.reddit.com/user/kojied/",
    "https://www.reddit.com/user/Hungry-Move-6603/",
    "https://www.reddit.com/user/Nater5000/",
    "https://www.reddit.com/user/Nater5000/"

]

# --------- Test Loop ---------
for url in test_urls:
    print(f"\n===== Testing URL: {url} =====")
    username = extract_username_from_url(url)

    if not username:
        print("[SKIPPED] Invalid URL format.")
        continue

    print(f"[INFO] Extracted username: {username}")
    print(f"[INFO] Scraping and saving data...")
    save_user_data(username)

    input_file = f"sample_data/{username}_data.json"
    if not os.path.exists(input_file):
        print(f"[ERROR] Data file {input_file} not found. Skipping...")
        continue

    with open(input_file, "r") as f:
        data = json.load(f)

    print(f"[INFO] Extracting persona...")
    persona = extract_persona(data, username)
    if not persona:
        print(f"[ERROR] Persona extraction failed for {username}")
        continue

    save_persona(persona, username)
    print(f"[SUCCESS] Persona saved for {username} ✅")

print("\n===== Test run complete =====")

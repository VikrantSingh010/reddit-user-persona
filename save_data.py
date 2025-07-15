import os
import json

from reddit_scraper.scraper import get_user_data


def save_user_data(username, output_dir="sample_data"):
    """Fetch and save Reddit user data to a JSON file."""
    data = get_user_data(username)
    if not data:
        print(f"[ERROR] No data fetched for user '{username}'.")
        return

    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{username}_data.json")

    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[SUCCESS] Data saved to {output_file}")


# if __name__ == "__main__":
#     USERNAME = "kojied"  # Change this as needed
#     save_user_data(USERNAME)

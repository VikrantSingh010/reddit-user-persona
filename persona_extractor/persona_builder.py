import json
import os
import re

from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_json_from_response(content):
    """Extract JSON from Groq response, with fallback to braces matching."""
    match = re.search(r"```(?:json)?\n(.*?)\n```", content, re.DOTALL)
    if match:
        print("[INFO] Found JSON code block.")
        return match.group(1).strip()

    print("[WARNING] No JSON code block found. Trying to extract JSON object.")
    braces = 0
    json_start = None
    for i, c in enumerate(content):
        if c == '{':
            if braces == 0:
                json_start = i
            braces += 1
        elif c == '}':
            braces -= 1
            if braces == 0 and json_start is not None:
                return content[json_start:i+1].strip()
    print("[ERROR] No valid JSON object found in response.")
    return None


def extract_persona(data, username):
    """Extract user persona from Reddit data using Groq API."""
    sample_data = []

    for post in data.get("posts", [])[:10]:
        entry = (
            f"[POST] Title: {post.get('title', '')}\n"
            f"Content: {post.get('selftext', '')}\n"
            f"URL: {post.get('permalink', '')}"
        )
        sample_data.append(entry)

    for comment in data.get("comments", [])[:10]:
        entry = (
            f"[COMMENT] Body: {comment.get('body', '')}\n"
            f"Subreddit: {comment.get('subreddit', '')}\n"
            f"URL: {comment.get('permalink', '')}"
        )
        sample_data.append(entry)

    prompt = (
        "You are a professional personality profiler.\n"
        "Analyze the following Reddit posts and comments from a single user.\n\n"
        "Your task is to create a detailed user persona summary including:\n"
        "- Interests\n"
        "- Motivations\n"
        "- Personality Traits\n"
        "- Behaviour and Habits\n"
        "- Frustrations\n"
        "- Writing Style\n"
        "- Common Topics\n\n"
        "For each category, provide:\n"
        "- A summarized insight\n"
        "- At least one direct quote or excerpt that supports this insight\n"
        "- The exact Reddit permalink of the post or comment where this quote was found\n\n"
        "Your output must strictly follow this JSON structure:\n"
        "{\n"
        "  \"Interests\": [ { \"topic\": \"...\", \"evidence\": [ { \"quote\": \"...\", \"source\": \"...\" } ] } ],\n"
        "  \"Motivations\": [ { \"motivation\": \"...\", \"evidence\": [ { \"quote\": \"...\", \"source\": \"...\" } ] } ],\n"
        "  \"Personality_Traits\": [ { \"trait\": \"...\", \"evidence\": [ { \"quote\": \"...\", \"source\": \"...\" } ] } ],\n"
        "  \"Behaviour_and_Habits\": [ { \"behavior\": \"...\", \"evidence\": [ { \"quote\": \"...\", \"source\": \"...\" } ] } ],\n"
        "  \"Frustrations\": [ { \"frustration\": \"...\", \"evidence\": [ { \"quote\": \"...\", \"source\": \"...\" } ] } ],\n"
        "  \"Writing_Style\": [ { \"style\": \"...\", \"evidence\": [ { \"quote\": \"...\", \"source\": \"...\" } ] } ],\n"
        "  \"Common_Topics\": [ { \"topic\": \"...\", \"evidence\": [ { \"quote\": \"...\", \"source\": \"...\" } ] } ]\n"
        "}\n\n"
        "Respond in valid JSON format only.\n\n"
        f"User Data:\n{chr(10).join(sample_data)}"
    )

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    content = response.choices[0].message.content

    json_text = extract_json_from_response(content)
    if json_text:
        try:
            persona = json.loads(json_text)
            return persona
        except Exception as e:
            print(f"[ERROR] Failed to parse JSON: {e}\nRaw JSON:\n{json_text}")
            return None
    else:
        return None


def save_persona(persona, username, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{username}_persona.txt")
    with open(file_path, "w") as f:
        json.dump(persona, f, indent=4)
    print(f"[SUCCESS] Persona saved to {file_path}")


# if __name__ == "__main__":
#     USERNAME = "kojied"
#     input_file = f"sample_data/{USERNAME}_data.json"
#     if not os.path.exists(input_file):
#         print(f"[ERROR] Data file {input_file} does not exist. Run save_data.py first.")
#     else:
#         with open(input_file, "r") as f:
#             user_data = json.load(f)

#         extracted_persona = extract_persona(user_data, USERNAME)
#         if extracted_persona:
#             save_persona(extracted_persona, USERNAME)

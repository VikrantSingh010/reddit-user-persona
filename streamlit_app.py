import streamlit as st
import json
import os
import re

from save_data import save_user_data
from persona_extractor.persona_builder import extract_persona


def extract_username_from_url(url):
    """Extracts Reddit username from profile URL."""
    pattern = r"reddit\.com\/user\/([A-Za-z0-9_-]+)\/?$"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None


st.title("🧑‍💻 Reddit User Persona Extractor")

profile_url = st.text_input("Enter Reddit Profile URL (e.g. https://www.reddit.com/user/kojied/)")

if profile_url:
    username = extract_username_from_url(profile_url)

    if username:
        if st.button("Build Persona"):
            with st.spinner(f"Fetching data for '{username}'..."):
                save_user_data(username)

                input_file = f"sample_data/{username}_data.json"
                if not os.path.exists(input_file):
                    st.error(f"❌ Could not find saved data at {input_file}.")
                else:
                    with open(input_file, "r") as f:
                        data = json.load(f)

                    st.info("Extracting persona...")
                    persona = extract_persona(data, username)

                    if not persona:
                        st.error("❌ Persona extraction failed.")
                    else:
                        st.success("✅ Persona extraction complete!")
                        st.subheader("📄 Extracted Persona (JSON)")
                        st.json(persona)
    else:
        st.error("❌ Invalid Reddit Profile URL.")

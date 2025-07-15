# 🧑‍💻 Reddit User Persona Extractor

A Python tool that scrapes a Reddit user's posts and comments, analyzes them using LLMs, and builds a structured **User Persona** with direct evidence.

---

## 🚀 Features
- ✅ Scrapes Reddit posts and comments of any user
- ✅ Extracts key persona insights:
  - Interests
  - Motivations
  - Personality Traits
  - Behaviour and Habits
  - Frustrations
  - Writing Style
  - Common Topics
- ✅ Provides quotes and Reddit links as evidence
- ✅ Outputs persona in structured JSON/text
- ✅ CLI & Streamlit App interface

---

## 🛠️ Tech Stack

- Python 3.10+
- [`praw`](https://praw.readthedocs.io/) — Reddit API wrapper
- [`groq`](https://console.groq.com/) — LLM API
- [`python-dotenv`](https://pypi.org/project/python-dotenv/) — for environment variables
- [`streamlit`](https://streamlit.io/) — simple web interface

---

## 📂 Project Structure

```
reddit-user-persona/
├── reddit_scraper/
│   └── scraper.py
├── persona_extractor/
│   └── persona_builder.py
├── sample_data/
├── output/
├── main.py             # CLI Entry Point
├── streamlit_app.py    # Streamlit App Interface
├── save_data.py                   
├── test.py             # Sample Test Script
├── README.md
├── requirements.txt
```

---

## ⚡ Setup Instructions

1️⃣ **Clone the Repository**

```bash
git clone https://github.com/VikrantSingh010/reddit-user-persona.git
cd reddit-user-persona
```

2️⃣ **Install Dependencies**

```bash
pip install -r requirements.txt
```

3️⃣ **Set Up Environment Variables**

Create a `.env` file in the root directory with:
```
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=  
REDDIT_USER_AGENT=
GROQ_API_KEY=

```

---

## 🖥️ Usage

### CLI Mode

```bash
python main.py
```
- Enter the Reddit profile URL when prompted  
- Example: `https://www.reddit.com/user/kojied/`  

---

### Streamlit App

```bash
streamlit run app.py
```
- Use the web interface to enter Reddit URL and view persona output

---

## 📝 Example Output

```
[SUCCESS] Complete persona build for user 'kojied'.
 - Raw Data saved in 'sample_data/kojied_data.json'
 - Persona saved in 'output/kojied_persona.txt'
```

---


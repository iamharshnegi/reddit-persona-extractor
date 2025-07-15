# persona_generator.py
import json
import os
from collections import Counter
import re

def clean_text(text):
    return re.sub(r'[^\w\s]', '', text.lower())

def extract_keywords(data):
    all_text = " ".join(item.get("text", "") for item in data)
    words = clean_text(all_text).split()
    stopwords = {"the", "and", "to", "a", "of", "in", "is", "it", "that", "on", "for", "with", "this", "i", "you", "my"}
    filtered_words = [w for w in words if w not in stopwords and len(w) > 3]
    return Counter(filtered_words).most_common(10)

def detect_tone(text):
    if "?" in text:
        return "curious"
    elif "!" in text:
        return "expressive"
    elif any(w in text.lower() for w in ["sorry", "please", "thank"]):
        return "polite"
    return "neutral"

def generate_persona(username):
    filepath = f"data/{username}_data.json"
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    posts = data.get("posts", [])
    comments = data.get("comments", [])

    all_data = posts + comments
    keywords = extract_keywords(all_data)

    tone_counter = Counter(detect_tone(item.get("text", "")) for item in all_data)

    # Basic rule-based persona
    persona = f"""
User Persona: {username}
-------------------------
Interests (Top Keywords):
{', '.join([kw[0] for kw in keywords])}

Dominant Tone:
{tone_counter.most_common(1)[0][0].capitalize()}

Sample Citations:
"""

    for kw, _ in keywords[:3]:
        for item in all_data:
            if kw in clean_text(item.get("text", "")):
                persona += f"- '{kw}' found in: {item.get('link')}\n"
                break

    os.makedirs("output", exist_ok=True)
    with open(f"output/persona_{username}.txt", "w", encoding="utf-8") as f:
        f.write(persona.strip())

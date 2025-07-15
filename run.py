# run.py
from reddit_scraper_bs import fetch_reddit_data, save_user_data
from persona_generator import generate_persona
import sys
import re

def extract_username(profile_url):
    match = re.search(r"reddit\.com/user/([^/]+)/?", profile_url)
    if match:
        return match.group(1)
    else:
        print("Invalid Reddit profile URL.")
        sys.exit(1)

def process_user(username):
    posts = fetch_reddit_data(username, "submitted", 30)
    comments = fetch_reddit_data(username, "comments", 30)
    save_user_data(username, posts, comments)
    generate_persona(username)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run.py <reddit_profile_url>")
        print("Example: python run.py https://www.reddit.com/user/kojied/")
        sys.exit(1)

    profile_url = sys.argv[1]
    username = extract_username(profile_url)
    print(f"Processing user: {username}")
    process_user(username)

import os

import praw
from dotenv import load_dotenv

load_dotenv()


def get_reddit_instance():
    """Create and return a Reddit API instance using environment variables."""
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
    )


def get_user_data(username, post_limit=50, comment_limit=50):
    """Fetch user submissions and comments from Reddit."""
    reddit = get_reddit_instance()

    try:
        redditor = reddit.redditor(username)
        _ = redditor.id  # Trigger fetch to check if user exists
    except Exception as e:
        print(f"[ERROR] Could not fetch user '{username}': {e}")
        return None

    posts = []
    try:
        for submission in redditor.submissions.new(limit=post_limit):
            posts.append({
                "id": submission.id,
                "title": submission.title,
                "selftext": submission.selftext.strip() if submission.selftext else "",
                "subreddit": submission.subreddit.display_name,
                "created_utc": submission.created_utc,
                "permalink": f"https://reddit.com{submission.permalink}",
                "score": submission.score,
                "url": submission.url,
            })
    except Exception as e:
        print(f"[ERROR] Error fetching posts: {e}")

    comments = []
    try:
        for comment in redditor.comments.new(limit=comment_limit):
            comments.append({
                "id": comment.id,
                "body": comment.body.strip() if comment.body else "",
                "subreddit": comment.subreddit.display_name,
                "created_utc": comment.created_utc,
                "permalink": f"https://reddit.com{comment.permalink}",
                "score": comment.score,
                "parent_id": comment.parent_id,
            })
    except Exception as e:
        print(f"[ERROR] Error fetching comments: {e}")

    return {"posts": posts, "comments": comments}

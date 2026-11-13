import os
import time
import requests

CLIENT_ID = os.environ["REDDIT_CLIENT_ID"]
CLIENT_SECRET = os.environ["REDDIT_CLIENT_SECRET"]
USERNAME = os.environ.get("REDDIT_USERNAME", "i0j0")
PASSWORD = os.environ["REDDIT_PASSWORD"]
USER_AGENT = f"linux:reddit-unanswered-notifier:v1.0 (by /u/{USERNAME})"

SUBREDDITS = "SaaS+startups+googlecloud+devops+mcp+AI_Agents+LocalLLaMA+mlops+CustomsBroker+supplychain+logistics+commercialrealestate+RealEstateTechnology+sustainability"
POLL_INTERVAL_SECONDS = 900  # 15 minutes (< 10 requests/hour)
SEEN_POST_IDS = set()


def get_oauth_token() -> str:
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    data = {"grant_type": "password", "username": USERNAME, "password": PASSWORD}
    resp = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth,
        data=data,
        headers={"User-Agent": USER_AGENT},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def check_unanswered_threads(token: str) -> None:
    headers = {"Authorization": f"bearer {token}", "User-Agent": USER_AGENT}
    url = f"https://oauth.reddit.com/r/{SUBREDDITS}/new?limit=25"
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()

    for item in resp.json().get("data", {}).get("children", []):
        post = item["data"]
        post_id = post["id"]
        if post_id in SEEN_POST_IDS:
            continue
        SEEN_POST_IDS.add(post_id)

        if post.get("num_comments", 0) == 0 and not post.get("locked"):
            print(f"[UNANSWERED] r/{post['subreddit']}: {post['title']} -> https://www.reddit.com{post['permalink']}")


if __name__ == "__main__":
    bearer_token = get_oauth_token()
    while True:
        check_unanswered_threads(bearer_token)
        time.sleep(POLL_INTERVAL_SECONDS)

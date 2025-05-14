import requests
import pandas as pd
from datetime import date
import pandas as pd
import praw
import os
from dotenv import load_dotenv



def get_url(reddit, subreddit_name: str, fetch_hot: bool=True, fetch_new: bool =True, 
            fetch_top: bool = True, fetch_rising: bool = True, fetch_controversial: bool = True,
            maximum_post: int = 100) -> list:
    '''
    subreddit: name of subreddit. For example: Python
    categories: List of categories to fetch posts from. For example: ['hot', 'new', 'top', 'rising', 'controversial']
    maximum_post: maximum number of posts to fetch. -1 for all posts. minimum is 100
    '''
    subreddit = reddit.subreddit(subreddit_name)
    posts = []

    if fetch_hot:
        hot_posts = subreddit.hot(limit=maximum_post)
        posts.extend(hot_posts)
    if fetch_new:
        new_posts = subreddit.new(limit=maximum_post)
        posts.extend(new_posts)
    if fetch_top:
        top_posts = subreddit.top(limit=maximum_post)
        posts.extend(top_posts)
    if fetch_rising:
        rising_posts = subreddit.rising(limit=maximum_post)
        posts.extend(rising_posts)
    if fetch_controversial:
        controversial_posts = subreddit.controversial(limit=maximum_post)
        posts.extend(controversial_posts)

    posts_url = []
    for post in posts:
        posts_url.append(post.url)
    return posts_url

def fetch_post(reddit, url: str = "https://www.reddit.com/r/learnpython/comments/1234567/how_to_learn_python/") -> dict:
    '''
    url: url of the reddit post. For example: https://www.reddit.com/r/learnpython/comments/1234567/how_to_learn_python/
    '''
    if not url.startswith("https://www.reddit.com"):
        return {
            'title': None,
            'url': None,
            'flair': None,
            'author': None,
            'selftext': None,
        }
        
    submission = reddit.submission(url=url)
    post_data = {
        'title': submission.title,
        'url': submission.url,
        "flair": submission.link_flair_text,
        'author': str(submission.author),
        # 'created_utc': submission.created_utc,
        # 'num_comments': submission.num_comments,
        # 'score': submission.score,
        'selftext': submission.selftext,
    }
    return post_data



def main():
    # load environment variables from .env file
    load_dotenv()   
    # Initialize Reddit instance
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
    )
    subreddits = ['creepypasta', 'nosleep', 'Creepypastastories', 'Horror_stories', 'RedditHorrorStories']

    today = str(date.today()).replace('-', '_')

    for subreddit in subreddits:
        print(f"Fetching posts from subreddit: {subreddit}")
        urls = get_url(reddit, subreddit, fetch_hot=True, fetch_new=True, maximum_post=100)

        post_dicts = []
        for url in urls:
            post_data = fetch_post(reddit, url)
            print(f"\t-Fetched post: {post_data['title']}")
            post_dicts.append(post_data)

        posts_df = pd.DataFrame(post_dicts)
        posts_df.drop_duplicates(subset=['title'], inplace=True)  # Drop duplicates
        posts_df.T.to_json(f'./dataset/reddit/data_from_subreddit/{subreddit}_{today}.json')
        
        print("===================================================================================\n")
    

# import os

# current_directory = os.getcwd()
# print("Thư mục hiện tại là:", current_directory)

# path = './dataset/reddit/data_from_subreddit'
# if os.path.exists(path):
#     print("Path tồn tại")
# else:
#     print("Path không tồn tại")
if __name__ == "__main__":
    main()

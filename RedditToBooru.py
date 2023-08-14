import os.path
import urllib.request
import csv
import praw
from praw import models

# USER VARIABLES
BASE_LOCATION = "E:/Documents/Uni Work/Computer Programming/Personal/BooruSort/TestStart/Hu/"  # Directory to save images
ENABLE_WHITELIST_PROMPT = False  # Set to False to disable the whitelist prompt at the end
DO_UNSAVE = False  # Decide if you want to unsave the post after downloading


def create_reddit() -> praw.Reddit:
    """
    Create and return a Reddit instance for PRAW.
    """
    reddit = praw.Reddit(site_name="DEFAULT")
    return reddit


def load_whitelisted_subreddits(filename: str) -> set:
    """
    Load the whitelisted subreddits from the given file.

    :param filename: Name of the file containing the whitelisted subreddits.
    :return: A set containing the whitelisted subreddits.
    """
    with open(filename, 'r') as f:
        # Read each line, strip whitespace and convert to lowercase
        return set(line.strip().lower() for line in f)


def main():
    """
    Main function to retrieve and download images from saved Reddit posts.
    """
    reddit = create_reddit()
    # Get the saved items
    saved = reddit.user.me().saved(limit=None)
    total_count = len(list(saved))
    saved = reddit.user.me().saved(limit=None)
    i = 0
    whitelisted_subreddits = load_whitelisted_subreddits('whitelist.txt')
    non_whitelisted_subreddits = set()

    # Loop through the saved items
    for item in saved:
        i += 1
        print("Checking", i, "of", total_count)

        # If the item is a post (Submission), print the subreddit's display name
        if isinstance(item, praw.models.Submission):
            if item.subreddit.display_name.lower() not in whitelisted_subreddits:
                non_whitelisted_subreddits.add(item.subreddit.display_name)
            else:
                if "i.redd.it" in item.url or "imgur.com" in item.url:
                    download(item)
                if "gallery" in item.url:
                    gallery_dl(item)
                if DO_UNSAVE:
                    unsave(item)
        # If the item is a comment, print the body of the comment
        elif isinstance(item, praw.models.Comment):
            print(f"Comment: {item.body}")

    if ENABLE_WHITELIST_PROMPT and non_whitelisted_subreddits:
        process_non_whitelisted_subreddits(non_whitelisted_subreddits)


def download(post: praw.models.Submission):
    """
    Download an image post from Reddit.

    :param post: The Reddit post to download.
    """
    ext = os.path.splitext(post.url)[1]
    file_name = post.id + ext
    print("ext:", ext)
    print("filename:", file_name)
    print(post.url)
    print("Downloading", post.title, ":", file_name)
    print("To", BASE_LOCATION)
    urllib.request.urlretrieve(post.url, BASE_LOCATION + file_name)
    store_link_info(post)
    print("Unsaving", post.title)


def gallery_dl(post: praw.models.Submission):
    """
    Download images from a Reddit gallery post.

    :param post: The Reddit post to download from.
    """
    for n in post.media_metadata.items():
        url = n[1]['p'][0]['u']
        url = url.split("?")[0].replace("preview", "i")
        file_name = url.rsplit("/", 1)[1]
        print("Downloading", post.title, ":", file_name)
        print("To", BASE_LOCATION)
        urllib.request.urlretrieve(url, BASE_LOCATION + file_name)
        store_link_info(post)
    print("Unsaving", post.title)


def store_link_info(post: praw.models.Submission):
    """
    Store the Reddit post link information to a CSV file.

    :param post: The Reddit post whose info needs to be stored.
    """
    with open('E:/Documents/Uni Work/Computer Programming/Personal/redditRewrite/reddit_links.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        author = post.author.name if post.author else "Deleted"
        comment_section_url = 'https://www.reddit.com' + post.permalink
        writer.writerow([post.id, comment_section_url, post.title, str(post.subreddit), author])


def unsave(post: praw.models.Submission):
    """
    Unsave a Reddit post.

    :param post: The Reddit post to unsave.
    """
    post.unsave()
    pass


def process_non_whitelisted_subreddits(subreddits: set):
    """
    Process subreddits that are not in the whitelist by prompting the user to add them.

    :param subreddits: A set of subreddits that are not whitelisted.
    """
    print("\nSubreddits not in the whitelist:")
    for subreddit in sorted(subreddits):
        choice = input(f"Do you want to whitelist subreddit '{subreddit}'? (y/n): ").strip().lower()
        if choice == 'y':
            add_to_whitelist(subreddit)
            print(f"'{subreddit}' added to the whitelist.")


def add_to_whitelist(subreddit: str):
    """
    Add a subreddit to the whitelist file.

    :param subreddit: The subreddit name to add to the whitelist.
    """
    with open('whitelist.txt', 'a') as f:
        f.write(f"\n{subreddit.lower()}")


def test():
    """
    Test function to print details of saved Reddit items.
    """
    reddit = create_reddit()
    # Get the saved items
    saved = reddit.user.me().saved(limit=None)

    all_saved_items = []
    for item in saved:
        all_saved_items.append(vars(item))

    print(all_saved_items)


main()

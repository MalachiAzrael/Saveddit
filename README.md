
# RedditToBooru

RedditToBooru is a Python script that retrieves and downloads images from saved Reddit posts. It makes use of the PRAW (Python Reddit API Wrapper) library to interact with Reddit. The script is designed to fetch images only from whitelisted subreddits, which can be specified in a separate file.

This project was undertaken as a personal learning experience to understand the use of git, Python, and the PRAW library.

## Features

- Retrieve images from saved Reddit posts.
- Whitelist specific subreddits to fetch images from.
- User-defined customization like specifying the save directory, enabling whitelist prompts, and deciding whether to unsave the post after downloading.

## Requirements

- Python 3.x
- PRAW library (install via `pip install praw`)

## Usage

1. Set up your `praw.ini` file with your Reddit app credentials (see PRAW documentation for details).
2. Customize the user variables in the script:
   - `BASE_LOCATION`: Directory to save images.
   - `ENABLE_WHITELIST_PROMPT`: Set to False to disable the whitelist prompt at the end.
   - `DO_UNSAVE`: Decide if you want to unsave the post after downloading.
3. Create a `whitelist.txt` file in the same directory as the script, listing the subreddits you want to whitelist (one subreddit per line).
4. Run the script: `python RedditToBooru.py`.

## License

This project is open source and available under the [GPL-3.0 License](LICENSE).

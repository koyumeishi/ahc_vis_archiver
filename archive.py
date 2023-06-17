"""
This module provides functionality to download the AtCoder AHC (AtCoder Heuristic Contest) visualizer and its related files. It utilizes the selenium chromedriver for web scraping.

Usage:
1. Make sure you have the selenium chromedriver installed.
2. Run this module with the desired URL of the AHC visualizer as a command-line argument.

Example:
python archive.py https://img.atcoder.jp/ahc020/db611066.html

The module will fetch the visualizer's page using Selenium, extract the URLs of the required files, and save them to the current directory.

Main Function:
- main():
    The entry point of the module. Parses the command-line arguments, extracts the visualizer URL, and initiates the process of saving the visualizer and related files to the current directory.
"""


import argparse
import os
import json
from urllib.parse import urlparse

import requests

from selenium import webdriver
from selenium.webdriver.chrome import options


def save(urls: list[str]):
    """
    Fetche the contents of the URLs in the 'urls' list through an HTTP request and saves them to the specified path.
    Automatically creates the directory if it doesn't exist.
    """
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            parsed_url = urlparse(url)
            path = parsed_url.path

            # パスの先頭にスラッシュがある場合は除去する
            if path.startswith('/'):
                path = path[1:]

            # ファイルの保存先ディレクトリを作成
            dir_name = os.path.dirname(path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)

            file_name = os.path.basename(path)
            file_path = os.path.join(dir_name, file_name)

            with open(file_path, 'wb') as file:
                file.write(response.content)
                print(f"Saved {file_path} successfully.")
        else:
            print(f"Failed to retrieve {url}.")


def is_same_path(url0: str, url1: str) -> bool:
    """
    Return True if the file path and host of 'url0' and 'url1' are the same up to the file name.
    """
    parsed_url0 = urlparse(url0)
    parsed_url1 = urlparse(url1)
    path0 = os.path.dirname(parsed_url0.path)
    path1 = os.path.dirname(parsed_url1.path)
    netloc0 = parsed_url0.netloc
    netloc1 = parsed_url1.netloc
    return path0 == path1 and netloc0 == netloc1


def filter_urls(origin_url: str, urls: list[str]) -> list[str]:
    """
    is_same_path(origin_url, url in urls) == True のみをフィルタリングして返す.
    """
    return [url for url in urls if is_same_path(origin_url, url)]


def get_urls(url: str) -> list[str]:
    """
    Take a URL of a visualizer and retrieves the URLs of the files required for the visualizer.
    Opens the visualizer's page using Selenium and extracts only the URLs with the same path as the requested URL.
    """
    opt = options.Options()
    opt.add_argument('--headless')
    opt.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    with webdriver.Chrome(options=opt) as driver:
        driver.get(url)
        urls = []
        for log in driver.get_log("performance"):
            j = json.loads(log['message'])
            try:
                u = None
                if 'response' in j['message']['params']:
                    u = j['message']['params']['response']['url']
                elif 'request' in j['message']['params']:
                    u = j['message']['params']['request']['url']
                if u is not None:
                    urls += [u]
            except Exception:
                pass
        urls = list(set(urls))
        return urls


def main():
    """
    Download the AtCoder AHC visualizer and its related files from the specified URL to the current directory.
    Requires the selenium chromedriver to be installed.
    """
    parser = argparse.ArgumentParser(
        description="Save the AtCoder AHC visualizer and related files to the current directory. Make sure to have the selenium chromedriver installed.")
    parser.add_argument(
        "url", help="URL of the AHC visualizer. Example: https://img.atcoder.jp/ahc020/db611066.html")

    args = parser.parse_args()

    # Extract the URL from the command-line arguments
    vis_url = args.url

    # Your code to save the visualizer and related files to the current directory goes here
    # Make sure to check if the selenium chromedriver is installed

    # Example code for demonstration purposes
    print("Saving AHC visualizer and related files...")
    print("Visualizer URL:", vis_url)

    urls = get_urls(vis_url)
    urls = filter_urls(vis_url, urls)
    print(urls)
    save(urls)


if __name__ == "__main__":
    main()

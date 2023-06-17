"""
This module provides functionality to retrieve the URL of the AtCoder AHC (AtCoder Heuristic Contest) visualizer page for a given AHC ID. It uses web scraping techniques to extract the URL from the contest document page.

Usage:
1. Run this module with the desired AHC ID as a command-line argument.

Example:
python ahc_visualizer_url.py ahc010

The module will retrieve the URL of the AHC visualizer page associated with the provided AHC ID.

Dependencies:
- requests

Functions:
- get_visualizer_url(ahc_id: str) -> str:
    Retrieves the URL of the AHC visualizer page for the given AHC ID. It scrapes the contest document page, extracts the URL from the HTML, and returns it. Returns None if the URL cannot be found.

Main Function:
- main():
    The entry point of the module. Parses the command-line arguments, retrieves the AHC ID, and retrieves the URL of the AHC visualizer page using the 'get_visualizer_url' function. Prints the URL to the console.

Note:
Make sure to have the necessary dependencies installed before running the module.
"""

from lxml.etree import HTML
import re
import requests
import argparse


def get_visualizer_url(ahc_id: str):
    document_url = f"https://atcoder.jp/contests/{ahc_id}/tasks/{ahc_id}_a"

    response = requests.get(document_url)
    if response.status_code != 200:
        return None

    html = response.text
    tree = HTML(html)
    links = tree.xpath("//a/@href")

    regex = re.compile(r"https://img.atcoder.jp/ahc\d{3}/[^?]+\.html")
    target_url = None

    for link in links:
        m = regex.search(link)
        if m is not None:
            target_url = m[0]
            break
    return target_url


def main():
    parser = argparse.ArgumentParser(
        description='Retrieve the URL of the AHC visualizer page')
    parser.add_argument('ahc_id', type=str,
                        help='ID of the AHC (e.g., "ahc010", "ach001")')
    args = parser.parse_args()

    ahc_id = args.ahc_id
    url = get_visualizer_url(ahc_id)
    print(url)


if __name__ == '__main__':
    main()

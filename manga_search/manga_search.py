from bs4 import BeautifulSoup as bs
import requests
import os
import json
from manga_search.download import handle_download
from util.colors import ESC, YELLOW
from util.parse_json import parse_json
from util.print_log import error, info
from kcc.kindlecomicconverter.comic2ebook import main as c2e
import re


try:
    MANGA_URL = parse_json("data/config.json")["source_url"]
except KeyError:
    error(f"No {YELLOW}source_url{ESC} found in {YELLOW}config.json{ESC}")
    exit()


def check_all():
    with open("data/manga.json", "r") as f:
        all_mangas = json.load(f)
    for m in all_mangas.keys():
        download_links = search_manga(m, all_mangas[m])  
        handle_download(download_links, m)  # downloads the manga
        c2e(["--profile=KPW", f"--title={m}", "--format=MOBI", f"downloads/{m}/"])  # turns the manga into a mobi file


def search_manga(name: str, manga_settings={}):
    joined_url = os.path.join(MANGA_URL, name)
    website = requests.get(joined_url)
    soup = bs(website.content, "html.parser")
    chapters = soup.find_all("tr")

    # if the link is invalid, we are redirected to the front page
    # where there are no tables
    if len(chapters) == 0:
        error(f"No chapters found on {MANGA_URL}{YELLOW}{name}{ESC}")
        return False
    
    # episodes below the value are simply ignored for downloading
    ignore_below = float("-inf")
    ignore_above = float("inf")
    if "ignore_episodes_below" in manga_settings.keys() and manga_settings["ignore_episodes_below"] != -1:
        ignore_below = manga_settings["ignore_episodes_below"]
    if "ignore_episodes_above" in manga_settings.keys() and manga_settings["ignore_episodes_above"] != -1:
        ignore_above = manga_settings["ignore_episodes_above"]
        
    
    download_links = []
    for i, tr in enumerate(chapters):
        # gets the chapter number of the link
        try:
            chap_num = int(re.search(r"Chapter (\d+)", tr.td.a.text).groups()[0])
        except (ValueError, IndexError, AttributeError):
            error(f"There was a problem fetching table row {YELLOW}{i}{ESC}")
            continue
        
        if chap_num < ignore_below or chap_num > ignore_above:
            continue
        
        # gets the download link to the chapter
        download_url = tr.find("a", download=True)
        if download_url is None:
            info(f"Row {i} | Chapter {chap_num} had no download link, so it was skipped")
            continue
        download_url = download_url["href"]
        download_links.append((chap_num, download_url))

    info(f"Found {len(download_links)} chapters to download for {YELLOW}{name}{ESC}")
    return download_links
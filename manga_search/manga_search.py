import shutil
from bs4 import BeautifulSoup as bs
import requests
import os
import json
from manga_search.download import handle_download
from manga_search.email import send_mail
from util.colors import ESC, YELLOW
from util.parse_json import fetch_json, parse_json
from util.print_log import error, info
from kcc.kindlecomicconverter.comic2ebook import main as c2e
import re
import json


MANGA_URL = fetch_json()["source_url"]
BOOK_FORMAT = parse_json("data/config.json")["book_format"]
_already_added_fp = "data/added_manga.json"
ALREADY_ADDED = parse_json(_already_added_fp)
CLEANUP = True  # if successfully sent files should be deleted again


def check_all():
    with open("data/manga.json", "r") as f:
        all_mangas = json.load(f)
    for m in all_mangas.keys():
        # fetches the correct download links for the chapters
        download_links = search_manga(m, all_mangas[m])

        # makes sure to not download the same chapters again
        chapters_to_ignore = ALREADY_ADDED.setdefault(m, [])
        download_links = [
            (chap, durl) for chap, durl in download_links if chap not in chapters_to_ignore]
        if len(download_links) == 0:
            info(f"There are no new chapters to download for {m}")
            continue
        fetched_chapters = [chap for chap, durl in download_links]

        # downloads all the animes
        handle_download(download_links, m)  # downloads the manga

        # converts the downloaded images to MOBI
        root = os.path.join("downloads", m)
        for f in os.listdir(root):
            path = os.path.join(root, f)
            if not os.path.isdir(path):
                continue
            info(f"Converting {YELLOW}{path}{ESC}")
            # turns the manga into a mobi file
            c2e(["--profile=KPW", f"--format={BOOK_FORMAT}", path])

        # sends the mobi files per email
        files_to_cleanup = []
        for f in os.listdir(root):
            path = os.path.join(root, f)
            if not os.path.isfile(path):
                continue
            filename = os.path.basename(f)
            name, ext = os.path.splitext(filename)
            if ext.replace(".", "").lower() == BOOK_FORMAT.lower():
                suc = send_mail(path)
                if suc:
                    files_to_cleanup.append(path)

        if CLEANUP:
            for path in files_to_cleanup:
                try:
                    filename = os.path.basename(path)
                    name, ext = os.path.splitext(filename)
                    os.remove(path)  # removes the file
                    shutil.rmtree(path.replace(ext, ""))  # removes the dir
                    info(f"Cleaned up the files for {YELLOW}{filename}{ESC}")
                except FileNotFoundError:
                    error(
                        f"File with path {YELLOW}{path}{ESC} was not found to delete")

        ALREADY_ADDED[m] += fetched_chapters
        with open(_already_added_fp, "w") as f:
            json.dump(ALREADY_ADDED, f, indent=2)


def search_manga(name: str, manga_settings={}) -> list[tuple[int, str]]:
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
            chap_num = int(re.search(r"Chapter (\d+)",
                           tr.td.a.text).groups()[0])
        except (ValueError, IndexError, AttributeError):
            error(f"There was a problem fetching table row {YELLOW}{i}{ESC}")
            continue

        if chap_num < ignore_below or chap_num > ignore_above:
            continue

        # gets the download link to the chapter
        download_url = tr.find("a", download=True)
        if download_url is None:
            info(
                f"Row {i} | Chapter {chap_num} had no download link, so it was skipped")
            continue
        download_url = download_url["href"]
        download_links.append((chap_num, download_url))

    info(
        f"Found {len(download_links)} chapters to download for {YELLOW}{name}{ESC}")

    return download_links

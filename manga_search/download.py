from io import BytesIO
from typing import Tuple
import zipfile
import requests
from util.colors import ESC, RED, YELLOW
from util.print_log import info


def handle_download(download_links=[], name=""):
    downloaded_chaps = []
    for chap_num, d_url in download_links:
        info(f"Downloading chapter {chap_num}:\t", end="")
        filename = d_url.split("/")[-1]
        suc = download_file(d_url, filename, name)
        if suc:
            print(f" {YELLOW}DONE{ESC}")
            downloaded_chaps.append(chap_num)
        else:
            print(f" {RED}FAILED{ESC}")
    return downloaded_chaps


def download_file(url, filename, name) -> Tuple[bool, str]:
    # rety for 5 times incase there's an error
    for _ in range(5):
        try:
            req = requests.get(url, stream=True)
            z = zipfile.ZipFile(BytesIO(req.content))
            z.extractall(f"downloads/{name}/{filename}")
            break
        except zipfile.BadZipFile:
            pass
    else:
        return False
    return True

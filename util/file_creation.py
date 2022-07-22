import os
from util.colors import YELLOW, ESC
from util.print_log import info
import json


def check_files():
    created_file = False

    required_directories = ["data", "downloads"]
    for d in required_directories:
        if not os.path.isdir(d):
            os.mkdir(d)
            info(f"Created directory {YELLOW}{d}{ESC}")
            created_file = True

    if not os.path.isfile("data/config.json"):
        with open("data/config.json", "w") as f:
            j = {"kindle_email": [
                "tmp@mail.com"], "book_format": "MOBI", "notification_email": ["tmp@mail.com"]}
            json.dump(j, f, indent=4)
        info(f"Created {YELLOW}config.json{ESC}")
        created_file = True

    if not os.path.isfile("data/manga.json"):
        with open("data/manga.json", "w") as f:
            j = {"One_Piece": {"active": True,
                               "ignore_episodes_below": -1, "ignore_episodes_above": -1}}
            json.dump(j, f, indent=4)
        info(f"Created {YELLOW}manga.json{ESC}")
        created_file = True

    if not os.path.isfile("data/added_manga.json"):
        with open("data/added_manga.json", "w") as f:
            f.write("{}")
        info(f"Created {YELLOW}added_manga.json{ESC}")
        created_file = True

    if created_file:
        info("You need to update the created files and restart the script now.")

    return created_file

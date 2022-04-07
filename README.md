**This ReadMe is not finished yet**

# Auto Manga Kindle Updater

# Installing
1. Clone to your folder using `git clone --recurse-submodules git@github.com:markbeep/AutoMangaKindleUpdater.git` so that the requried submodules are also installed.
2. Install KindleGen (so that it can create to MOBI files)
  - Linux: [Download KindleGen here](https://archive.org/download/kindlegen2.9/kindlegen_linux_2.6_i386_v2_9.tar.gz) and follow [this guide](https://askubuntu.com/questions/790835/kindlegen-installation#823525) for more detail on how to install it.
  - Windows: Download KindleGen as explained [here](https://github.com/asciidoctor/asciidoctor-epub3/issues/363#issuecomment-684794354) and add `kindlegen` to your path or simply drop it in the root directory (where `main.py` is).
3. Install Pipenv
4. Call `pipenv install` to install the required packages
5. Enter the Python environment with `pipenv shell` and then run `main.py` (or `pipenv run python main.py`)
6. Add the login info to your throwaway GMail account into `data/login.json`
7. Update `manga.json` with the mangas you want downloaded and the amount that should be downloaded
8. Update `config.json` with the email address of your Kindle
9. Run `main.py` again and watch the magic happen.

# Problems
- If the book is supposably being sent to the kindle, but it never arrives, make sure you added your email as a confirmed mail on Amazon.
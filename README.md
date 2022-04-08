# Auto Manga Kindle Updater
Downloads mangas, converts them to .mobi files and then sends them to your Kindle. This can be used to download any amount of Manga or simply run on a time routine to always have the most up to date mangas on your Kindle.


# Requirements
- **Throwaway GMail account:** You want to create a new GMail account and turn [*Allow less secure apps to ON*](https://myaccount.google.com/lesssecureapps). It is not suggested to use an already existing account, because this option makes your account vulnerable.
- **Kindle Email Address**
- **Python 3.6 - 3.9**
- **Pipenv**
- [**KindleGen**](#installing-kindlegen)


# Installing
1. Clone to your folder using `git clone --recurse-submodules git@github.com:markbeep/AutoMangaKindleUpdater.git` so that the requried submodules are also installed.
2. Install KindleGen (so that it can create MOBI files)
  - [Windows](#windows)
  - [Linux](#linux)
  - [MacOS](#macos)
3. Install Pipenv
4. Call `pipenv install` to install the required packages
5. Enter the Python environment with `pipenv shell` and then run `main.py` (or `pipenv run python main.py`)
6. Add the login info to your throwaway GMail account into `data/login.json`
7. Update `manga.json` with the mangas you want downloaded and the amount that should be downloaded
8. Update `config.json` with the email address of your Kindle
9. Run `main.py` again and watch the magic happen.

# Problems
- If the book is supposably being sent to the kindle, but it never arrives, make sure you added your email as a confirmed mail on Amazon.

# Installing KindleGen

## Windows
1. Install [Kindle Previewer](https://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765261)
2. Inside of the Kindle Previewer files locate `kindlegen.exe`. Default location is `https://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765261`
3. Place `kindlegen.exe` in this root directory
4. Done

## Linux
1. Download the Linux version of KindleGen [over here](https://archive.org/download/kindlegen2.9/kindlegen_linux_2.6_i386_v2_9.tar.gz)
2. Go to where you downloaded it, create a folder and extract the contents inside that folder
 - `mkdir KindleGen`
 - `tar xvfz kindlegen_linux_2.6_i386_v2_9.tar.gz -C ./KindleGen`
4. Move the file `kindlegen` to `/usr/local/bin/
  - `mv ~/KindleGen/kindlegen /usr/local/bin/`
5. Done (you should now be able to call `kindlegen` in the terminal)

## MacOS
*I have no way of trying this out, but from what I gather it should be similar to the Windows install:*
1. Install [Kindle Previewer](https://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765261)
2. Locate `kindlegen` inside the install files. Default location is `/Applications/Kindle Previewer 3.app/Contents/lib/fc/bin/kindlegen`
3. Place `kindlegen` in this root directory
4. Hopefully done

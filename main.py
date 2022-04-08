from util.file_creation import check_files
from util.print_log import info


def main(args=[]):
    info("Starting Auto Manga Updater")
    # checks if all the required files are in place and exits otherwise
    if check_files():
        return

    # we only import later, to make sure the correct files exist
    from manga_search.manga_search import check_all
    check_all()
    info("Finished all operations")

if __name__ == "__main__":
    main()

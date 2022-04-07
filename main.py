from util.file_creation import check_files


def main(args=[]):
    # checks if all the required files are in place and exits otherwise
    if check_files():
        return

    # we only import later, to make sure the correct files exist
    from manga_search.manga_search import check_all
    check_all()


if __name__ == "__main__":
    main()

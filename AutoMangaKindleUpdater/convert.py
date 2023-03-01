import os, sys, getopt
from loguru import logger
from PIL import Image, UnidentifiedImageError
from typing import Tuple, List


def compile_document(input_dir: str, output_pdf: str):
    # converts the downloaded images or zip files to PDF
    image_list = []    
    images = os.listdir(input_dir)
    images.sort()
    for f in images:
        path = os.path.join(input_dir, f)
        if os.path.isdir(path):
            continue
        try:
            img = Image.open(path)
        except UnidentifiedImageError:
            continue
        logger.debug(f"Adding {path}")
        img.convert("RGB")
        image_list.append(img)

    if len(image_list) == 0:
        raise ValueError("There are no images in the given input directory")
    
    logger.info(f"Generating PDF: {output_pdf}")
    image_list[0].save(f"{output_pdf}", save_all=True, append_images=image_list[1:])
    logger.info(f"Generation successful. Saved to {output_pdf}")


def handle_input(argv: List[str]) -> Tuple[str, str]:
    opts, args = getopt.getopt(argv, "i:f:o:", ["--input-dir=", "--output-pdf="])
    input_dir = None
    output_pdf = None
    for opt, arg in opts:
        if opt in ["-i", "-f", "--input-dir"]:
            input_dir = arg
        elif opt in ["-o", "--output-pdf"]:
            output_pdf = arg
    # check the arguments at the end
    if input_dir is None and output_pdf is None and len(args) == 0:
        raise ValueError("--input-dir and --output-pdf not given")
    elif input_dir is None and len(args) == 0:
        raise ValueError("--input-dir is not given")
    elif output_pdf is None and len(args) == 0:
        raise ValueError("--output-pdf is not given")
    elif input_dir is not None and output_pdf is not None and len(args) > 0:
        raise ValueError("Arguments are not allowed if --input-dir and --output-pdf are given")
    if input_dir is None and output_pdf is None:
        logger.debug("input_dir & output_pdf are None, using the first two command line arguments")
        input_dir = args[0]
        output_pdf = args[1]
    elif input_dir is None:
        logger.debug("input_dir is None, using the first command line argument")
        input_dir = args[0]
    elif output_pdf is None:
        logger.debug("output_pdf is None, using the first command line argument")
        output_pdf = args[0]
    
    logger.debug(f"Input Directory: {input_dir}")
    logger.debug(f"Output PDF: {output_pdf}")
    
    return input_dir, output_pdf


def main(argv: List[str]):
    input_dir, output_pdf = handle_input(argv)
    if not os.path.exists(input_dir):
        raise ValueError("Invalid input_dir path")
    
    head, _ = os.path.split(output_pdf)
    if head != "":
        os.makedirs(head)

    compile_document(input_dir, output_pdf)
    
    logger.configure(levels=)
    
    
if __name__ == "__main__":
    main(sys.argv[1:])

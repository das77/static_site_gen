import os
import shutil
import logging

def copy_directory_recursive(src, dst):
    # Ensure the destination directory exists
    if not os.path.exists(dst):
        os.makedirs(dst)
        logging.info(f"Created directory: {dst}")

    # Iterate over all items in the source directory
    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dst_item = os.path.join(dst, item)

        # Check if it's a directory
        if os.path.isdir(src_item):
            logging.info(f"Copying directory: {src_item} to {dst_item}")
            copy_directory_recursive(src_item, dst_item)
        else:
            # It's a file, copy it
            logging.info(f"Copying file: {src_item} to {dst_item}")
            shutil.copy2(src_item, dst_item)
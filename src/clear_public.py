import os
import shutil
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def delete_all_contents(directory):
    """
    Deletes all files and subdirectories in the specified directory.
    
    :param directory: Path to the directory whose contents are to be deleted.
    """
    if not os.path.exists(directory):
        raise Exception(f"The directory {directory} does not exist.")
    
    # Iterate over all the items in the directory
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)  # Remove the file or link
            logging.info(f"Deleted file: {item_path}")
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)  # Remove the directory and all its contents
            logging.info(f"Deleted directory: {item_path}")
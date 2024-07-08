from copystatic import copy_directory_recursive
from generate_page import generate_page

import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def main():
    # Copy static files
    src_directory = "C:/Users/dsper/Projects/static_site_gen/static"
    dst_directory = "C:/Users/dsper/Projects/static_site_gen/public"
    try:
        copy_directory_recursive(src_directory, dst_directory)
    except Exception as err:
        logging.error(f'Error copying static files: {err}')
    # Set content source and dest paths
    from_path = 'C:/Users/dsper/Projects/static_site_gen/content/index.md'
    template_path = 'C:/Users/dsper/Projects/static_site_gen/template.html'
    dest_path = 'C:/Users/dsper/Projects/static_site_gen/public/index.html'
    # Generate page
    generate_page(from_path, template_path, dest_path)

if __name__ == '__main__':
    main()
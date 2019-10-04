#!/usr/bin/env python3
"""
This module extracts and does some simple cleanup of Google Photos takeout
archives.

WARNING: This module assumes all JSON metadata files aren't useful and deletes
them by default.
"""

import argparse
import fnmatch
import os
import zipfile

def dir_path(string):
    """Determines if the argument is an existing directory."""
    if os.path.isdir(string):
        return string
    else:
        raise argparse.ArgumentTypeError(
            'Path "' + string + '" is not a directory.')

PARSER = argparse.ArgumentParser(description=('Extract images and videos from a'
                                              ' directory of Google Photos '
                                              'Takeout archives.'))
PARSER.add_argument('takeout_dir', type=dir_path,
                    help='The directory containing Google Photos takeout '
                    'archives (i.e. one or multiple zip file)')

# Path to the Google Photos data directory in the extracted takeout data.
# When extracted the photos will be in: <takeout_dir>/Takeout/Google Photos/
PHOTOS_SUBDIR = ('Takeout', 'Google Photos')


def list_takeout_archives(takeout_dir):
    """Lists the full path of all Google Takeout archives."""
    dir_files = []
    for filename in os.listdir(takeout_dir):
        if fnmatch.fnmatch(filename, 'takeout-*.zip'):
            dir_files.append(os.path.join(takeout_dir, filename))
    return dir_files


def unzip_archives(takeout_dir):
    """Extracts all archives to the archive directory."""
    for archive in list_takeout_archives(takeout_dir):
        print('unzipping: ', archive)
        with zipfile.ZipFile(archive, 'r') as zip_ref:
            zip_ref.extractall(takeout_dir)


def delete_metadata_files(takeout_dir):
    """Deletes all metadata files in the Photos data."""
    for dirpath, _, filenames in os.walk(os.path.join(takeout_dir,
                                                      *PHOTOS_SUBDIR)):
        metadata_files = [os.path.join(dirpath, name) for name in filenames if
                          name.endswith('.json')]

        for metadata_file in metadata_files:
            os.remove(metadata_file)


def clean_up(takeout_dir, delete_archives=False):
    """Cleans up extra files and the compressed archives."""
    delete_metadata_files(takeout_dir)
    if delete_archives:
        takeout_archives = list_takeout_archives(takeout_dir)
        for archive in takeout_archives:
            print('deleting archive: ', archive)
            os.remove(archive)
    else:
        print("Not deleting archives.")


def main():
    args = PARSER.parse_args()
    unzip_archives(args.takeout_dir)

    # Clean up.
    answer = input("Delete all takeout archives? y/n: ")
    answer = True if answer == 'y' else False
    clean_up(args.takeout_dir, answer)

if __name__ == "__main__":
    main()

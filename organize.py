#!/usr/bin/env python3
"""
Tool for organizing and cleaning up Google takeout data.
"""

import argparse
import distutils.core
import os

import mail
import photos

def dir_path(string):
    """Determines if the argument is an existing directory."""
    if os.path.isdir(string):
        return string
    else:
        raise argparse.ArgumentTypeError(
            'Path "' + string + '" is not a directory.')

PARSER = argparse.ArgumentParser(description=('Tool for processing and '
                                              'organizing Google takeout '
                                              'data.'))
PARSER.add_argument('--photos_dir', type=dir_path,
                    help='The directory containing Google Photos takeout '
                    'archives (i.e. one or multiple zip file)')
PARSER.add_argument('--mbox_file',
                    help='The mbox file with Gmail takeout data.')


def _maybe_organize_photos_takeout(takeout_dir):
    if not takeout_dir:
        print('Invalid (or no) Photos takeout archive directory specified. Not '
              'extracting photos from archives.')
        return
    else:
        organize_photos = input('Organize Photos takeout archives? y/n: ')
        organize_photos = distutils.util.strtobool(organize_photos)
        if not organize_photos:
            return
    photos.organize_photos_takeout(takeout_dir)


def _maybe_extract_email_attachments(mbox_file_path):
    if (mbox_file_path and os.path.isfile(mbox_file_path) and
            mbox_file_path.endswith('.mbox')):
        answer = input('Extract mailbox attachments? y/n: ')
        answer = distutils.util.strtobool(answer)
        if answer:
            mail.extract_mail_attachments(mbox_file_path)
    else:
        print('Invalid (or no) .mbox path specified. Not extracting email '
              'attachments.')

def main():
    args = PARSER.parse_args()
    _maybe_organize_photos_takeout(args.photos_dir)
    _maybe_extract_email_attachments(args.mbox_file)

if __name__ == '__main__':
    main()

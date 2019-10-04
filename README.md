
# Recover your photos from Google Photos

1. Download all `.zip` archives for
   [*only* Google Photos data](https://takeout.google.com/settings/takeout).
   For me, selecting more than Google Photos resulted in an error. This is most
   likely because of the size of **all** of my Google data being so massive.
    *  Note: It can take hours or even days for Google to generate Zip files with
       all your data.
1. Run `./organize.py <directory where all your archives are>`.  For example:
   `./organize.py ~/Downloads/google_takeout_archives/`.  The script will:
    *  Find all of the takeout archives in this directory
    *  Extract the photos from these archives
    *  Delete extra metadata files (i.e. not the images and videos)
    *  Give you an option to delete the archives after to reclaim some hard
       drive space.
1. (Strongly recommended) Back up your photos somewhere else.  Google does a ton
   of work to make sure your images will never get accidentally delete or lost.
   So much that it's very unlikely you are willing/can afford to have the same
   level of reliability.  I'm no expert, but I've found [this subreddit's
   wiki](https://www.reddit.com/r/DataHoarder/wiki/backups) to be a good
   starting point for learning about how to back up.

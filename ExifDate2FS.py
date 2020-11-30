import argparse
import os
import pathlib
import sys
import time
from typing import Iterable

import exifread

if os.name == 'nt':
    from win32_setctime import setctime

SUPPORTED_FORMATS = ['jpg', 'jpeg', 'tif', 'tiff', 'webp', 'heic']

__version__ = '0.8.5'


# Ported from: https://github.com/victordomingos/optimize-images
def search_images(dirpath: str, recursive: bool) -> Iterable[str]:
    if recursive:
        for root, dirs, files in os.walk(dirpath):
            for f in files:
                if not os.path.isfile(os.path.join(root, f)):
                    continue
                extension = os.path.splitext(f)[1][1:]
                if extension.lower() in SUPPORTED_FORMATS:
                    yield os.path.join(root, f)
    else:
        with os.scandir(dirpath) as directory:
            for f in directory:
                if not os.path.isfile(os.path.normpath(f)):
                    continue
                extension = os.path.splitext(f)[1][1:]
                if extension.lower() in SUPPORTED_FORMATS:
                    yield os.path.normpath(f)


def main():
    start_time = time.time()
    c = 0
    s = 0
    parser = argparse.ArgumentParser(description='This tool will recursively update image file timestamps to '
                                                 'information from EXIF tag DateTimeOriginal.')
    parser.add_argument('directory', metavar='directory', type=str, help='Directory to start from')
    parser.add_argument('-nr', '--no-recursion', action='store_true',
                        help="Don't recurse through subdirectories.")
    parser.add_argument('--rename', help='Rename file to IMG_DATE_TIME (IMG_YYYYMMDD_HHMMSS)', action='store_true')
    parser.add_argument('-v', '--verbose', help='show every file processed', action='store_true')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    args = parser.parse_args()
    print('ExifDate2FS', __version__)
    if os.name == 'nt':
        # We strip nasty mess if trailing slash and quotes used
        directory = os.path.abspath(pathlib.PureWindowsPath(args.directory.rstrip("\"")))
    else:
        directory = os.path.abspath(pathlib.PurePosixPath(args.directory))
    if args.no_recursion:
        print('Processing non-recursively starting from', directory)
        recursive = False
    else:
        print('Processing recursively starting from', directory)
        recursive = True
    if not os.access(directory, os.W_OK):
        print('No such directory or not writable')
        sys.exit(1)
    for filepath in search_images(str(directory), recursive=recursive):
        with open(filepath, 'rb') as f:
            tags = exifread.process_file(f, details=False, stop_tag='DateTimeOriginal')
        if 'EXIF DateTimeOriginal' in tags.keys():
            datetime_original = tags['EXIF DateTimeOriginal'].values
            if args.verbose:
                print(filepath, datetime_original)
            if datetime_original != '0000:00:00 00:00:00':
                time_object = time.strptime(datetime_original, '%Y:%m:%d %H:%M:%S')
                unix_time = float(time.mktime(time_object))
                os.utime(filepath, (time.time(), unix_time))
                if os.name == 'nt':
                    # Set file creation date (Windows only)
                    setctime(filepath, unix_time)
                if args.rename:
                    oldext = os.path.splitext(filepath)[1]
                    newname = 'IMG_' + time.strftime('%Y%m%d_%H%M%S', time_object) + oldext
                    if newname.lower() != os.path.basename(filepath).lower():
                        newpath = os.path.dirname(filepath) + os.sep + newname
                        if not os.path.exists(newpath):
                            os.rename(filepath, newpath)
                            if args.verbose:
                                print("File renamed to", newname)
                        else:
                            print(newname, " already exists")
                    else:
                        print("No need to rename")
                c += 1
            else:
                print(filepath, 'EXIF DateTimeOriginal is zeroes')
                s += 1
        else:
            print(filepath, 'no EXIF DateTimeOriginal')
            s += 1

    print(c, 'files processed', s, 'skipped', 'in', (time.time() - start_time))


if __name__ == '__main__':
    main()

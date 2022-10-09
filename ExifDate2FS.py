#!/usr/bin/env python3
import argparse
import hashlib
import logging as log
import os
import pathlib
import sys
import time
from typing import Iterable

import exifread

if os.name == 'nt':
    from win32_setctime import setctime

SUPPORTED_FORMATS = ['jpg', 'jpeg', 'tif', 'tiff', 'webp', 'heic', 'heif', 'cr2']

__version__ = '0.8.14'


def issame(filepath1, filepath2):
    if os.path.getsize(filepath1) != os.path.getsize(filepath2):
        # Sizes dont' match, obviously not same
        return False
    hasher1 = hashlib.sha3_256()
    hasher2 = hashlib.sha3_256()
    with open(filepath1, 'rb') as afile:
        buf = afile.read()
        hasher1.update(buf)
    with open(filepath2, 'rb') as afile:
        buf = afile.read()
        hasher2.update(buf)
    if hasher1.hexdigest() == hasher2.hexdigest():
        return True
    else:
        return False


def update_fs(filepath, time_object):
    unix_time = float(time.mktime(time_object))
    os.utime(filepath, (time.time(), unix_time))
    if os.name == 'nt':
        # Set file creation date (Windows only)
        setctime(filepath, unix_time)


def rename_file(filepath, time_object, dedup=False):
    oldext = os.path.splitext(filepath)[1]
    newname = 'IMG_' + time.strftime('%Y%m%d_%H%M%S', time_object) + oldext
    if newname.lower() != os.path.basename(filepath).lower():
        newpath = pathlib.PurePath(os.path.dirname(filepath) + os.sep + newname)
        if not os.path.exists(newpath):
            try:
                os.rename(filepath, newpath)
                log.info("%s renamed to %s", str(filepath), newname)
            except PermissionError:
                log.error("Error renaming %s: %s is not writeable. ", str(filepath), newname)
                print(sys.exc_info())
        elif os.path.exists(newpath) and dedup and issame(filepath, newpath):
            try:
                os.replace(filepath, newpath)
                log.info("%s renamed to %s with overwrite (dedup)", str(filepath), newname)
            except PermissionError:
                log.error("Error renaming %s: %s is not writeable. ", str(filepath), newname)
                print(sys.exc_info())
        else:
            print(newname, "already exists")

    else:
        log.info("No need to rename")


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
    parser = argparse.ArgumentParser(description='This tool will recursively update image file timestamps to '
                                                 'information from EXIF tag DateTimeOriginal.')
    parser.add_argument('directory', metavar='directory', type=str, help='Directory to start from')
    parser.add_argument('-nr', '--no-recursion', action='store_true',
                        help="Don't recurse through subdirectories.")
    parser.add_argument('--rename', help='Rename file to IMG_DATE_TIME (IMG_YYYYMMDD_HHMMSS)', action='store_true')
    parser.add_argument('-d', '--dedup', help='Allow overwrite if file is the same (checksum)', action='store_true')
    parser.add_argument('-v', '--verbose', help='Show every file processed', action='store_true')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    args = parser.parse_args()
    print('ExifDate2FS', __version__)

    if args.verbose:
        log.basicConfig(format='%(message)s', level='INFO')
    else:
        log.basicConfig(format='%(message)s')

    if os.name == 'nt':
        # We strip nasty mess if trailing slash and quotes used
        directory = os.path.abspath(args.directory.rstrip("\""))
    else:
        directory = os.path.abspath(args.directory)
    if args.no_recursion:
        print('Processing non-recursively starting from', directory)
        recursive = False
    else:
        print('Processing recursively starting from', directory)
        recursive = True
    if not os.access(directory, os.W_OK) or not os.path.exists(directory):
        log.error('No such directory or not writable')
        sys.exit(1)
    for filepath in search_images(str(directory), recursive=recursive):
        filepath = pathlib.PurePath(filepath)
        extension = os.path.splitext(filepath)[1]
        if extension.lower() in ['.cr3', '.jxl']:
            # Reserved for special processing of special extensions
            pass
        else:
            try:
                with open(filepath, 'rb') as f:
                    tags = exifread.process_file(f, details=False)
                if 'EXIF DateTimeOriginal' in tags.keys():
                    datetime_original = tags['EXIF DateTimeOriginal'].values
                    try:
                        # Fix weird varians of EXIFs. Thanks to:
                        # https://github.com/TheLastGimbus/GooglePhotosTakeoutHelper/
                        datetime_original = datetime_original.replace('-', ':').replace('/', ':').replace('.', ':').replace('\\', ':').replace(': ', ':0')[:19]
                        time_object = time.strptime(datetime_original, '%Y:%m:%d %H:%M:%S')
                        update_fs(filepath, time_object)
                        log.info("%s %s", str(filepath), time.strftime("%Y-%m-%d %H:%M:%S", time_object))
                        if args.rename:
                            rename_file(filepath, time_object, dedup=args.dedup)
                        c += 1
                    except ValueError as e:
                        log.warning("%s EXIF date processing error: %s", str(filepath), str(e))
                else:
                    log.warning("%s no EXIF DateTimeOriginal", str(filepath))
            except Exception as e:
                log.warning("%s processing error: %s", str(filepath), e)
    print(c, 'files processed in', (time.time() - start_time))


if __name__ == '__main__':
    main()

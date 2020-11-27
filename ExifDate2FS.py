import time
import os
import sys
import exifread
import argparse
import pathlib

if os.name == 'nt':
    from win32_setctime import setctime

__version__ = '0.8.0'


def main():
    start_time = time.time()
    c = 0
    s = 0
    supported = ('.jpg', '.jpeg', '.tiff', '.webp', '.heic')
    parser = argparse.ArgumentParser(description='This tool will recursively update image file timestamps to '
                                                 'information from EXIF tag DateTimeOriginal.')
    parser.add_argument('directory', metavar='directory', type=str, help='Directory to start from')
    parser.add_argument('-v', '--verbose', help='show every file processed', action='store_true')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    args = parser.parse_args()
    print('ExifDate2FS', __version__)
    if os.name == 'nt':
        # We strip nasty mess if trailing slash and quotes used
        directory = pathlib.PureWindowsPath(args.directory.rstrip("\""))
    else:
        directory = pathlib.PurePosixPath(args.directory)
    print('Processing recursively starting from', directory)
    if not os.access(directory, os.W_OK):
        print('No such directory or not writable')
        sys.exit(1)
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            filepath = subdir + os.sep + filename.lower()
            if filepath.endswith(supported):
                f = open(filepath, 'rb')
                tags = exifread.process_file(f, details=False, stop_tag='DateTimeOriginal')
                if 'EXIF DateTimeOriginal' in tags.keys():
                    datetime_original = tags['EXIF DateTimeOriginal'].values
                    if args.verbose:
                        print(filepath, datetime_original)
                    if datetime_original != '0000:00:00 00:00:00':
                        unix_time = float(time.mktime(time.strptime(datetime_original, '%Y:%m:%d %H:%M:%S')))
                        os.utime(filepath, (time.time(), unix_time))
                        if os.name == 'nt':
                            # Set file creation date (Windows only)
                            setctime(filepath, unix_time)
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

# ExifDate2FS

This tool will recursively update file timestamps to information from EXIF tag DateTimeOriginal. It accepts one argument - filesystem path.
It will not modify files themselves, only filesystem timestamps. For Linux it will modify mtime while for Windows it will also modify
“Date Created”.

## Supported file formats (file extensions):

* JPEG (.jpg/.jpeg)
* TIFF
* WebP
* HEIF (.heic)

Supports Windows, Linux, MacOS and probably other OSes.

## Installation

```sh
pip install exifdate2fs
```

You can download and use it as single Windows binary, see [Releases](https://github.com/varnav/ExifDate2FS/releases/)

## Usage

### PiPy package

```sh
exifdate2fs [-h] [-v] directory
```

### Windows executable

```cmd
./ExifDate2FS.exe [-h] [-v] directory
```

## See also

* [Jhead](https://www.sentex.ca/~mwandel/jhead/)
* [ExifTool](https://exiftool.org/)
* [Exiv2](http://www.exiv2.org/)
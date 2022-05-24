# ExifDate2FS

This tool will recursively update file timestamps to information from EXIF tag DateTimeOriginal. It accepts one argument - filesystem path.
It will not modify files themselves, only filesystem timestamps. For Linux, it will modify mtime while for Windows it will also modify
“Date Created”.

Optionally you can rename file to IMG_YYYYMMDD_HHMMSS.jpg with `--rename`

## Supported file formats (file extensions):

* JPEG (.jpg .jpeg)
* TIFF (.tif .tiff)
* WebP
* HEIC/HEIF (.heic, .heif) - experimental
* CR2 (.cr2)

Supports Windows, Linux, macOS and probably other OSes.

## Installation

```sh
pip install exifdate2fs
```

You can download and use it as single Windows binary, see [Releases](https://github.com/varnav/ExifDate2FS/releases/)

Unfortunately antiviruses [don't like packed Python executables](https://github.com/pyinstaller/pyinstaller/issues?q=is%3Aissue+virus+is%3Aclosed), so expect false positives from them if you go this way. Best way is pip.

## Usage

### PiPy package

```sh
exifdate2fs /home/username/myphotos
```

### Windows executable

```cmd
./ExifDate2FS.exe "c:\Users\username\Pictures\My Vacation"
```

## See also

* [Jhead](https://www.sentex.ca/~mwandel/jhead/)
* [ExifTool](https://exiftool.org/)
* [Exiv2](http://www.exiv2.org/)
* [NameEXIF](https://us.digicamsoft.com/softnamexif.html)
* [EXIF Date Changer](https://www.relliksoftware.com/exifdatechanger/)

# ExifDate2FS

This tool will recursively update file timestamps to information from EXIF tag DateTimeOriginal. It accepts one argument - filesystem path.
It will not modify files themselves, only filesystem timestamps. For Linux it will modify mtime while for Windows it will also modify
“Date Created”.

Supported file formats (file extensions):

* JPEG (jpg/jpeg)
* TIFF
* WebP
* HEIC

Supports Windows, Linux, and probably other OSes.

You can use it as single Windows binary, see "Releases" on the right. 

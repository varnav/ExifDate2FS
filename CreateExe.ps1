& venv\Scripts\Activate.ps1
$env:PYTHONOPTIMIZE = 1
pyinstaller -y --onefile ExifDate2FS.py
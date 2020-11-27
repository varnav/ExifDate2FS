import setuptools
import os
import shutil
import ExifDate2FS

if not os.path.exists('exifdate2fs'):
    os.mkdir('exifdate2fs')
shutil.copyfile('ExifDate2FS.py', 'exifdate2fs/__init__.py')

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    'exifread>=2',
    'win32-setctime ; platform_system=="Windows"'
]

setuptools.setup(
    name="exifdate2fs",  # Replace with your own username
    version=ExifDate2FS.__version__,
    author="Evgeny Varnavskiy",
    author_email="varnavruz@gmail.com",
    description="This tool will recursively update file timestamps to information from EXIF tag DateTimeOriginal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/varnav/ExifDate2FS",
    keywords=["jpeg", "exif", "filesystem", "filetime"],
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Utilities",
        "Topic :: Multimedia :: Graphics",
        "Environment :: Console",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires='>=3.7',
    entry_points={
        "console_scripts": [
            "exifdate2fs = exifdate2fs.__init__:main",
        ]
    }
)

Automate generating your android drawables
==========================================

build-drawables.py uses a template res folder (T) to build the real res folder (R). It looks for all folder in T
starting with drawable. If the folder name contains a DPI category (e.g. drawable-portrait-mdpi) it's contents are
copied to R/drawable-portrait-mdpi because it is assumed that every file in this folder is prerendered for mdpi.
If there is not DPI category in the name (e.g. drawable-portrait) every file is copied to R/drawable-portrait except for
the files ending on ".svg". They are rendered using the inkscape command line tool and saved in the appropriate dpi
specific folders: e.g. R/drawable-portrait-(lpdi|mdpi|hdpi|xhdpi).

SVG requirements
----------------

Your svgs must be made for mdpi.

Usage
-----

```sh
./build-drawables.py --src /path/to/template-res --out /path/to/android-project/res
```


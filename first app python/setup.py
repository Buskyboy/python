from setuptools import setup

APP = ['wxtryontest.py']
 
OPTIONS = { 
    'argv_emulation': True,
    'packages': ['yt_dlp'],
    'packages': ['wxpython'],
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
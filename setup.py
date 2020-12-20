from setuptools import setup

setup(name='xtranslator',
      packages=['xtranslator'],
      install_requires=[
          'PySide2',
          'numpy',
          'pillow',
          'pytesseract',
          'opencv-python',
          'argostranslate'
      ])

from setuptools import setup, find_packages

setup(
    name='ocr_video_processor',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'opencv-python-headless',
        'numpy',
        'pytesseract',
        'googletrans==4.0.0-rc1',
        'Pillow',
    ],
    entry_points={
        'console_scripts': [
            'ocr_video_processor = src.ocr_handler:main',
        ],
    },
    author='sayuz',
    author_email='pioneerofcomputer.shb@gmail.com',
    description='A package for OCR processing in videos',
    url='https://github.com/bshakhruz/ocr_video_processor',
)

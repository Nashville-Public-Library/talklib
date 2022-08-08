# talklib

## A TL module to process shows and segments

Use this module to process two types of shows/segments:
- shows/segments we receive via RSS feed
    - such as New York Times, Wall Street Journal, etc.
- shows/segments downloaded locally ahead of time
    - such as Sound Beat, Animal Airwaves, etc.

---
## Installation

To use this module, clone this repo, unzip it, remove the `-main` from the directory name, and copy the directory to the `site-packages` directory inside the Python directory. If it exists, DO overwrite the existing directory.

Depending on how you installed Python, the `site-packages` directory could be somewhere like: `C:\Users\<username>\AppData\Local\Programs\Python\Python###\Lib\site-packages`

---

## Dependencies

To use this module, you will need Python 3.10.1+ AND Windows binaries for the following installed on the PC and added to the PATH:

- **FFmpeg**

- **FFprobe**

- **Wget**

To repeat, this module **will not work** without FFmpeg, FFprobe, and Wget.

It also uses a number of environment variables. Make sure to set all of these on your PC. (*TODO: make a list of these and add it here*)


*An obvious improvement here would be to download the audio files for the RSS feeds in a more "Pythonic" fashion, IE not using Wget.*

---

## Usage
 

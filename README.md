# talklib

## A module to automate processing of shows/segments airing on the TL

Use this module to process these types of shows/segments:
- Full shows we receive via RSS feed
    - such as New York Times, Wall Street Journal, etc.
- Segments we receive via RSS Feed
    - Such as Health in a Heartbeat, Academic Minute, etc.
- Segments we receive via "permalink"
    - such as PNS
- Segments downloaded locally ahead of time
    - such as Sound Beat, Animal Airwaves, etc.

---

## Dependencies

### -Python
Use Python 3.10.1 or above.

### -Binaries
You need Windows binaries for the following installed on the PC and added to the PATH:

- **[FFmpeg](https://www.ffmpeg.org/download.html#build-windows)**
- **FFprobe**
- **[Wget](http://wget.addictivecode.org/FrequentlyAskedQuestions.html#download)**

To repeat, **this module will not work without FFmpeg, FFprobe, and Wget**. 

FFmpeg and FFprobe should be two separate binaries.

### -Twilio
[Twilio](https://www.twilio.com/) is used for SMS notifications. There is a [Twilio library for Python](https://www.twilio.com/docs/libraries/python). It is not in the Python standard library and needs to be installed via PIP (`pip install twilio`). Store the Twilio credentials in environment variables on the PCs, as shown in the script. 

The alternative is to use `curl` with long, complicated URLs. See the "Usage" section below for how to disable Twilio.

### -Environment Variables
Many items are stored in environment variables. Make sure to set all of these on your PC(s). (*TODO: make a list of these and add it here*)


*An obvious improvement here would be to download the audio files for the RSS feeds in a more "Pythonic" fashion, IE not using Wget.*

---
## Installation

To use this module: 
- clone this repo 
- unzip it
- remove the "-main" from the directory name (it should just be called "talklib")
- copy the directory to the `site-packages` directory inside the Python directory
- If it exists, DO overwrite the existing directory.

Depending on how you installed Python, the `site-packages` directory could be somewhere like: `C:\Users\<username>\AppData\Local\Programs\Python\Python###\Lib\site-packages`

---

## About WireReady

Before we begin, a general note:

### We run most of our Python scripts via WireReady (WR)
- The "Run" command in WR defaults to running from a different directory AND a different drive letter. This causes confusion.
- WR also does not run `.py` files by default. 
- For these reasons and more, we do not run `.py` files directly from WR.
- Instead, we tell WR to run a Batch script (`.bat` file) which in turn will run the Python script (`.py` file). 
- The batch script ensures we CD to the correct directory.
- Ensure the Batch & Python scripts are in the same directory.
- A sample `.bat` file (`Example.bat`) is inlcuded in this repo. 

Here is what an example directory structure should look like:
````
D:\wireready
    \Washington Post
        \WP.bat
        \WP.py
````
You would tell WR to run the `WP.bat` file, which would run the `WP.py` file.

---

## Usage
In a new Python script, use `from talklib.show import TLShow` to import the class to your script. 

Create an instance like this: 

`example = TLShow()`

---

### RSS Example

For an RSS show, here is an example script:

````
from talklib.show import TLShow

WP = TLShow()

WP.show = 'Washington Post'
WP.show_filename = 'WP'
WP.url = 'https://somesite.org/wp-feed.rss'
WP.remove_yesterday = True
WP.include_date = True
WP.check_if_above = 59
WP.check_if_below = 55

WP.run()
````

Let's go through what each of these are for

`show` (required)
- This is the name of the program
- Mostly used for notifications, etc.
- enclose in quotes (single or double, Python doesn't care)

`show_filename` (required)
- the filename of the program
- note that it does NOT include a trailing dash `-` OR the file extension `.wav`. use the base name only
- enclose in quotes

`url` (required)
- link to the RSS feed
- ensure there is not a trailing forward slash `/` at the end of the link
    - correct: 'https://somesite.org/wpfeed.rss'
    - incorrect: 'https://somesite.org/wpfeed.rss/'
- enclose in quotes

`remove_yesterday` (optional)
- whether or not you want to remove yesterday's files (if any exists)
- if set to `True`, it will delete any file matching the show_filename attribute you set.
- the default is `False`. 

`include_date` (optional)
- whether or not you want to include today's date in the filename
- if set to `True`, the date will be appended as such: `WP-MMDDYY.wav`
- if not set, or set to `False`, the resulting filename will be: `WP.wav`
- Generally, for TL programs, if it is a daily show, like the New York Times, etc., you need the date in the filename, as this is what WireReady will match.
- the default is `False`

`check_if_above` and `check_if_below` (optional)
- these are for checking whether the length of the program (**in minutes!**) falls outside a range
- used strictly for notification purposes
- decimal numbers are OK.
- if these are not set, the checks will not be run
- do not enclose in quotes
- again, these values are in MINUTES

`run()`
- starts running the script with the attributes you set

---
### Local File Example

For a show whose files we already have downloaded, here is an example script:

````
from talklib.show import TLShow

MWB = TLShow()

MWB.show = 'Magical World of Bees'
MWB.show_filename = 'MWB'
MWB.is_local = True
MWB.local_file = 'D:Production\path\to\the\file.wav'
MWB.remove_source = True
MWB.check_if_above = 2.1
MWB.check_if_below = 1.9

MWB.run()
````
Definitions for attributes unique to local shows:

`is_local` (required)
- tells the module that this is a local show
- you must set this to `True` if it is a local show
- default is `False`

`local_file` (required)
- path to the local file
- you will not probably not have a hardcoded path here. Usually, you will be running a short algorithm to determine the path. Please see the [MISC](https://github.com/talkinglibrary/misc) repo for some examples.

`remove_source` (optional)
- whether or not you want to remove/delete the local source file after processing
- default is `False`

----
### Permalink Example

By "permalink", We're referring to shows whose audio URL does not change, E.G. PNS. For shows we receive via permalink, here is an example script:
````
from talklib.show import TLShow

WK = TLShow()

WK.show = 'Who Knows'
WK.show_filename = 'WhoKnows'
WK.url = 'https://somesite.org/who-knows-static'
WK.is_permalink = True

WK.run()
````

Definitions for attributes unique to "permalink" shows:

`is_permalink` (required)
- set to `True` for permalink shows
- default is `False`

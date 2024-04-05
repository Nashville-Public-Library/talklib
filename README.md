# talklib

![tests](https://github.com/Nashville-Public-Library/talklib/actions/workflows/talklib.yml/badge.svg)

## A package to automate processing of shows/segments airing on the TL

[Skip to Examples](#examples)

*THIS README IS INTENDED TO ASSIST TL STAFF IN INSTALLING AND USING THIS PACKAGE*

Use this module to process the following types of shows/segments:
- Shows and segments we receive via RSS feed
    - Shows such as New York Times, Wall Street Journal,  etc.
    - Segments such as Health in a Heartbeat, Academic Minute, etc.
- Segments we receive via "permalink"
    - Such as PNS, Cirrus, etc.
- Segments downloaded locally ahead of time
    - Such as Sound Beat, Animal Airwaves, etc.

---

## Requirements

### -[Python](https://www.python.org/downloads/)
Use Python 3.10.1 or above.

### -[FFmpeg](https://www.ffmpeg.org/download.html#build-windows)
You need Windows binaries for FFmpeg & FFprobe installed on the PC and added to the PATH:

To repeat, **this package will not work without FFmpeg and FFprobe**. 

FFmpeg and FFprobe should be two separate binaries.

### -[Twilio](https://www.twilio.com/)
Twilio is used for SMS and phone call notifications.

Access our TL Twilio info (token, etc.) by [logging in](https://www.twilio.com/login) to Twilio.

See [below](#disable-twilio) for how to disable Twilio.

### -Environment Variables
Several global variables used here are pulled from environment variables. This gives the module more portability, and keeps sensitive info separated.

The entire list of these is in the ev.py file. Make sure to set all of these on your PC(s). They are case-sensitive!

---
## Installation

- Open a terminal/command prompt
- Run `pip install talklib`. That's it!
    - Depending on your OS, instead of `pip` you may need to use `pip3`
    - This will install the package globally. If you're a TL user just trying to install the package for everyday use, that's likely what you want to do. If you want to install it locally (for testing, etc.), see the [development](#development) section below.
    - If you already have it installed and need to update it to the newest version, run `pip install --upgrade talklib`

---

## About WireReady

Before we begin, a general note:

### We run most of our Python scripts via WireReady (WR)
- The "Run" command in WR defaults to running from a different directory AND a different drive letter. This causes confusion.
- WR also does not run `.py` files by default. 
- These are some of the reasons why we do not run `.py` files directly from WR.
- Instead, we tell WR to run a Batch script (`.bat` file) which in turn will run the Python script (`.py` file).
- Ensure the Batch & Python scripts are in the same directory.
- A sample `.bat` file (`Example.bat`) is included in the [misc](https://github.com/Nashville-Public-Library/misc/tree/main/talklib_examples) repo. 
- PLEASE NOTE: the `.bat` file will run all Python files in the folder. This is one reason it is best to separate your Python files into different folders, each with its own `.bat` file.

Here is what an example directory structure should look like:
````
D:\wireready
    \Washington Post
        -WP.bat
        -WP.py
````
You would tell WR to run the `WP.bat` file, which would run the `WP.py` file.

----

## Usage

[Skip to Examples](#examples)

`TLShow` is the main class to use.

Import the class to your script like this:

`from talklib import TLShow`

This is also fine:

`from talklib.show import TLShow`

Create an instance like this: 

`example = TLShow()`

----

## Available Attributes

### here is a list of all the attributes, along with their type and whether they are required.

`show`

*string*

required
- This is the name of the program
- Mostly used for notifications, etc.

`show_filename`

*string*

required

- the filename of the program
- do NOT include a trailing dash `-` OR a file extension `.wav`. use the base name only 

`url`

*string*

required for all RSS or permalink shows
- URL for the RSS feed OR the permalink
- ensure there is not a trailing forward slash `/` at the end of the URL
    - correct: 'https://somesite.org/wpfeed.rss'
    - incorrect: 'https://somesite.org/wpfeed.rss/'

`is_local`

*boolean*

*required* for "local" shows
- tells the module whether this is a local show
- must be set to `True` if it is a local show
- default is `False`

`local_file`

*string*

required for "local" shows
- path to the local file as such: `D:\path\to\the\show.wav`
- you will probably not have a hardcoded path here. Usually, you will be running a short algorithm to determine the path. Please see the [MISC](https://github.com/talkinglibrary/misc) repo for some examples.

`is_permalink`

*boolean*

required for "permalink" shows
- must be set to `True` for permalink shows
- default is `False`

`remove_yesterday`

*boolean*

optional
- whether or not you want to remove yesterday's files (if any exists)
- if set to `True`, it will delete any file matching the show_filename attribute you set.
- default is `False`. 

`include_date`

*boolean*

optional
- whether or not you want to include today's date in the filename
- if set to `True`, the date will be appended as such: `WP-MMDDYY.wav`
- if not set, or set to `False`, the resulting filename will be: `WP.wav`
- Generally, for TL programs, if it is a daily show, like the New York Times, etc., you need the date in the filename, as this is what WireReady will match.
- the default is `False`

`check_if_above` and `check_if_below`

*number*

optional
- these are for checking whether the length of the program (**in minutes!**) falls outside a range
- used strictly for notification purposes
- if these are not set, the checks will not be run
- again, these values are in **minutes**, not seconds
- currently, if you set one of these, you must set both of them. All or nothing.

`remove_source`

*boolean*

optional
- whether you want to remove/delete the original source file after processing
- applies only to local shows
- default is `False`

`notifications`

*object*

optional
- this is its own object with the following attributes: 
    - `enable_all`
    - `syslog_enable`
    - `twilio_enable`
    - `email_enable`
- to disable all notifications, set `enable_all` to false like this: `object.notifications.enable_all = False`
- to disable a particular one of these, set them like this: `object.notifications.twilio_enable = False`
- default for all of them is `True`
- more [examples](#examples) below

`ffmpeg`

*object*

- this is its own object with various attributes. The ones you might want to change are `breakaway` and `compression_level`
    - `breakaway`
        - if you only want to convert/output the audio file up to a certain point, set this to the number of seconds at which point you want it to stop.
        - change it like this: `object.ffmpeg.breakaway = 120`. This will cut the audio at 2 minutes.
        - again, this number is in seconds (not minutes)
        - perhaps the only time you need to set this is for shows like PNS where there is an expected "breakaway" time.
        - default is to convert the entire file

    - `compression_level`
        - sets the level for FFmpeg's compression/normalization
        - this is the EBU R128 LUFS "integrated loudness" standard
        - change it like this: `object.ffmpeg.compression_level = 18`
        - the smaller the number, the more compression is applied (17 is more compressed than 18)
        - the max is 5 (do not set to 1, 2, 3, or 4)!
        - be careful with this!
        - default is 21

### Notes about formatting:

if you're new to Python, here're some reminders

### string 
- must be enclosed in quotes (single or double; Python doesn't care)

### boolean
- either True or False
- do not enclose in quotes
- must be capitalized
    - correct: True
    - incorrect: true
    
### number
- in our case, these can be either type int OR float, meaning either whole numbers OR decimal numbers are allowed
    - OK: 5
    - also OK: 5.4
- do not enclose in quotes

## Methods

`run()`

required
- executes the script with the attributes you set
- should be the last line in your script

this should be the only method/function you call directly from an outside script. Even if your IDE shows you all the available methods, please ignore them as most of them are not (yet) designed to be called directly.


----
## Examples<a id="examples"></a>
### RSS Example

The minimum attributes you must set are `show`, `show_filename`, and `url`.

Here is an example script:

````python
from talklib import TLShow

SD = TLShow()

SD.show = 'Skywalker Daily News'
SD.show_filename = 'SDN'
SD.url = 'https://somesite.org/sdn-feed.rss'

SD.run()
````
---
### Local Example

"Local" shows are shows whose files we already have downloaded ahead of time.

The minimum attributes you must set are: `show`, `show_filename`, `is_local`, and `local_file`. 

Here is an example script:

````python
from talklib import TLShow

MWB = TLShow()

MWB.show = 'Magical World of Bees'
MWB.show_filename = 'MWB'
MWB.is_local = True
MWB.local_file = 'D:Production\path\to\the\file.wav'

MWB.run()
````
----
### Permalink Example

"Permalink" shows are shows whose audio URL does not change, E.G. PNS & Cirrus

The minimum attributes you must set are: `show`, `show_filename`, `url`, and `is_permalink`.

Here is an example script:

````python
from talklib import TLShow

WK = TLShow()

WK.show = 'Who Knows'
WK.show_filename = 'WhoKnows'
WK.url = 'https://somesite.org/who-knows-static'
WK.is_permalink = True

WK.run()
````

### Misc. Examples

Here are some examples of how to access/modify certain attributes. 

### Disable Twilio<a id="disable-twilio"></a>

To disable Twilio notifications, simply add a line like this:

````python
from talklib import TLShow

SD = TLShow()

SD.show = 'Skywalker Daily News'
SD.show_filename = 'SDN'
SD.url = 'https://somesite.org/sdn-feed.rss'
SD.notifications.twilio_enable = False

SD.run()
````

### Disable Notifications

To disable ALL notifications, add a line like this:

> This will disable all notifications **including** syslog messages

````python
from talklib import TLShow

SD = TLShow()

SD.show = 'Skywalker Daily News'
SD.show_filename = 'SDN'
SD.url = 'https://somesite.org/sdn-feed.rss'
SD.notifications.enable_all = False

SD.run()
````

### Adjust FFmpeg compression

To adjust the level of compression applied with FFmppeg, add a line like this:

````python
from talklib import TLShow

SD = TLShow()

SD.show = 'Skywalker Daily News'
SD.show_filename = 'SDN'
SD.url = 'https://somesite.org/sdn-feed.rss'
SD.ffmpeg.compression_level = 18

SD.run()
````

-----
## Development<a id="development"></a>

- Clone this repository
    - `git clone https://github.com/Nashville-Public-Library/talklib.git`
- cd into the folder
    - `cd talklib`
- Create a virtual environment
    - `python -m venv venv`
    - depending on your OS, instead of `python`you may need to use `py` or `python3`
- Activate virtual environment
    - On Windows: `venv\Scripts\activate`
    - On Mac: `source venv/bin/activate`
- Update pip
    - `pip install --upgrade pip`
    - depending on your OS, instead of `pip` you may need to run `pip3`
- Install the package into your virtual environment
    - `pip install -e .`
- Run Pytest
    - `pytest`
        - to see code coverage, use `pytest --cov=talklib`
    - The tests can take a while to run. Watch the terminal output for progress.
    - If the tests fail, you may have installed something incorrectly. 
    - You must be connected to the internet to run the tests


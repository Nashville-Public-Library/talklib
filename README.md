# talklib

## A module to automate processing of shows/segments airing on the TL

[Skip to Examples](#examples)

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
[Twilio](https://www.twilio.com/) is used for SMS notifications. There is a [Twilio library for Python](https://www.twilio.com/docs/libraries/python). It is not in the Python standard library and needs to be installed via PIP (`pip install twilio`).

Access our TL Twilio info (token, etc.) by [logging in](https://www.twilio.com/login) to Twilio.

See the "Usage" section below for how to disable Twilio.

### -Environment Variables
Several global variables used here are pulled from environment variables. This gives the module more portability, and keeps sensitive info out of the module.

The entire list of these is in the ev.py file. Make sure to set all of these on your PC(s). They are case-sensitive!

---
## Installation

### Download
- clone this repo 
- unzip it
- remove the "-main" from the directory name (it should just be called "talklib")
- copy the directory to the `site-packages` directory inside the Python directory
- If it exists, DO overwrite the existing directory.

Depending on how you installed Python, the `site-packages` directory could be somewhere like: `C:\Users\<username>\AppData\Local\Programs\Python\Python###\Lib\site-packages`

### Install Python Packages
- open a `cmd` terminal
- cd to this directory
- run `pip install -r requirements.txt`

This will download all the Python packages we're using. Yes, doing this will download the packages globally. It's probably fine, for now...

---

## About WireReady

Before we begin, a general note:

### We run most of our Python scripts via WireReady (WR)
- The "Run" command in WR defaults to running from a different directory AND a different drive letter. This causes confusion.
- WR also does not run `.py` files by default. 
- These are some of the reasons why we do not run `.py` files directly from WR.
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

----

## Usage

`TLShow` is the main class to use.

Import the class to your script like this:

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

`remove_source`

*boolean*

optional
- whether you want to remove/delete the original source file after processing
- applies only to local shows
- default is `False`

`notifications`

*boolean*

optional
- whether you want to enable notifications (email, SMS)
- if disabled, you do not need to also disable twilio.
- True = enable, False = disable
- default is `True`

`breakaway`

*number*

optional
- if you only want to convert/output the audio file up to a certain point, set this to the number of seconds at which point you want it to stop.
- again, this number is in **seconds**, not minutes
- perhaps the only time you need to set this is for shows like PNS where there is an expected "breakaway" time.
- default is to convert the entire file

`twilio_enable`

*boolean*

optional
- whether you want to enable twilio (SMS) notifications
- True = enable, False = disable
- default is `True`

`ff_level`

*number*

optional
- sets the level for FFmpeg's compression/normalization
- this is the EBU R128 LUFS "integrated loudness" standard
- the smaller the number, the more compression is applied (17 is more compressed than 18)
- the max is 5 (do not set to 1, 2, 3, or 4)!
- **be careful with this!**
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
## Examples
### RSS Example

The minimum attributes you must set are `show`, `show_filename`, and `url`.

Here is an example script:

````python
from talklib.show import TLShow

SD = TLShow()

SD.show = 'Skywalker Daily News'
SD.show_filename = 'SDN'
SD.url = 'https://somesite.org/sdn-feed.rss'
SD.remove_yesterday = True
SD.include_date = True
SD.check_if_above = 59
SD.check_if_below = 55

SD.run()
````
---
### Local Example

"Local" shows are shows whose files we already have downloaded ahead of time.

The minimum attributes you must set are: `show`, `show_filename`, `is_local`, and `local_file`. 

Here is an example script:

````python
from talklib.show import TLShow

MWB = TLShow()

MWB.show = 'Magical World of Bees'
MWB.show_filename = 'MWB'
MWB.is_local = True
MWB.local_file = 'D:Production\path\to\the\file.wav'
MWB.remove_source = True
MBW.twilio_enable = False

MWB.run()
````
----
### Permalink Example

"Permalink" shows are shows whose audio URL does not change, E.G. PNS.

The minimum attributes you must set are: `show`, `show_filename`, `url`, and `is_permalink`.

Here is an example script:

````python
from talklib.show import TLShow

WK = TLShow()

WK.show = 'Who Knows'
WK.show_filename = 'WhoKnows'
WK.url = 'https://somesite.org/who-knows-static'
WK.is_permalink = True
WK.notifications = False

WK.run()
````
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

See the "Usage" section below for how to disable Twilio.

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

----

## Usage

`TLShow` is the main class to use.

In a new Python script, import the class to your script like this:

`from talklib.show import TLShow`

Create an instance like this: 

`example = TLShow()`

## Instance Attributes


`show`

required for all types of shows/segments
- This is the name of the program
- Mostly used for notifications, etc.
- enclose in quotes (single or double, Python doesn't care)

`show_filename`

required for all types of shows/segments
- the filename of the program
- note that it does NOT include a trailing dash `-` OR the file extension `.wav`. use the base name only
- enclose in quotes

`url`

required for all RSS or permalink shows
- link to the RSS feed
- ensure there is not a trailing forward slash `/` at the end of the link
    - correct: 'https://somesite.org/wpfeed.rss'
    - incorrect: 'https://somesite.org/wpfeed.rss/'
- enclose in quotes

`is_local`

required for "local" shows
- tells the module that this is a local show
- you must set this to `True` if it is a local show
- default is `False`

`local_file`

required for "local" shows
- path to the local file as such: `D:\path\to\the\show.wav`
- you will not probably not have a hardcoded path here. Usually, you will be running a short algorithm to determine the path. Please see the [MISC](https://github.com/talkinglibrary/misc) repo for some examples.

`is_permalink`

required for "permalink" shows
- set to `True` for permalink shows
- default is `False`

`remove_yesterday`

optional
- whether or not you want to remove yesterday's files (if any exists)
- if set to `True`, it will delete any file matching the show_filename attribute you set.
- the default is `False`. 

`include_date`

optional
- whether or not you want to include today's date in the filename
- if set to `True`, the date will be appended as such: `WP-MMDDYY.wav`
- if not set, or set to `False`, the resulting filename will be: `WP.wav`
- Generally, for TL programs, if it is a daily show, like the New York Times, etc., you need the date in the filename, as this is what WireReady will match.
- the default is `False`

`check_if_above` and `check_if_below`

optional
- these are for checking whether the length of the program (**in minutes!**) falls outside a range
- used strictly for notification purposes
- decimal numbers are OK.
- if these are not set, the checks will not be run
- do not enclose in quotes
- again, these values are in MINUTES

`remove_source`

optional
- whether or not you want to remove/delete the local source file after processing
- applies only to local shows
- default is `False`

`notifications`

optional
- whether you want to turn notifications (email, SMS) on or off
- set to False if you want to turn notifications off
- default is True

`breakaway`

optional
- if you only want to convert/output the audio file up to a certain point, set this to the number of seconds at which point you want it to stop.
- decimal numbers are OK
- again, this number is in **seconds**, not minutes
- perhaps the only time you need to set this is for shows like PNS where there is an expected "breakaway" time.
- default is to convert the entire file

### to run the script:

`run()`

required
- executes the script with the attributes you set


----
## Examples
### RSS Example

For an RSS show, here is an example script:

````
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

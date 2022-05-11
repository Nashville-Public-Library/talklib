# rss

Various scripts to parse RSS feeds and download their audio files

What you need:

- **Python 3.10.1+**

- **FFmpeg**

- **FFprobe**

- **Wget**

These need to be installed and added to the PATH.
Also, set the environment variables as shown in the scripts, or change these manually.
For TL, it's best to use environment variables.

We're also using **Twilio** for SMS notifications. Install via PIP.
Credentials can be retrieved by logging in to the Twilio dashboard.

-----
## rss_show 

for daily, full shows with a date

This will check the RSS feed and, if the newest entry has a pub date matching today's date,
it will download the linked audio file, convert it to TL format via FFmpeg, and transfer the file
to the destination directory(ies). It also runs some checks/tests along the way. See source for more info.


Do not use zero for the check_if_above & below variables unless you want a notifcation each time you run it.
To disable the, comment out the check_length function call.

-----
## rss_segment 

for daily, short segments without a date
 

# rss

Various scripts to parse RSS feeds and download their audio files

These check the given RSS feed and, if the newest entry/episode's pub date matches today's date,
it will download the linked audio file, convert it to TL format via FFmpeg, and transfer the file
to the destination(s). It also runs some checks/tests along the way. See source for more info.

You can leave the check_if_above & below variables at zero, but that will cause notifcations each time you run it.

For EITHER of these scripts, here's What you need:

- **Python 3.10.1+**

- **FFmpeg**

- **FFprobe**

- **Wget**

These need to be installed and added to the PATH.
Also, set the environment variables as shown in the scripts, or change these manually.
For TL, it's best to use environment variables.

We're also using **Twilio** for SMS notifications. Install via PIP.
Credentials can be retrieved by logging in to the Twilio dashboard.
Comment out or delete the relevant code if you don't want to use it.

-----
## rss_show 

for daily, full shows with a date

-----
## rss_segment 

for daily, short segments without a date
 

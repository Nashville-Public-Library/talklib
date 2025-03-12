import argparse
import os
import sys
import xml.etree.ElementTree as ET

from talklib.pod import SSH, Notifications

def parse_args():
    parser = argparse.ArgumentParser(description="use talklib in the terminal")

    feed_template_help = "Generate an RSS feed template in the current directory"
    parser.add_argument('--feed-template', action='store_true', help=feed_template_help, required=False)

    new_podcast_directory_help = "Creates a new podcast directory on the server with the value you pass in. \
        You MUST have an RSS feed (feed.xml) and logo (image.jpg) in the current directory."
    parser.add_argument('--new-pod-dir', type=str, help=new_podcast_directory_help, required=False)

    download_feed_help:str = "Download the RSS feed from the folder on the server you specify."
    parser.add_argument('--download-feed', type=str, help=download_feed_help, required=False)

    upload_feed_help:str = "Upload the RSS feed to the folder on the server you specify."
    parser.add_argument('--upload-feed', type=str, help=upload_feed_help, required=False)

    args = parser.parse_args()
    return args

def get_SSH():
    Notifications.prefix = "talklib CLI"
    notifications = Notifications()
    notifications.notify.email_enable = False
    ssh = SSH(notifications=notifications)
    return ssh

def download_feed(name: str):
    ssh = get_SSH()
    ssh.get_feed_from_folder(folder=name)

def upload_feed(name:str):
    if not os.path.isfile("feed.xml"):
        return print(f"cannot find 'feed.xml' in {os.getcwd()}. You must have this file in the current directory.")
    ssh = get_SSH()
    ssh.upload_feed_to_folder(folder=name)

def generate_feed_template():
    ET.register_namespace(prefix="atom", uri="http://www.w3.org/2005/Atom")
    ET.register_namespace(prefix="itunes", uri="http://www.itunes.com/dtds/podcast-1.0.dtd")
    feed = ET.fromstring(feed_template)
    tree = ET.ElementTree(feed)
    tree.write("feed.xml", encoding="utf-8", xml_declaration=True)
    # feed.write("feed.xml", encoding="utf-8", xml_declaration=True)
    print("'feed.xml' file created in " + os.getcwd())
    return

def new_podcast_dir(name: str):
    if not os.path.isfile("feed.xml"):
        return print(f"cannot find 'feed.xml' in {os.getcwd()}. You must have this file in the current directory.")

    if not os.path.isfile("image.jpg"):
        return print(f"cannot find 'image.jpg' in {os.getcwd()}. You must have this file in the current directory.")

    print("generating new podcast directory called " + name)

    ssh = get_SSH()
    ssh.make_new_folder(folder=name)
    ssh.upload_file(file="feed.xml", folder=name)
    ssh.upload_file(file="image.jpg", folder=name)

    print("done! you can now delete the local copies of the files")
    return

def main():
    if len(sys.argv) == 1: # if no arguments are passed
        return print("talklib -h for help")
    args = parse_args()

    if args.feed_template:
        return generate_feed_template()
    if args.new_pod_dir:
        return new_podcast_dir(name=args.new_pod_dir)
    if args.download_feed:
        return download_feed(name=args.download_feed)
    if args.upload_feed:
        return upload_feed(name=args.upload_feed)

feed_template: str = """
<rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
  <channel>
    <title>!!CHANGEME!!</title>
    <link>http://nashvilletalkinglibrary.org/</link>
    <atom:link href="https://assets.library.nashville.org/talkinglibrary/shows/!!CHANGEME!!/feed.xml" rel="self" type="application/rss+xml" />
    <description>
    !!CHANGEME!!
    </description>
    <copyright>© 1975-2022 Nashville Talking Library - Do not copy or redistribute</copyright>
    <docs>https://cyber.harvard.edu/rss/rss.html</docs>
    <generator>NTL Python Magic</generator>
    <webMaster>nashvilletalkinglibrary@gmail.com (Darth Vader)</webMaster>
    <itunes:owner>
      <itunes:name>Nashville Talking Library</itunes:name>
      <itunes:email>ntl@nashville.gov</itunes:email>
    </itunes:owner>
    <itunes:category text="Education" />
    <itunes:explicit>true</itunes:explicit>
    <itunes:image href="https://assets.library.nashville.org/talkinglibrary/shows/!!CHANGEME!!/image.jpg" />
    <image>
      <url>https://assets.library.nashville.org/talkinglibrary/shows/!!CHANGEME!!/image.jpg</url>
      <title>!!CHANGEME!!</title>
      <link>http://nashvilletalkinglibrary.org/</link>
    </image>
    <language>en</language>
    <lastBuildDate>leave me alone</lastBuildDate>
  </channel>
</rss>
"""
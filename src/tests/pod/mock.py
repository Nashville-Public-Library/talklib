import xml.etree.ElementTree as ET
import os
import requests


'''
We need to test 'local' files - meaning files we already have downloaded. But we don't want
to have to put an audio file into Git. So we're using this static URL to download first,
to mock a local file. Downloading the file itself it just setting up the test.

This static link was chosen because it's reliably available and the file is small/short.
'''
permalink = "http://www.newsservice.org/LatestNC.php?ncd=MzksMzcwLDI="

def mock_destinations():
    destination = 'dest1'
    if not os.path.exists(destination):
            os.mkdir(destination)
    return destination

env_vars = {
        'destinations': mock_destinations(),
        'syslog_server': '10.10.10.10',
        'fromEmail': 'mocked_value2',
        'toEmail': 'mocked_value2',
        'mail_server_external': 'mocked_value2',
        'twilio_sid': 'mocked_value2',
        'twilio_token': 'mocked_value2',
        'twilio_from': 'mocked_value2',
        'twilio_to': 'mocked_value2',
        'icecast_user': 'mahhhh',
        'icecast_pass': 'mahhhhh',
        'pod_server_uname': 'mahhhhh'
    }

    
def download_test_file(filename: str = 'input.mp3'):
    downloaded_file = filename
    file_exists = os.path.isfile(filename)
    if not file_exists:
        with open (filename, mode='wb') as downloaded_file:
            a = requests.get(permalink)
            downloaded_file.write(a.content)
            downloaded_file.close()
            return downloaded_file.name

    return downloaded_file

mock_feed = """
<rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
  <channel>
    <title>Mock Title</title>
    <link>http://nashvilletalkinglibrary.org/</link>
    <atom:link href="http://someURL/shows/wsj/feed.xml" rel="self" type="application/rss+xml" />
    <description>
    Mock feed file. Does not exist. Why are you reading this? 
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
    <itunes:image href="http://someURL/shows/wsj/image.jpg" />
    <image>
      <url>http://someURL/shows/wsj/image.jpg</url>
      <title>Wall Street Journal</title>
      <link>http://nashvilletalkinglibrary.org/</link>
    </image>
    <language>en</language>
    <lastBuildDate>Wed, 15 Jan 2025 15:02:49 -0600</lastBuildDate>
    <item>
        <title>Mock Title 011525</title>
    </item>
  </channel>
</rss>
"""

def write_mock_feed():
    ET.register_namespace(prefix="atom", uri="http://www.w3.org/2005/Atom")
    ET.register_namespace(prefix="itunes", uri="http://www.itunes.com/dtds/podcast-1.0.dtd")
    tree = ET.fromstring(mock_feed)
    ET.ElementTree(tree).write("mock.xml", encoding="UTF-8", xml_declaration=True)
    return "mock.xml"

mock_feed_no_items = """
<rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
  <channel>
    <title>Mock Title</title>
    <link>http://nashvilletalkinglibrary.org/</link>
    <atom:link href="http://someURL/shows/wsj/feed.xml" rel="self" type="application/rss+xml" />
    <description>
    Mock feed file. Does not exist. Why are you reading this? 
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
    <itunes:image href="http://someURL/shows/wsj/image.jpg" />
    <image>
      <url>http://someURL/shows/wsj/image.jpg</url>
      <title>Wall Street Journal</title>
      <link>http://nashvilletalkinglibrary.org/</link>
    </image>
    <language>en</language>
    <lastBuildDate>Wed, 15 Jan 2025 15:02:49 -0600</lastBuildDate>
  </channel>
</rss>
"""

def write_mock_feed_no_items():
    ET.register_namespace(prefix="atom", uri="http://www.w3.org/2005/Atom")
    ET.register_namespace(prefix="itunes", uri="http://www.itunes.com/dtds/podcast-1.0.dtd")
    tree = ET.fromstring(mock_feed_no_items)
    ET.ElementTree(tree).write("mock_no_items.xml", encoding="UTF-8", xml_declaration=True)
    return "mock_no_items.xml"
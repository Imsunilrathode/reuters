"""
Readme
==========
Get URL's from webpage
======================

This programe aims to parse the reuters datewise url data, fetch article_url and download all
URL's mentioned in webpage except VIDEOS to local drive.

COMMAND LINE EXECUTION EXAMPLE:
===============================
C:\Users>python <URL> <DEST_PATH> <COUNT> <BATCH_SIZE> <PAUSE_TIME>

Downloading Completed
-----------------------------------------
Saving Stdout print statements
C:\Users\Sunil>python geturl_reuters.py http://www.reuters.com/resources/archive/us/20071223.html F://HTML/ 10 2 15
"""

import sys
from time import sleep
import urllib
import urllib2
import random
from bs4 import BeautifulSoup

url = sys.argv[1]  # URL which needed to be parsed stored in variable url.
output_path = sys.argv[2]  # Destination path to store downloaded html pages.
count = int(sys.argv[3])  # Number of news articles to be downloaded.
batch = int(sys.argv[4])  # Batch size of urls to be downloaded in each interval
pause_time = int(sys.argv[5])  # Sleep time in between each batch downloading

# Request page url and read the data.
req_url = urllib2.Request(url)
open_url = urllib2.urlopen(req_url)
fchData = open_url.read()
soup = BeautifulSoup(fchData, "lxml")


# Find all <loc> tags to fetch article urls.
article_head = soup.find('div' , {'class' : 'module'})

article_url = article_head.find_all('div' , {'class' : 'headlineMed'})
url_list = []
for a in range(0,len(article_url)):
    b = article_url[a].find('a',href = True)
    url_list.append(b['href'])

#
print >>sys.stdout, len(url_list), " articles to be retrieved."

for i in range(min(count,len(url_list))):
    #Condition to exit program if count is greater than article count in the URL.

    print >> sys.stdout, str(url_list[i])
#         continue
    # Filepath to define its arctile file name and destination path.
    filePath = output_path+"//" + str(url_list[i].rsplit('/', 1)[1]) + '.html'
#
#     # retrive each article_url and save directly to filepath.
    try:
        urllib.urlretrieve(url_list[i], filePath)
    except:
        print >>sys.stdout, "[error] ", url_list[i]
#
    # Group URL's in batch size and pause for pause_time +- 10% secs.
    if (i+1) % batch == 0:
        pause_time = pause_time + random.randint(-int(pause_time*0.1), int(pause_time*0.1))
        sleep(pause_time)


print >> sys.stdout, "Downloading Completed"

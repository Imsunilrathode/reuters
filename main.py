"""
Readme
==========
Get URL's from reuters for each year from 2007 to 2017.
======================

This programe aims to parse the reuters webpage for each year and get url for each date,
 and pass the each_date URL to another program i.e. geturl_reuters.py where program will fetch article_url and download all
URL's mentioned in webpage except VIDEOS to local drive.

This program will generate logfile for each date url.

COMMAND LINE EXECUTION EXAMPLE:
===============================
C:\Users>python <program_name> <URL> <DEST_PATH> <logfile_path> <COUNT> <BATCH_SIZE> <PAUSE_TIME> <from_year_month> <to_year_month>

Downloading Completed
-----------------------------------------
Saving Stdout print statements
C:\Users\Sunil>python main.py http://www.reuters.com/resources/archive/us/2017.html F://HTML F://logfile/ 10000 20 40 2014-05 2014-08
"""

import sys
import urllib2
import os
from datetime import datetime
from bs4 import BeautifulSoup

url = sys.argv[1]  # URL which needed to be parsed stored in variable url.
output_path = sys.argv[2]  # Destination path to store downloaded html pages.
log_path = sys.argv[3]      # Log file path to store print statements
count = int(sys.argv[4])  # Number of news articles to be downloaded.
batch = int(sys.argv[5])  # Batch size of urls to be downloaded in each interval
pause_time = int(sys.argv[6])  # Sleep time in between each batch downloading
from_date = sys.argv[7]    # Year and month from where sitemap to be downloaded
to_date = sys.argv[8]      # Year  and month till where sitemap to be downloaded


# Read from_date and to_date as string and convert into datetime format
fd = datetime.strptime(from_date,'%Y-%m') # fd is from_date in datetime format
td = datetime.strptime(to_date,'%Y-%m') # td is to_date in datetime format

# Request page url and read the data.
# change the years based on required years.
year_url_list = [url[:-9]+str(x)+".html" for x in range(2015,2019)]
print(year_url_list)
# Iter through each year_url_list
for each in year_url_list:

    req_url = urllib2.Request(each)
    open_url = urllib2.urlopen(req_url)
    fchData = open_url.read()
    soup = BeautifulSoup(fchData, "lxml")


    get_html = soup.find('div' , {'class' : 'moduleBody'})
    if get_html is None:
        exit()
    each_date_url = get_html.find_all('p')
    url_list = []

    for x in range(0,len(each_date_url)):
        b = each_date_url[x].find_all('a',href = True)
        for e in range(0,len(b)):
            url_list.append(b[e]['href'])



    for i in range(0,len(url_list)):
        year_month = str(url_list[i].rsplit('/', 1)[-1])[:-7]
        y = year_month[:4]
        m = year_month[4:]
        folder_name = y+"-"+m
        d = datetime.strptime(y+"-"+m,'%Y-%m')

        if(d >= fd and d <= td):

            try:
                date_url = "http://www.reuters.com"+str(url_list[i])
                print("Started downloading "+date_url)
                folder_name = url_list[i].rsplit('/', 1)[-1]
                filePath = output_path +"//" +str(folder_name[:-5])
                print(filePath)

                # create folder for each sitemap in filePath
                if not os.path.exists(filePath):
                    os.makedirs(filePath)

                # create log folder for each sitemap in log_path
                log_filePath = log_path + str(folder_name[:-5]) + '.log'


                geturl = "python2 geturl_reuters.py " + date_url + " " + filePath+" " + str(count) + " " + str(batch) + " " + str(pause_time)

                # Pass the arguments to connect geturl.py program through cmd and save log files in output.txt
                os.system(geturl +" > " +log_filePath+ ' -u')


            except:
                continue


print >> sys.stdout, "Downloading completed"

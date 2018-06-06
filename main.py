import datetime 
from rfeed import *
from bs4 import BeautifulSoup
import urllib2
import requests
import pickle
import os

def generate_feed( journal_Id ):

    response = urllib2.urlopen("https://www.readbyqxmd.com/journal/%s" % journal_Id)
    soup = BeautifulSoup(response.read(),'html5lib')
    journal_title = soup.find("div", class_="subheader_list").find("h1").text
    journal_desc = journal_title
    journal_link = ""
    output_file = "/var/www/html/%s.rss.xml" % journal_title.replace(" ","")
    if os.path.isfile("%s.pk" % output_file):
        with open("%s.pk" % output_file, "r") as handle:
            records = pickle.load(handle)
    else:
        records = set()

    print "Processding Journal : %s" % journal_title

    items = []

    for page in range(1,6):

        data = {
        "ajax": "journal",
        "type": "journal",
        "page": str(page),
        "list_id": str(journal_Id),
        "end_date":"" 
        }

        r = requests.post('https://www.readbyqxmd.com/cgi-bin/web.pl', data = data)
        soup = BeautifulSoup(r.text,'html5lib')


        for res in soup.find_all("div", class_="rbox_inner"):
            link = "https://www.readbyqxmd.com"+res.find_all('a', class_='atl')[0]['href']+'/pubmed'
            paper_id = link.split("/")[-2]
            if paper_id in records:
                break
            else:
                records.add(paper_id)
            title = res.find_all('a', class_='atl')[0].text
            author = res.find_all('div', class_='small txt_999 ln15 p10bo')[0].text
            abstract = res.find_all('div', class_='ln15 p10bo')[0].text

            if "No abstract" in abstract:
                continue

            items.append( Item(
                title = title,
                link = link,
                description = abstract,
                guid = Guid(link),
                author = author,
                pubDate = datetime.datetime.now()
            ) )

        feed = Feed(
        title = journal_title,
        link = "http://bioinfo.life.hust.edu.cn",
        description = journal_desc,
        language = "en-US",
        lastBuildDate = datetime.datetime.now(),
        items = items)

    with open(output_file, "w") as f:
        f.write(feed.rss())
    with open("%s.pk" % output_file, "w") as handle:
        pickle.dump(records, handle)

if __name__ == '__main__':
    journal_list = [35114, 42959, 32413, 24515, 40701]
    for code in journal_list:
        generate_feed(code)
    

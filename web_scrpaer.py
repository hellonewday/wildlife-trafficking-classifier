import csv

import requests
import html2text
from bs4 import BeautifulSoup
from csv import writer

h = html2text.HTML2Text()
h.ignore_links = True

def getWebInfo(url):
    page = requests.get(url)
    html_code = page.content

    soup = BeautifulSoup(html_code, "html.parser")
    texts = soup.findAll("p", text=True)
    title = soup.findAll("h1", text=True)

    line = []
    content = ""
    titleLine = ""
    for el in texts[:-2]:
        content += el.getText().strip()

    for t in title:
        titleLine = t.getText().strip()

    line = [url, titleLine, content]

    return line


def collectUrls(url):

    page = requests.get(url)
    html_code = page.content

    soup = BeautifulSoup(html_code, "html.parser")
    links = soup.findAll("a", href=True)

    with open('data.csv', mode='a+', encoding="utf-8") as data_file:
        urlList = [];
        wr = writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,
                    lineterminator='\n')
        ## Add title
        wr.writerow(["Url", "Title", "Content"])
        for l in links:
            if (str(l.attrs["href"])[0] == "/" and len(str(l.attrs["href"])) > 40 and "http://" + url.split("/")[
                2] + str(
                l.attrs["href"]) not in urlList and str(l.attrs["href"]) != url):
                exUrl = "http://" + url.split("/")[2] + str(l.attrs["href"])
                urlList.append(exUrl)
                newLine = getWebInfo(exUrl)
                wr.writerow(newLine)


for i in range(1, 20):
    collectUrls(f"https://dantri.com.vn/tim-kiem/%C4%91%E1%BB%99ng+v%E1%BA%ADt.htm?pi={i}")
# collectUrls(
#     "http://www.hanoimoi.com.vn/tim-kiem?q=%C4%91%E1%BB%99ng%20v%E1%BA%ADt&type=title&category=0&media_type=0&latest=&date_format=year&page=1");


# data = getWebInfo("http://www.hanoimoi.com.vn/tin-tuc/Chuyen-la/1016358/dong-vat-thay-doi-hinh-dang-de-thich-nghi-voi-bien-doi-khi-hau");

# print(data)

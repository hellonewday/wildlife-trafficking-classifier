import csv
import regex as re
import requests
import html2text
from bs4 import BeautifulSoup
from csv import writer

h = html2text.HTML2Text()
h.ignore_links = True


def loaddicchar():
    dic = {}
    char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
        '|')
    charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
        '|')
    for i in range(len(char1252)):
        dic[char1252[i]] = charutf8[i]
    return dic


dicchar = loaddicchar()


def covert_unicode(txt):
    return re.sub(
        r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
        lambda x: dicchar[x.group()], txt)


def text_processing(sentence):
    sentence = covert_unicode(sentence)
    sentence = sentence.lower()
    sentence = re.sub(r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ_]', ' ', sentence)
    sentence = re.sub(r'\s+', ' ', sentence).strip()

    return sentence


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

    line = [url, titleLine if titleLine != "" else "nothing here",
            text_processing(content) if content != "" else "nothing here"]

    return line


def geth2WebInfo(url):
    page = requests.get(url)
    html_code = page.content

    soup = BeautifulSoup(html_code, "html.parser")
    texts = soup.findAll("p", text=True)
    title = soup.findAll("h2", text=True)

    line = []
    content = ""
    titleLine = ""
    for el in texts[:-2]:
        content += el.getText().strip()

    for t in title:
        titleLine = t.getText().strip()

    line = [url, titleLine if titleLine != "" else "nothing here",
            text_processing(content) if content != "" else "nothing here"]

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
        # wr.writerow(["Url", "Title", "Content"])
        for l in links:
            if (str(l.attrs["href"])[0] == "/" and len(str(l.attrs["href"])) > 40 and "https://" + url.split("/")[
                2] + str(
                l.attrs["href"]) not in urlList and str(l.attrs["href"]) != url):
                exUrl = "https://" + url.split("/")[2] + str(l.attrs["href"])
                urlList.append(exUrl)
                newLine = getWebInfo(exUrl)
                wr.writerow(newLine)


def collectFullUrls(url):
    page = requests.get(url)
    html_code = page.content
    soup = BeautifulSoup(html_code, "html.parser")
    links = soup.findAll("a", href=True)

    with open('data.csv', mode='a+', encoding="utf-8") as data_file:
        urlList = []
        wr = writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,
                    lineterminator='\n')
        ## Add title
        # wr.writerow(["Url", "Title", "Content"])
        for l in links:
            if len(str(l.attrs["href"])) > 60 and str(l.attrs["href"])[0] != "/" and str(
                    l.attrs["href"]) not in urlList:
                newLine = geth2WebInfo(str(l.attrs["href"]))
                urlList.append(str(l.attrs["href"]))
                wr.writerow(newLine)


# for i in range(21, 25):
#     collectFullUrls(f"https://thanhnien.vn/dong-vat-hoang-da/?trang={i}")
# for i in range(1, 4):
#     collectFullUrls(f"https://plo.vn/search/xJHhu5luZyB24bqtdCBob2FuZyBkw6M=/dong-vat-hoang-da.html?trang={i}")
# for i in range(1, 10):
#     collectUrls(f"https://cand.com.vn/article/PagingByTag?tagId=3768&pageSize=20&pageIndex={i}&displayView=PagingByTag")
# for i in range(1, 15):
#     collectUrls(f"https://dantri.com.vn/tim-kiem/%C4%91%E1%BB%99ng+v%E1%BA%ADt.htm?pi={i}")
for i in range(3, 41):
    print(i)
    collectUrls(f"https://vtc.vn/tieu-diem/dong-vat/trang-{i}.html")

# collectUrls(
#     "https://baotintuc.vn/tags/%C4%91%E1%BB%99ng+v%E1%BA%ADt+hoang+d%C3%A3.htm")

# data = getWebInfo("https://vov.vn/the-gioi/cuoc-song-do-day/te-giac-chau-phi-lam-nguy-vi-loi-don-vo-can-cu-dung
# -sung-chua-covid19-1078194.vov");

# print(data)

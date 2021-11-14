#
# document = "Việt Nam là một trong những quốc gia đa dạng về sinh học, do đó việc tìm ra các giải pháp nhằm bảo tồn đa dạng sinh học và chống buôn bán động vật hoang dã chính là chìa khóa để đạt được phát triển bền vững. Mỹ tự hào hỗ trợ các chương trình đa dạng sinh học và đối phó với nạn buôn bán động vật hoang dã và hợp tác cùng Việt Nam như một đối tác đáng tin cậy"
# document = 'Đơn vị cứu hộ vườn quốc gia Cúc Phương vừa tổ chức một "cầu" cứu hộ đặc biệt để đảm bảo phòng chống dịch Covid-19, đưa 4 cá thể Tê tê quý hiếm từ Bắc Kạn về chăm sóc, bảo tồn tại vườn'
# document = 'Thanh tra Chính phủ phát hiện UBND tỉnh Ninh Bình "nhầm lẫn về khái niệm đá nguyên khai", 3 doanh nghiệp sản xuất xi măng còn thiếu 32,5 tỷ đồng tiền thuế tài nguyên.'
# label = loaded_model.predict([document])
#
# print(label)
# #
import requests
import csv
import regex as re
import requests
import html2text
from bs4 import BeautifulSoup
import pickle
import regex as re

loaded_model = pickle.load(open("../api/models/finalized_model.sav", 'rb'))


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


def categorize(category):
    if category == 1:
        return "Illegal Wildlife Trafficking"
    else:
        return "Counter Wildlife Trafficking"

response = []
for i in range(1, 30):

    page = requests.get(
        f"https://dantri.com.vn/xa-hoi/moi-truong/trang-{i}.htm")
    #
    html_code = page.content
    soup = BeautifulSoup(html_code, "html.parser")

    links = soup.findAll("a", text=True)
    allLinks = []
    for l in links:
        if len(str(l.attrs["href"])) > 100 and str(l.attrs["href"])[0] == "/" and str(l.attrs["href"]) not in allLinks:
            allLinks.append(str(l.attrs["href"]))

    for i in range(len(allLinks)):
        page = requests.get("https://dantri.com.vn" + allLinks[i])
        html_code = page.content
        soup = BeautifulSoup(html_code, "html.parser")
        image = soup.select("figure > img")
        title = soup.findAll("h1", text=True)
        subtitle = soup.findAll("h2", text=True)
        paragraph = soup.findAll("p", text=True)
        datetime = soup.find_all("span", {"class": "dt-news__time"})
        author = soup.select("p > strong")
        content = ""
        for el in paragraph:
            content += el.getText().strip()
        content = text_processing(content)
        document = f"{title} {subtitle} {content}"
        label = loaded_model.predict([document])
        if label[0] != 0:
            # result = {
            #     "link": "https://dantri.com.vn" + allLinks[i],
            #     "image": image[0].attrs["src"],
            #     "title": title[0].getText().strip(),
            #     "subtitle": subtitle[0].getText().strip(),
            #     "date":  datetime[0].getText().strip(),
            #     "author": author[-1].getText().strip(),
            #     "category": categorize(label[0])
            # }
            # response.append(result)
            print("link: ", "https://dantri.com.vn" + allLinks[i])
            print("image: ", image[0].attrs["src"])
            print("title: ", title[0].getText().strip())
            print("subtitle: ", subtitle[0].getText().strip())
            print("date: ", datetime[0].getText().strip())
            print("author: ", author[-1].getText().strip())
            print("category: ", categorize(label[0]))

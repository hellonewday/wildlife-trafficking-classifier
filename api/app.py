# save this as app.py
from flask import Flask, jsonify, request
import pandas as pd
import json
from keras.models import Sequential, load_model
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from werkzeug.utils import secure_filename
import tensorflow as tf
import os
import numpy as np
import pickle
import requests
import csv
import html2text
from bs4 import BeautifulSoup
import regex as re
from flask_cors import CORS, cross_origin
import threading

app = Flask(__name__)
cors = CORS(app)

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
IMAGE_SIZE = (180, 180)
UPLOAD_FOLDER = 'tmp'
## Animal classfication model
model = load_model("models/image_model.h5")
## Paragraph classifier.
classifier = pickle.load(open("models/finalized_model.sav", 'rb'))


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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def predict(file):
    img = tf.keras.utils.load_img(
        file, target_size=(180, 180)
    )
    class_names = ['cavallo', 'elefante', 'farfalla', 'gallina', 'scoiattolo']
    img = tf.keras.utils.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    predictions = model.predict(img)
    score = tf.nn.softmax(predictions[0])
    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
            .format(class_names[np.argmax(score)], 100 * np.max(score))
    )
    output = {'Label:': class_names[np.argmax(score)], 'Precision': 100 * np.max(score)}
    return output


@app.route("/")
def hello():
    new = pd.read_csv('dataset.csv')
    jsonfiles = json.loads(new.to_json(orient='records'))
    return jsonify({"data": jsonfiles})


@app.route('/uploads', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join("tmp", filename)
            file.save(file_path)
            print(file_path)
            output = predict(file_path)
        return jsonify(output)
    else:
        return "Get something here"

@app.route("/gendata")
def runBackground():
    response = []
    for i in range(1, 20):
        page = requests.get(
            f"https://dantri.com.vn/xa-hoi/moi-truong/trang-{i}.htm")
        #
        html_code = page.content
        soup = BeautifulSoup(html_code, "html.parser")

        links = soup.findAll("a", text=True)
        allLinks = []
        for l in links:
            if len(str(l.attrs["href"])) > 100 and str(l.attrs["href"])[0] == "/" and str(
                    l.attrs["href"]) not in allLinks:
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
            label = classifier.predict([document])
            if label != 0:
                result = {
                    "link": "https://dantri.com.vn" + allLinks[i],
                    "image": image[0].attrs["src"],
                    "title": title[0].getText().strip(),
                    "subtitle": subtitle[0].getText().strip(),
                    "date": datetime[0].getText().strip(),
                    "author": author[-1].getText().strip(),
                    "category": categorize(label[0])
                }
                response.append(result)
    jsonFile = {"counts": len(response), "data": response}
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(jsonFile, f, ensure_ascii=False, indent=4)
    print(f"Complete. Found {len(response)} news.")
    return jsonify(jsonFile)




@app.route("/crawler")
def crawler():
    f = open('data.json', encoding="utf8")
    data = json.load(f)

    return jsonify(data)

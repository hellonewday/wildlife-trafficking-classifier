import pandas as pd
from flashtext.keyword import KeywordProcessor

data = pd.read_csv("data.csv", delimiter=",")

## Keyword cho những tin tức vi pham động vật hoang dã
Violate_Keywords = ["buôn bán", "bắt giữ", "động vật hoang dã", "chết", "rruy tố", "Vi phạm", "phạt tù",
                    "phạt tiền", "tù",
                    "tích trữ",
                    "tàng trữ",
                    "cò tặc",
                    "Phi tang",
                    "nội tạng"]

## Keyword cho những tin tức bảo tồn động vật

Observation_Keywords = ["cứu chữa", "Bảo tồn", "giúp đỡ", "hỗ trợ", "khỏe mạnh", "động vật", "thú nuôi",
                        "đẹp", "tuyệt vời", "cứu hộ", "cơ sở bảo tồn", "trung tâm cứu trợ", "sinh thái", "cộng đồng"]

## Keyword cho những chính sách của chính phủ

Rule_Keywords = ["Chỉ thị", "Chính phủ", "Bảo vệ động vật hoang dã", "Chính sách", "Quy định",
                 "Quy luật"]

keywords = Violate_Keywords + Observation_Keywords + Rule_Keywords

kp0 = KeywordProcessor()
for word in keywords:
    kp0.add_keyword(word)

kp1 = KeywordProcessor()
for word in Violate_Keywords:
    kp1.add_keyword(word)

kp2 = KeywordProcessor()
for word in Observation_Keywords:
    kp2.add_keyword(word)

kp3 = KeywordProcessor()
for word in Rule_Keywords:
    kp3.add_keyword(word)


def percentage1(dum0, dumx):
    try:
        ans = float(dumx) / float(dum0)
        ans = ans * 100
    except:
        return 0
    else:
        return ans


def find_class(sample):
    y0 = len(kp0.extract_keywords(sample))
    y1 = len(kp1.extract_keywords(sample))
    y2 = len(kp2.extract_keywords(sample))
    y3 = len(kp3.extract_keywords(sample))

    total_matches = y0
    per1 = float(percentage1(y0, y1))
    per2 = float(percentage1(y0, y2))
    per3 = float(percentage1(y0, y3))

    if (y0 == 0):
        category = 0
    else:
        if per1 >= per2 and per1 >= per3:
            category = 1
        elif per2 >= per3 and per2 >= per1:
            category = 2
        elif per3 >= per1 and per3 >= per2:
            category = 3
    return category


categories = []
for i in range(data.shape[0]):
    categories.append(find_class(data.iloc[i]["Content"]))

data["category"] = categories

df = pd.DataFrame(data)

df.to_csv("dataset.csv")

import pandas as pd
from flashtext.keyword import KeywordProcessor

data = pd.read_csv("data.csv", delimiter=",")

data = data[data['Content'] != "nothing here"]

data = data[data["Content"].str.len() > 10]

data = data[data["Title"].str.len() > 10]

## Keyword cho những tin tức vi pham động vật hoang dã 6 words only
Violate_Keywords = ["buôn bán động vật", "săn bắt động vật", "vận chuyển trái phép ngà voi",
                    "vận chuyển trái phép tê tê", "ngược đãi", "cò tặc", "buôn bán", "săn bắt", "vận chuyển",
                    "buôn bán ngà voi",
                    "buôn bán tê tê", "săn bắt ngà voi", "buôn bán ngà voi", "ngược đãi động vật"]

## Keyword cho những tin tức bảo tồn động vật

Observation_Keywords = ["giải cứu động vật", "giải thoát", "giải cứu tê tê", "giải cứu tê giác", "cứu hộ tê tê",
                        "cứu hộ động vật",
                        "phòng chống",
                        "bảo tồn động vật hoang dã", "bảo tồn", "giải cứu", "cứu hộ", "bảo vệ",
                        "bảo tồn tê tê", "bảo tồn tê giác", "bảo vệ động vật hoang dã", "bảo vệ tê tê", "bảo vệ hổ"]

keywords = Violate_Keywords + Observation_Keywords

kp0 = KeywordProcessor()
for word in keywords:
    kp0.add_keyword(word)

kp1 = KeywordProcessor()
for word in Violate_Keywords:
    kp1.add_keyword(word)

kp2 = KeywordProcessor()
for word in Observation_Keywords:
    kp2.add_keyword(word)


def percentage1(dum0, dumx):
    try:
        ans = float(dumx) / float(dum0)
        ans = ans * 100
    except:
        return 0
    else:
        return ans


def find_class(sample):
    sample = sample.lower()
    y0 = len(kp0.extract_keywords(sample))
    y1 = len(kp1.extract_keywords(sample))
    y2 = len(kp2.extract_keywords(sample))

    per1 = float(percentage1(y0, y1))
    per2 = float(percentage1(y0, y2))

    if (y0 == 0):
        category = 0
    else:
        if per1 >= per2:
            category = 1
        elif per2 > per1:
            category = 2
    return category


categories = []
for i in range(data.shape[0]):
    categories.append(find_class(data.iloc[i]["Title"] + " " + data.iloc[i]["Content"]))

data["category"] = categories

df = pd.DataFrame(data)

df.to_csv("dataset.csv", index=False)

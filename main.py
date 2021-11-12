## Decision Tree
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
import sklearn.tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score
from sklearn.ensemble import RandomForestClassifier

data = pd.read_csv("san_fran_crime.csv", delimiter="\t")

data = pd.get_dummies(data, columns=["Category", 'PdDistrict'], drop_first=False)

train_data, test_data = train_test_split(data, random_state=2, test_size=0.1, shuffle=True);

features = [c for c in data.columns if c != "Resolution"]


def train_and_test_model(model):
    global features

    model.fit(train_data[features], train_data.Resolution)

    train_pred = model.predict(train_data[features])

    train_acc = balanced_accuracy_score(train_data.Resolution, train_pred)

    test_pred = model.predict(test_data[features])

    test_acc = balanced_accuracy_score(test_data.Resolution, test_pred)

    return train_acc, test_acc


# model = sklearn.tree.DecisionTreeClassifier(random_state=1, max_depth=10)
# train, test = train_and_test_model(model)
# print("Decision Tree:\n")
# print(train)
# print(test)
# estimtors = [2, 4, 6, 8, 10, 15, 20, 50, 100]
#
# for est in estimtors:
random_forest = RandomForestClassifier(
        n_estimators=10,
        random_state=2,
        # max_depth=est,
        criterion="gini",
        verbose=False)

train, test = train_and_test_model(random_forest)

print(train)
print(test)

random_forest = RandomForestClassifier(
        n_estimators=10,
        random_state=2,
        # max_depth=est,
        criterion="entropy",
        verbose=False)

train, test = train_and_test_model(random_forest)

print(train)
print(test)


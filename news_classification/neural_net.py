from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle
import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import time
import os

data = pd.read_csv("dataset.csv")
feature = ["Title", "Content"]
label = "category"

X_train, X_test, y_train, y_test = train_test_split(data[feature[0]] + " " + data[feature[1]], data[label],
                                                    test_size=0.2,
                                                    random_state=42)

start_time = time.time()
text_clf = Pipeline([('vect', CountVectorizer(ngram_range=(1, 1),
                                              max_df=0.8,
                                              max_features=None)),
                     ('tfidf', TfidfTransformer()),
                     ('clf', LogisticRegression(solver='lbfgs',
                                                multi_class='auto',
                                                max_iter=10000))
                     ])
text_clf = text_clf.fit(X_train, y_train)

train_time = time.time() - start_time
print('Done training Linear Classifier in', train_time, 'seconds.')

y_pred = text_clf.predict(X_test)

print(classification_report(y_test, y_pred, labels=[0, 1, 2]))

filename = '../api/models/finalized_model.sav'
pickle.dump(text_clf, open(filename, 'wb'))

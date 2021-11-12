import pandas as pd
import numpy as np
from underthesea import word_tokenize
from nltk.stem.lancaster import LancasterStemmer
import datetime
import time
import json

print("Read the file: ")
data = pd.read_csv("dataset.csv")

data = data[data["category"] != 0]

train_data = [];

print("Start preprocessing: ")
for index, row in data.iterrows():
    train_data.append({"category": row["category"], "sentence": row["Content"]})

words = []
classes = []
documents = []
ignore_words = ['?']

for pattern in train_data:
    w = word_tokenize(pattern["sentence"])
    words.extend(w)
    documents.append((w, pattern["category"]))
    if pattern["category"] not in classes:
        classes.append(pattern["category"])

words = [w.lower() for w in words if w not in ignore_words]
words = list(set(words))
classes = list(set(classes))

# training = []
# output = []
# output_empty = [0] * len(classes)
#
# for doc in documents:
#     bag = []
#     pattern_words = doc[0]
#
#     pattern_words = [word.lower() for word in pattern_words]
#
#     for w in words:
#         bag.append(1) if w in pattern_words else bag.append(0)
#     training.append(bag)
#     output_row = list(output_empty)
#     output_row[classes.index(doc[1])] = 1
#     output.append(output_row)

print("Done preprocessing!")


def derivative(x):
    return x * (1 - x)


def sigmoid(x):
    a = 1 / (1 + np.exp(-x))
    return derivative(a)


def clean_up_sentence(sentence):
    sentence_words = word_tokenize(sentence)
    return sentence_words


def bag_of_words(s, w):
    sentence_words = clean_up_sentence(s)
    bag = [0] * len(w)
    for sentence in sentence_words:
        for i, j in enumerate(w):
            if j == sentence:
                bag[i] = 1
    return np.array(bag)


def evaluate(sentence):
    x = bag_of_words(sentence.lower(), words)
    l0 = x
    l1 = sigmoid(np.dot(l0, s0))
    l2 = sigmoid(np.dot(l1, s1))
    return l2


def train(X, y, hidden_neurons=10, alpha=1, epochs=5000, dropout=False, dropout_percent=0.5):
    print("Training with %s neurons, alpha:%s, dropout:%s %s" % (
        hidden_neurons, str(alpha), dropout, dropout_percent if dropout else ''))
    print("Input matrix: %sx%s    Output matrix: %sx%s" % (len(X), len(X[0]), 1, len(classes)))

    np.random.seed(1)
    last_mean_error = 1
    s0 = 2 * np.random.random((len(X[0]), hidden_neurons)) - 1
    s1 = 2 * np.random.random((hidden_neurons, len(classes))) - 1
    prev_s0 = np.zeros_like(s0)
    prev_s1 = np.zeros_like(s1)

    s0_direction_count = np.zeros_like(s0)
    s1_direction_count = np.zeros_like(s1)

    for j in iter(range(epochs + 1)):
        print("Epoch ", j, " is starting to run...")
        layer_0 = X
        layer_1 = sigmoid(np.dot(layer_0, s0))
        if dropout:
            layer_1 *= np.random.binomial([np.ones((len(X), hidden_neurons))], 1 - dropout_percent)[0] * (
                    1.0 / (1 - dropout_percent))

        layer_2 = sigmoid(np.dot(layer_1, s1))
        layer_2_error = y - layer_2

        if j % 10000 == 0 and j > 5000:
            if np.mean(np.abs(layer_2_error)) > last_mean_error:
                last_mean_error = np.mean(np.abs(layer_2_error))
            else:
                break
        layer_2_delta = layer_2_error * derivative(layer_2)
        layer_1_error = layer_2_delta.dot(s1.T)
        layer_1_delta = layer_1_error * derivative(layer_1)
        prev_s1 = (layer_1.T.dot(layer_2_delta))
        prev_s0 = (layer_0.T.dot(layer_1_delta))

        if j > 0:
            s0_direction_count += np.abs(
                ((prev_s0 > 0) + 0) - ((prev_s0 > 0) + 0))
            s1_direction_count += np.abs(
                ((prev_s1 > 0) + 0) - ((prev_s1 > 0) + 0))
        print("Epoch ", j, " is starting to run...")
    now = datetime.datetime.now()
    res = {'synapse0': s0.tolist(), 'synapse1': s1.tolist(),
           'datetime': now.strftime("%Y-%m-%d %H:%M"),
           'words': words,
           'classes': classes
           }
    result_file = "result.json"
    with open(result_file, 'w') as outfile:
        json.dump(res, outfile, indent=2, sort_keys=True)
    print("saved synapses to:", result_file)


# print("Preparing data")
# X = np.array(training)
# y = np.array(output)
# start_time = time.time()
#
# print("Start training")
# train(X, y, hidden_neurons=10, alpha=0.1, epochs=50000, dropout=False, dropout_percent=0.2)
# elapse_time = time.time() - start_time
# print("processing time: ", elapse_time, " seconds")

labels = [1, 2, 3]
## Testing
error_threshold = 0.2
with open("result.json") as data_file:
    s = json.load(data_file)
    s0 = np.asarray(s['synapse0'])
    s1 = np.asarray(s['synapse1'])


def classify(sentence):
    results = evaluate(sentence)
    results = [[i, r] for i, r in enumerate(results) if r > error_threshold]
    results.sort(key=lambda x: x[1], reverse=True)
    return_results = [[labels[r[0]], r[1]] for r in results]
    print("\n classification: %s" % return_results)


print("Test with data....")
classify(data.iloc[120]["Content"].values[0])

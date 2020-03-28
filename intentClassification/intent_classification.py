import nltk
import random
import collections
import pandas as pd
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.metrics import *
from config import domains

nltk.download()

# Init the Wordnet Lemmatizer
lemmatizer = WordNetLemmatizer()

data = {}
for domain in domains:
    file_data = pd.read_json('files/' + domain + '.json')
    data[domain] = file_data['text'].to_numpy()

"""Getting the words from the data"""

all_words = []

document = [(text, category)
            for category in data.keys()
            for text in data[category]]
random.shuffle(document)

array_words = [nltk.word_tokenize(w) for (w, cat) in document]
flat_list = [word for sent in array_words for word in sent]

"""Removes the **stop words** like ( ‘off’, ‘is’, ‘s’, ‘am’, ‘or’) and
  ***non alphabetical*** characters"""

stopWords = set(stopwords.words('english'))


def remove_stop_words(words):
    words_filtered = []

    for w in words:
        if w not in stopWords:
            if w.isalpha():
                words_filtered.append(w)

    return words_filtered


flat_list = remove_stop_words(flat_list)

"""**Lemmatization** i.e., tranforms different
            forms of words to a single one"""


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


def lemmatization(words):
    return [lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in words]


filtered_list = lemmatization(flat_list)

"""Getting the ***frequency*** of each word and extracting top 2000"""

frequencyDistribution = nltk.FreqDist(w.lower() for w in filtered_list)
word_features = list(frequencyDistribution)[:2000]

"""**FEATURE** **EXTRACTION**"""


def feature_extraction(doc):
    document_words = [word.lower() for word in nltk.word_tokenize(doc)]

    document_words = remove_stop_words(document_words)
    document_words = lemmatization(document_words)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features


"""Training the model"""

test_set = nltk.classify.apply_features(feature_extraction, document[:500])
train_set = nltk.classify.apply_features(feature_extraction, document[500:])
classifier = nltk.NaiveBayesClassifier.train(train_set)

"""Testing the model *accuracy*"""

print('Accuracy:', nltk.classify.accuracy(classifier, test_set))

classifier.show_most_informative_features(20)

"""Measuring **Precision,Recall,F-Measure** of a classifier.
  Finding **Confusion matrix**"""

actual_set = collections.defaultdict(set)
predicted_set = collections.defaultdict(set)
# cm here refers to confusion matrix
actual_set_cm = []
predicted_set_cm = []

for i, (feature, label) in enumerate(test_set):
    actual_set[label].add(i)
    actual_set_cm.append(label)
    predicted_label = classifier.classify(feature)
    predicted_set[predicted_label].add(i)
    predicted_set_cm.append(predicted_label)

for category in data.keys():
    print(category, 'precision :',
          precision(actual_set[category], predicted_set[category]))
    print(category, 'recall :',
          recall(actual_set[category], predicted_set[category]))
    print(category, 'f-measure :',
          f_measure(actual_set[category], predicted_set[category]))

confusion_matrix = ConfusionMatrix(actual_set_cm, predicted_set_cm)
print('Confusion Matrix')
print(confusion_matrix)

"""**OUTPUTS**"""

print('Intent Classification Outputs')
print("Is it sunnier today? ->",
      classifier.classify(feature_extraction("Is it sunnier today?")))
print("book a table ->",
      classifier.classify(feature_extraction("book a table")))
print("I want to listen to popular telugu song ->",
      classifier.classify(feature_extraction(
          " I want to listen to popular telugu song ")))

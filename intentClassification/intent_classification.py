import operator

import nltk
import random
import collections
import pandas as pd
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.metrics import precision, recall, f_measure, ConfusionMatrix
from config import domains

nltk.download()


class IntentClassification:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.data = {}
        self.document = []
        self.flat_list = []

        self.read_files()

        """Getting the words from the data"""
        self.get_words()
        """Removes the **stop words** like ( ‘off’, ‘is’, ‘s’, ‘am’, ‘or’) and
               ***non alphabetical*** characters"""
        self.flat_list = self.remove_stop_words(self.flat_list)

        """**Lemmatization** i.e., tranforms different
                forms of words to a single one"""
        filtered_list = self.lemmatization(self.flat_list)

        """Getting the ***frequency*** of each word and extracting top 2000"""

        frequency_distribution = nltk.FreqDist(w.lower()
                                               for w in filtered_list)

        self.word_features = list(frequency_distribution)[:2000]

        """Training the model"""

        self.test_set = nltk.classify.apply_features(
            self.feature_extraction, self.document[:500])
        self.train_set = nltk.classify.apply_features(
            self.feature_extraction, self.document[500:])
        self.classifier = nltk.NaiveBayesClassifier.train(self.train_set)

    def read_files(self):
        for domain in domains:
            file_data = pd.read_json(
                'intentClassification/files/'+domain+'.json')
            self.data[domain] = file_data['text'].to_numpy()

    def get_words(self):
        self.document = [(text, category)
                         for category in self.data.keys()
                         for text in self.data[category]]

        random.shuffle(self.document)
        array_words = [nltk.word_tokenize(w) for (w, cat) in self.document]
        self.flat_list = [word for sent in array_words for word in sent]

    def remove_stop_words(self, words):
        stop_words = set(stopwords.words('english'))

        words_filtered = []

        for w in words:
            if w not in stop_words:
                if w.isalpha():
                    words_filtered.append(w)

        return words_filtered

    def get_wordnet_pos(self, word):
        """Map POS tag to first character lemmatize() accepts"""
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}

        return tag_dict.get(tag,
                            wordnet.NOUN)

    def lemmatization(self, words):
        return [self.lemmatizer.lemmatize(w,
                                          self.get_wordnet_pos(w))
                for w in words]

    def feature_extraction(self, doc):
        document_words = [word.lower() for word in nltk.word_tokenize(doc)]

        document_words = self.remove_stop_words(document_words)
        document_words = self.lemmatization(document_words)
        features = {}
        for word in self.word_features:
            if word in document_words:
                features['contains({})'.format(word)] = (
                    word in document_words)
        return features

    def measuring_accuracy(self):
        """Testing the model *accuracy*"""
        print('Accuracy:',
              nltk.classify.accuracy(self.classifier, self.test_set))
        self.classifier.show_most_informative_features(20)
        """Measuring **Precision,Recall,F-Measure** of a classifier.
             Finding **Confusion matrix**"""
        actual_set = collections.defaultdict(set)
        predicted_set = collections.defaultdict(set)
        # cm here refers to confusion matrix
        actual_set_cm = []
        predicted_set_cm = []
        for i, (feature, label) in enumerate(self.test_set):
            actual_set[label].add(i)
            actual_set_cm.append(label)
            predicted_label = self.classifier.classify(feature)
            predicted_set[predicted_label].add(i)
            predicted_set_cm.append(predicted_label)

        for category in self.data.keys():
            print(category, 'precision :',
                  precision(actual_set[category], predicted_set[category]))
            print(category, 'recall :',
                  recall(actual_set[category], predicted_set[category]))
            print(category, 'f-measure :',
                  f_measure(actual_set[category], predicted_set[category]))
        confusion_matrix = ConfusionMatrix(actual_set_cm, predicted_set_cm)
        print('Confusion Matrix')
        print(confusion_matrix)

    def intent_identifier(self, text):
        dist = self.classifier.prob_classify(self.feature_extraction(text))
        first_label = next(iter(dist.samples()))
        all_equal = all(round(dist.prob(label), 1) ==
                        round(dist.prob(first_label), 1)
                        for label in dist.samples())
        if all_equal:
            return None
        else:
            return max([(label, dist.prob(label)) for label in dist.samples()],
                       key=operator.itemgetter(1))[0]

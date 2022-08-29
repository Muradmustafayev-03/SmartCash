from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from Parsers.extract_title import quantity_markers
from dataset_builder import SimpleDatasetBuilder


class Classifier:
    def __init__(self):
        self.dataset_builder = SimpleDatasetBuilder()
        self.x_train, self.x_test, self.y_train, self.y_test = self.dataset_builder.get_split()
        self.vectorizer = CountVectorizer(stop_words=quantity_markers,
                                          ngram_range=(1, 3),
                                          analyzer='word')

    def train(self):
        x_train_vectorized = self.vectorizer.fit_transform(self.x_train)
        nb_classifier = MultinomialNB().fit(x_train_vectorized, self.y_train)
        return nb_classifier

    def predict(self):
        pass

    def save_to_file(self):
        pass

    def read_from_file(self):
        pass

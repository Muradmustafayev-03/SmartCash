import pickle
from sklearn import metrics
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
        self.model = self.train()

    def train(self):
        x_train_vectorized = self.vectorizer.fit_transform(self.x_train)
        nb_classifier = MultinomialNB().fit(x_train_vectorized, self.y_train)
        return nb_classifier

    def predict(self):
        x_test_vectorized = self.vectorizer.transform(self.x_test)
        return self.model.predict(x_test_vectorized)

    def test(self):
        y_pred = self.predict()

        precision = metrics.precision_score(self.y_test, y_pred)
        recall = metrics.recall_score(self.y_test, y_pred)
        f1 = metrics.f1_score(self.y_test, y_pred)

        return precision, recall, f1

    def save_to_file(self, filename='category_classifier'):
        path = '/models/' + filename + '.pkl'
        pickle.dump(self.model, open(path, 'wb'))

    def read_from_file(self, filename='category_classifier'):
        path = '/models/' + filename + '.pkl'
        self.model = pickle.load(open(path, 'wb'))

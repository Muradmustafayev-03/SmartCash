import pickle
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from Parsers.extract_title import quantity_markers
from .dataset_builder import SimpleDatasetBuilder


class SimpleClassifier:
    def __init__(self, split=0.8):
        self.dataset_builder = SimpleDatasetBuilder()
        self.x_train, self.x_test, self.y_train, self.y_test = self.dataset_builder.get_split(split)
        self.y_train = [y[0] for y in self.y_train]
        self.y_test = [y[0] for y in self.y_test]
        self.vectorizer = CountVectorizer(stop_words=quantity_markers,
                                          ngram_range=(1, 3),
                                          analyzer='word')
        self.model = LinearSVC()

    def train(self):
        x_train_vectorized = self.vectorizer.fit_transform(self.x_train)
        model = self.model.fit(x_train_vectorized, self.y_train)
        self.model = model
        return model

    def predict(self):
        x_test_vectorized = self.vectorizer.transform(self.x_test)
        return self.model.predict(x_test_vectorized)

    def test(self):
        y_pred = self.predict()

        precision = metrics.precision_score(self.y_test, y_pred, average='micro')
        recall = metrics.recall_score(self.y_test, y_pred, average='micro')
        f1 = metrics.f1_score(self.y_test, y_pred, average='micro')

        return precision, recall, f1

    def save_to_file(self, filename='category_classifier'):
        path = '/models/' + filename + '.pkl'
        pickle.dump(self.model, open(path, 'wb'))

    def read_from_file(self, filename='category_classifier'):
        path = '/models/' + filename + '.pkl'
        self.model = pickle.load(open(path, 'wb'))

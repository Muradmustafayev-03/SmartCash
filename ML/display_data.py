from PurchasesData.models import Category
from Parsers.extract_title import quantity_markers
import nltk

nltk.download('punkt')


def print_frequency_distribution():
    for category in Category.objects.all():
        tokens = nltk.word_tokenize(' '.join([' '.join([product.title, product.manufacturer, product.description])
                                              for product in category.product_set.all()]))
        tokens = [word for word in tokens if word not in quantity_markers]

        fd = nltk.FreqDist(tokens)
        print(category)
        print(fd.most_common(20))

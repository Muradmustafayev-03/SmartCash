from PurchasesData.models import Category, Product
import random


class DatasetBuilder:
    def __init__(self):
        self.products_list = self.get_products_list()
        self.dataset = self.get_dataset_from_db()
        self.path = 'ML/dataset/'

    def get_products_list(self):
        self.products_list = Product.objects.exclude(categories=None)
        return Product.objects.exclude(categories=None)

    def get_split(self):
        size = len(self.dataset)

        x_train, x_test, y_train, y_test = [], [], [], []

        pivot = int(0.8 * size)

        for i in range(0, pivot):
            x_train.append(self.dataset[i][0])
            y_train.append(self.dataset[i][1])
        for i in range(pivot, size):
            x_test.append(self.dataset[i][0])
            y_test.append(self.dataset[i][1])

        return x_train, x_test, y_train, y_test

    def get_dataset(self):
        pass

    def get_dataset_from_db(self):
        return []

    def get_dataset_from_file(self, filename):
        dataset = []
        with open(self.path + filename + 'csv', 'r', encoding='utf-8') as file:
            line = file.read().split(',')
            dataset.append([', '.join(line[:3]), line[3:]])


class SimpleDatasetBuilder(DatasetBuilder):
    def get_dataset_from_db(self):
        """
        :return: dataset list
        """
        dataset = []
        for product in self.products_list:
            categories = product.categories.all()

            dataset.append([f'{product.title}, {product.manufacturer}, {product.description}',
                            [categories[len(categories) - 1].title]])

        random.shuffle(dataset)
        return dataset

    def save_dataset(self, filename: str):
        """
        writes the dataset into csv file
        """

        with open(self.path + filename + 'csv', 'w', encoding='utf-8') as file:
            # first row is label
            file.write('Title, Manufacturer, Description, Main Category')
            for entry in self.dataset:
                file.write(f'{entry[0]}, {entry[1]}, {entry[2]}, {entry[3]}\n')


class ComplexDatasetBuilder(DatasetBuilder):
    categories_list: list

    def __init__(self):
        super().__init__()
        self.get_categories_list()

    def get_categories_list(self):
        self.categories_list = Category.objects.all()

    def get_dataset_from_db(self):
        """
        :return: dataset list
        """
        dataset = []

        for product in self.products_list:
            row_x = f'{product.title}, {product.manufacturer}, {product.description}'
            row_y = []

            for category in self.categories_list:
                if category in product.categories.all():
                    row_y.append(1)
                else:
                    row_y.append(0)

            dataset.append([row_x, row_y])

        random.shuffle(dataset)
        self.dataset = dataset
        return dataset

    def save_dataset(self, filename: str):
        """
        writes dataset into csv file
        """
        with open(self.path + filename + 'csv', 'w', encoding='utf-8') as file:
            # first row as label
            file.write('Title, Manufacturer, Description')
            for category in self.categories_list:
                file.write(f', {category}')
            file.write('\n')

            # write each product
            for product in self.products_list:
                file.write(f'{product.title}, {product.manufacturer}, {product.description}')

                for category in self.categories_list:
                    if category in product.categories.all():
                        file.write(', 1')
                    else:
                        file.write(', 0')
                file.write('\n')

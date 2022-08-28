from PurchasesData.models import Category, Product


class DatasetBuilder:
    products_list: list

    def __init__(self):
        self.get_products_list()

    def get_products_list(self):
        self.products_list = Product.objects.exclude(categories=None)


class SimpleDatasetBuilder(DatasetBuilder):
    def get_dataset(self):
        """
        :return: dataset list
        """
        dataset = []
        for product in self.products_list:
            categories = product.categories.all()

            dataset.append((product.title, product.manufacturer, categories[len(categories)-1].title))
        return dataset

    def save_dataset(self):
        """
        writes the dataset into csv file
        """
        dataset = self.get_dataset()
        with open('simple_dataset.csv', 'w', encoding='utf-8') as file:
            # first row is label
            file.write('Title, Manufacturer, Main Category')
            for entry in dataset:
                file.write(f'{entry[0]}, {entry[1]}, {entry[2]}\n')


class ComplexDatasetBuilder(DatasetBuilder):
    categories_list: list

    def __init__(self):
        super().__init__()
        self.get_categories_list()

    def get_categories_list(self):
        self.categories_list = Category.objects.all()

    def get_dataset(self):
        """
        :return: dataset list
        """
        dataset = []

        for product in self.products_list:
            row = [product.title, product.manufacturer]

            for category in self.categories_list:
                if category in product.categories.all():
                    row.append(1)
                else:
                    row.append(0)

            dataset.append(tuple(row))

        return dataset

    def save_dataset(self):
        """
        writes dataset into csv file
        """
        with open('complex_dataset.csv', 'w', encoding='utf-8') as file:
            # first row as label
            file.write('Title, Manufacturer')
            for category in self.categories_list:
                file.write(f', {category}')
            file.write('\n')

            # write each product
            for product in self.products_list:
                file.write(f'{product.title}, {product.manufacturer}')

                for category in self.categories_list:
                    if category in product.categories.all():
                        file.write(', 1')
                    else:
                        file.write(', 0')
                file.write('\n')

import requests
from bs4 import BeautifulSoup as bs
from ML.classifiers import get_manufacturer, get_product_title
from .extract_title import get_title_and_quantity
from PurchasesData.models import Store, Category, Product
from bazarstoreDoc import ProductUnit


class BazarstoreParser:
    soup = bs(requests.get('https://bazarstore.az/').text, 'html.parser')

    def get_class_head_name_as_list(self, num):
        return self.soup.find("li", {"class": f"menu-item{num}"}).find("div", {"class": "col"}).find("span").text

    @staticmethod
    def get_description_by_link(link):
        soup = bs(requests.get(link).text, 'html.parser')
        return str(soup.find("div", {"class": "product-description"}).text).strip()

    def get_class_child_name_as_list(self):
        classes = []
        for num in range(20):
            try:
                for element in self.soup.find("li", {"class": f"menu-item{num}"}).find_all("div", {"class": "col"}):
                    classes.append(element.find("span").text)
            except AttributeError:
                pass
            except Exception as e:
                print(e)

        classes.remove('Öz Məhsullarımız')

        return classes[:-5]

    def get_class_child_url_as_list(self):
        list_of_links = []
        for num in range(20):
            try:
                for i in self.soup.find("li", {"class": f"menu-item{num}"}).find_all("a"):
                    list_of_links.append(i.get("href"))
            except AttributeError:
                pass
            except Exception as e:
                print(e)
        return list_of_links

    def get_every_product_from_page(self, page_soup):
        dirty_titles = page_soup.find_all("h5", {"class": "product-title"})

        clear_titles = []
        for i in dirty_titles:
            name = i.text
            link = i.find("a").get("href")
            description = self.get_description_by_link(link)
            clear_titles.append(ProductUnit(name, link, description))

        return clear_titles

    @staticmethod
    def get_count_of_pages_or_NONE(soup):
        dirty_pagination_numbers = (soup.find_all("li", {"class": "mx-2"}))
        pagination_numbers_as_str = []
        for i in dirty_pagination_numbers:
            pagination_numbers_as_str.append(i.find("span").text)

        pagination_numbers_as_int = []
        for i in pagination_numbers_as_str:
            try:
                i = int(i)
                pagination_numbers_as_int.append(i)
            except ValueError:
                pass
            except Exception as e:
                print(e)

        if not pagination_numbers_as_int:
            return None
        return max(pagination_numbers_as_int)

    def parse_products_from_link(self, link):
        page = requests.get(link)
        page_soup = bs(page.text, 'html.parser')
        pagination = self.get_count_of_pages_or_NONE(page_soup)
        if not pagination:
            return self.get_every_product_from_page(page_soup)

        product_list = []
        for page_num in range(1, pagination + 1):
            page = requests.get(link + f'?page={page_num}')
            page_soup = bs(page.text, 'html.parser')
            product_list.append(self.get_every_product_from_page(page_soup))

        return product_list

    def get_classes_and_urls_as_dict(self):
        classname = self.get_class_child_name_as_list()
        classurl = self.get_class_child_url_as_list()
        return dict(zip(classname, classurl))

    def get_product_and_its_class(self):
        link_class_dict = self.get_classes_and_urls_as_dict()
        link_product_dict = {}
        i = 0  #
        for cls, link in link_class_dict.items():
            i += 1  #
            # os.system('cls')
            print(f"{i}/492")  #
            if link:
                link_product_dict[cls] = self.parse_products_from_link(link)

        return link_product_dict


def write_to_db():
    parser = BazarstoreParser()
    store = Store.objects.get_or_create(name='Bazarstore',
                                        address='Bakı şəhəri, Binəqədi rayonu, Dərnəgül qəsəbəsi 108',
                                        taxpayer_name='Bazarstore MMC', type='supermarket', is_manufacturer=False)[0]
    store.save()
    categories_products = parser.get_product_and_its_class()

    for category_name in categories_products.keys():
        category = Category.objects.get_or_create(title=category_name)[0]
        category.save()

        for product_title in categories_products[category_name]:
            if type(product_title) == list:
                product_title = product_title[0]

            product_title = get_title_and_quantity(product_title)[0]
            manufacturer = get_manufacturer(product_title, store)
            product_title = get_product_title(product_title, store)

            product = Product.objects.get_or_create(title=product_title, manufacturer=manufacturer,
                                                    quantity=1, quantity_marker='', description='', price=0)[0]
            product.save()
            product.categories.add(category)


if __name__ == "__main__":
    BazarstoreParser().get_product_and_its_class()

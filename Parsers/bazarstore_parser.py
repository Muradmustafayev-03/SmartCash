import requests
from bs4 import BeautifulSoup as bs
import os


class BazarstoreParser:
    soup = bs(requests.get('https://bazarstore.az/').text, 'html.parser')

    def get_class_head_name_as_list(self, num):
        return self.soup.find("li", {"class": f"menu-item{num}"}).find("div", {"class": "col"}).find("span").text

    def get_class_child_name_as_list(self):
        classes = []
        for num in range(20):
            try:
                for element in self.soup.find("li", {"class": f"menu-item{num}"}).find_all("div", {"class": "col"}):
                    classes.append(element.find("span").text)
            except AttributeError:
                pass

        return classes[:-5]

    def get_class_child_url_as_list(self):
        list_of_links = []
        for num in range(20):
            try:
                for i in self.soup.find("li", {"class": f"menu-item{num}"}).find_all("a"):
                    list_of_links.append(i.get("href"))
            except Exception as e:
                print(e)
        return list_of_links

    @staticmethod
    def get_every_product_from_page(page_soup):
        dirty_titles = page_soup.find_all("h5", {"class": "product-title"})
        clear_titles = []
        for i in dirty_titles:
            clear_titles.append(i.text)

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
            except Exception as e:
                print(e)

        if not pagination_numbers_as_int:
            return None
        return max(pagination_numbers_as_int)

    def pars_products_from_link(self, link):
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
            os.system('cls')
            print(f"{i}/498")  #
            if link:
                link_product_dict[cls] = self.pars_products_from_link(link)

        return link_product_dict

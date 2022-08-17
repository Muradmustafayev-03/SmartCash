from ML.classifiers import get_product_title, get_manufacturer
from extract_title import get_title_and_quantity
from PurchasesData.models import Product, Store
from jellyfish import levenshtein_distance
from bs4 import BeautifulSoup
from wsgiref import headers
import requests


def get_search_url(title: str):
    return 'https://bazarstore.az/search?controller=search&s=' + '+'.join(title.split())


def get_products_url_list(search_url: str):
    content = requests.get(search_url, headers).content
    soup = BeautifulSoup(content, 'html.parser')
    products = [a.select('h5') for a in soup.find_all('article')]
    return [p[0].select('a')[0].attrs for p in products]


def multiple_word_levenshtein(s1: str, s2: str):
    s1, s2 = s1.lower(), s2.lower()
    d = 0
    for word1 in s1.split():
        word_d = levenshtein_distance(word1, s2.split()[0])
        for word2 in s2.split():
            if levenshtein_distance(word1, word2) < word_d:
                word_d = levenshtein_distance(word1, word2)
        d += word_d
    return d


def find_most_similar_product_url(title: str, products_url_list: list):
    most_similar = products_url_list[0]

    for product in products_url_list:
        product_title = product['title'].lower()
        most_similar_title = most_similar['title'].lower()

        if multiple_word_levenshtein(title, product_title) < multiple_word_levenshtein(title, most_similar_title):
            most_similar = product

    return most_similar['href']


def get_url_from_title(title: str):
    return find_most_similar_product_url(title, get_products_url_list(get_search_url(title)))


def get_info_from_url(url: str):
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    main = soup.select('section', {'id': 'main'})[0]

    title = main.select('h1')[0].text
    categories = [category.text.lower().strip('\n') for category in main.find_all('li')][1:-1]
    try:
        description = main.select('td')[0].getText()
    except IndexError:
        description = ''

    return title, categories, description


def get_info_from_title(title: str):
    return get_info_from_url(get_url_from_title(title))


def get_product_and_categories(title_from_receipt: str, price: float, store: Store):
    title_quantity_tuple = get_title_and_quantity(title_from_receipt)
    title_from_receipt = title_quantity_tuple[0]
    quantity = title_quantity_tuple[1]
    quantity_marker = title_quantity_tuple[2]

    site_title, categories, description = get_info_from_url(get_url_from_title(title_from_receipt))
    site_title = get_title_and_quantity(site_title)[0]

    title = get_product_title(site_title, store)
    manufacturer = get_manufacturer(site_title, store)

    product = Product.objects.get_or_create(title=title, manufacturer=manufacturer, quantity=quantity,
                                            quantity_marker=quantity_marker, description=description, price=price)[0]

    return product, categories

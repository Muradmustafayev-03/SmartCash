from .models import User, Purchase, Store, Product, PurchaseUnit
from .PurchaseDoc import PurchaseDoc
from ML import classifiers
import requests_html
import datetime
import re


def render_js(fiscal_ID: str):
    """
    Renders HTML and JS from e-kassa for a given Fiscal ID into the string
    :param fiscal_ID: Fiscal ID of the purchase
    :return: string that contains the electronic receipt data
    """
    url = 'https://monitoring.e-kassa.gov.az/#/index?doc=' + fiscal_ID
    session = requests_html.HTMLSession()
    r = session.get(url)
    r.html.render()
    text = r.html.text[22134:len(r.html.text) - 3780]
    session.close()
    try:
        assert text != ''
        return text
    except AssertionError:
        return render_js(fiscal_ID)
    except RecursionError:
        print('Connection problems, try again later')  # should raise a custom error
        return


def parse_purchase(user_FIN: str, fiscal_ID: str):
    """
    Parses all the important data from e-kassa into a dataclass object
    :param user_FIN: FIN of the user
    :param fiscal_ID: Fiscal ID of the purchase
    :return: PurchaseDoc
    """
    render = render_js(fiscal_ID)

    store_name = (re.findall(r'(?:TS adı:)(.*?)(?:\n)', render, re.MULTILINE)[0]).strip()
    store_address = (re.findall(r'(?:TS ünvanı:)(.*?)(?:\n)', render, re.MULTILINE)[0]).strip()
    taxpayer_name = (re.findall(r'(?:VÖ ADI:)(.*?)(?:\n)', render, re.MULTILINE)[0]).strip()
    date = datetime.datetime.strptime(re.findall(r'(?:Tarix:)(?:\n)(.*?)(?:\n)', render,
                                                 re.MULTILINE)[0], '%d.%m.%Y').date()
    time = datetime.datetime.strptime(re.findall(r'(?:Saat:)(?:\n)(.*?)(?:\n)', render,
                                                 re.MULTILINE)[0], '%H:%M:%S').time()
    products = re.findall(r'(.*?)(?:\*ƏDV: 18%\n)\((?:.*?)\)(?:\n)(\d+\.\d*)\n(\d+\.\d*)', render, re.MULTILINE) + \
               re.findall(r'(.*?)(?:\*ƏDV: 18%\n)(\d+\.\d*)\n(\d+\.\d*)', render, re.MULTILINE)
    total_price = float(re.findall(r'(?:Cəmi\n)(.*?)(?:\n)', render, re.MULTILINE)[1])

    cashless = bool(float(re.findall(r'(?:Nağd:\n)(.*?)(?:\n)', render, re.MULTILINE)[0]) == 0)

    total_payed = float(re.findall(r'(?:Nağdsız:\n)(.*?)(?:\n)', render, re.MULTILINE)[0]) if cashless \
        else float(re.findall(r'(?:Nağd:\n)(.*?)(?:\n)', render, re.MULTILINE)[0])

    discount = total_price - total_payed

    return PurchaseDoc(user_FIN=user_FIN, store_name=store_name, store_address=store_address,
                       taxpayer_name=taxpayer_name, date=date, time=time, products=products, total_price=total_price,
                       discount=discount, total_payed=total_payed, cashless=cashless)


def write_to_db(purchase_doc: PurchaseDoc):
    """
    Writes data from a PurchaseDoc into the database
    :param purchase_doc: PurchaseDoc that contains data to be saved in the database
    :return: None
    """
    user = User.objects.get_or_create(FIN=purchase_doc.user_FIN)[0]
    user.save()

    store = Store.objects.get_or_create(name=purchase_doc.store_name, address=purchase_doc.store_address,
                                        taxpayer_name=purchase_doc.taxpayer_name)[0]
    if store.type is None:
        store.type = classifiers.store_type(store)
        store.is_manufacturer = classifiers.is_manufacturer(store)

    store.save()

    purchase = Purchase(user=user, store=store, date=purchase_doc.date, time=purchase_doc.time,
                        total_price=purchase_doc.total_price, discount=purchase_doc.discount,
                        total_payed=purchase_doc.total_payed)
    purchase.save()

    for product_tuple in purchase_doc.products:
        title = classifiers.get_product_title(product_tuple[0], store)
        manufacturer = classifiers.get_manufacturer(product_tuple[0], store)
        product = Product.objects.get_or_create(title=title, manufacturer=manufacturer, price=product_tuple[2])[0]

        if product.category is None:
            product.category = classifiers.get_category(product)

        product.save()

        purchase_unit = PurchaseUnit(purchase=purchase, product=product, amount=product_tuple[1])
        purchase_unit.save()

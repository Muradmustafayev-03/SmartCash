from PurchasesData.models import Store, Product, Category


def store_type(store: Store):  # to be done
    return ''


def is_manufacturer(store: Store):  # to be done
    return False


def get_product_title(title_forms: list, store: Store):  # to be done
    return title_forms[0]


def get_manufacturer(title_forms: list, store: Store):  # to be done
    if store.is_manufacturer:
        return store.name
    else:
        return title_forms[0]


def get_categories(product: Product):  # to be done
    return Category.objects.get_or_create(title='undefined')[0]

from PurchasesData.models import Store, Product, Category


def store_type(store: Store):  # to be done
    return ''


def is_manufacturer(store: Store):  # to be done
    return False


def get_product_title(product: str, store: Store):  # to be done
    return product.name


def get_manufacturer(product: str, store: Store):  # to be done
    if store.is_manufacturer:
        return store.name
    else:
        return product


def get_category(product: Product):  # to be done
    return Category.objects.get_or_create(title='undefined')[0]

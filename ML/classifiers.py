from PurchasesData.models import Store, Product, Category


def store_type(store: Store):  # to be finished
    if 'store' in (store.name + store.taxpayer_name).lower() or 'market' in (store.name + store.taxpayer_name).lower():
        return 'supermarket'
    if 'cafe' in (store.name + store.taxpayer_name).lower() or 'kafe' in (store.name + store.taxpayer_name).lower():
        return 'cafe'
    if 'restaurant' in (store.name + store.taxpayer_name).lower() \
            or 'restoran' in (store.name + store.taxpayer_name).lower():
        return 'restaurant'
    return ''


def is_manufacturer(store: Store):  # to be reviewed
    if store.type == 'supermarket':
        return False
    else:
        return True


def get_product_title(title: str, store: Store):  # to be done
    return title


def get_manufacturer(title: str, store: Store):  # to be done
    if store.is_manufacturer:
        return store.name
    else:
        return title


def get_categories(product: Product):  # to be done
    return Category.objects.get_or_create(title='undefined')[0]

import re

quantity_markers = ['ml', 'l', 'lt', 'ltr', 'g', 'gr', 'q', 'qr', 'kg', 'kq', 'person', 'ed', 'eded', 'ədəd']


def get_title_and_quantity(title: str):
    title = title.lower().strip().strip('.').strip('-')\

    if 'pl' in title.split() or 'pl.' in title.split():
        title.replace('pl', 'pet')

    quantity = 1
    quantity_marker = ''

    numbers = re.findall(r'(\d+\.\d*)', title) + re.findall(r'(\d+,\d*)', title) + re.findall(r'(\d+)', title)

    for number in numbers:
        for qm in quantity_markers[::-1]:
            if title.endswith(number + qm):
                title = title.replace(number + qm, '')
                quantity, quantity_marker = number.replace(',', '.'), qm
            if title.endswith(number + ' ' + qm):
                title = title.replace(number + ' ' + qm, '')
                quantity, quantity_marker = number.replace(',', '.'), qm

    new_title = ''

    for i in range(len(title)):
        if title[i].isalpha() or title[i] == ' ':
            new_title += title[i]
        elif title[i].isnumeric():
            if title[i] != '0':
                new_title += title[i]
            elif title[i-1].isnumeric() and title[i-1] != '0':
                new_title += title[i]
        elif title[i] == '-' and title[i-1].isalpha() and title[i+1].isalpha():
            new_title += '-'

    new_title = new_title.strip()

    quantity = float(quantity)

    if quantity_marker in ['l', 'lt', 'ltr']:
        if quantity >= 1:
            quantity_marker = 'l'
        else:
            quantity_marker = 'ml'
            quantity *= 1000

    elif quantity_marker in ['g', 'gr', 'q', 'qr']:
        quantity_marker = 'gr'

    elif quantity_marker in ['kg', 'kq']:
        if quantity >= 1:
            quantity_marker = 'kg'
        else:
            quantity_marker = 'gr'
            quantity *= 1000

    return new_title, quantity, quantity_marker

from dataclasses import dataclass
import datetime


@dataclass
class Purchase:
    """
        user_FIN: str FIN code of user that made the purchase / scanned the QR - code\n
        store_name: str\n
        store_address: str\n
        taxpayer_name: str\n
        date: datetime.date\n
        time: datetime.time\n
        products: list [(product name: str, amount: float, price: float)), (...), ...]\n
        total_price: float sum(amount*price) for every product\n
        discount: float by default is set to 0, used only in case there is any discount\n
        total_payed: float total_price - discount\n
        cashless: bool indicates whether the payment was cashless\n
    """
    user_FIN: str  # FIN code of user that made the purchase / scanned the QR - code
    store_name: str
    store_address: str
    taxpayer_name: str
    date: datetime.date
    time: datetime.time
    products: list  # [(product name: str, amount: float, price: float)), (...), ...]
    total_price: float  # sum(amount*price) for every product
    discount: float  # by default is set to 0, used only in case there is any discount
    total_payed: float  # total_price - discount
    cashless: bool  # indicates whether the payment was cashless

    def __str__(self):
        return f'User FIN: {self.user_FIN}\n' \
               f'Store name: {self.store_name}\n' \
               f'Store address: {self.store_address}\n' \
               f'Taxpayer name: {self.taxpayer_name}\n' \
               f'Date: {self.date}\n' \
               f'Time: {self.time}\n' \
               f'Products:\n' \
               f'Name\tAmount\tPrice\n' + \
               '\n'.join(f'{product[0]}\t{product[1]}\t{product[2]}\n' for product in self.products) + \
               f'Total price: {self.total_price}\n' \
               f'Discount: {self.discount}\n' \
               f'Total payed: {self.total_payed}\n' \
               f'Payed cashless: {self.cashless}'


@dataclass
class ProductUnit:
    name: str
    link: str
    description: str = None

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

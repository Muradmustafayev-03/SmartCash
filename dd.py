import requests
from bs4 import BeautifulSoup as bs
    
    
soup = bs(requests.get('https://bazarstore.az/alkoqollu-pivlr/7837-pv-kronenburg-1664-blank-460ml-').text, 'html.parser')


print(str(soup.find("div",{"class":"product-description"}).text).strip())
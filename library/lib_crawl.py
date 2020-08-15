import requests
from lxml.cssselect import CSSSelector
from lxml.html import fromstring

def get_seat(campus):
    if campus == 0:
        url = "https://information.hanyang.ac.kr/#/smuf/seat/status"
    else:
        url = "https://lib.hanyang.ac.kr/#/smuf/seat/status"
    
    
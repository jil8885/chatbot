from enum import Enum
import requests
from lxml.cssselect import CSSSelector
from lxml.html import fromstring
import datetime

from utils import *
# Google firebase
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin

def get_cred():
    # cred = credentials.ApplicationDefault()
    cred = credentials.Certificate('C:\\Users\\Jeongin\\Downloads\\personal-sideprojects-c013420f3313.json')
    return cred

class Cafeteria(Enum):
    student_seoul_1 = "1"
    teacher_seoul_1 = "2"
    sarang_seoul = "3"
    teacher_seoul_2 = "4"
    student_seoul_2 = "5"
    dorm_seoul_1 = "6"
    dorm_seoul_2 = "7"
    hangwon_seoul = "8"
    teacher_erica = "11"
    student_erica = "12"
    dorm_erica = "13"
    foodcoart_erica = "14"
    changbo_erica = "15"

def get_recipe_from_firebase(cafeteria: Cafeteria):
    if (not len(firebase_admin._apps)):
        cred = get_cred()
        initialize_app(cred, {'projectId': 'personal-sideprojects'})
    db = firestore.client()
    fooddb = db.collection("foodinfo")
    food_doc = fooddb.document(cafeteria.value)
    now = datetime.datetime.now()
    try:
        if now.day != food_doc.get().to_dict()['date'].day:
            result = get_recipe(cafeteria)
            food_doc.update({
                'date' : now,
                'result' : result
            })
            return result
        else:
            return dict(food_doc.get().to_dict()['result'])
    except:
        result = get_recipe(cafeteria)
        food_doc.set({
            'date' : now,
            'result' : result
        })
        return result

def get_recipe(cafeteria : Cafeteria, url="https://www.hanyang.ac.kr/web/www/re"):
    ret = {}
    ret["restaurant"] = cafeteria.name

    inboxes = CSSSelector("div.in-box")
    h4 = CSSSelector("h4")  # 조식, 중식, 석식
    h3 = CSSSelector("h3")  # menu
    li = CSSSelector("li")
    price = CSSSelector("p.price")
    # get
    try:
        res = requests.get(f"{url}{cafeteria.value}")
    except requests.exceptions.RequestException as _:
        ret["restaurant"] = "-1"
        return ret

    tree = fromstring(res.text)
    for inbox in inboxes(tree):
        title = h4(inbox)[0].text_content()
        ret[title] = []
        for l in li(inbox):
            menu = h3(l)[0].text_content().replace("\t", "").replace("\r\n", "")
            p = price(l)[0].text_content()
            ret[title].append({"menu": menu, "price": p})

    return ret

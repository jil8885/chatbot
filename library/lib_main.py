import requests, os, time
from bs4 import BeautifulSoup
# Google firebase
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin

def get_cred():
    cred = credentials.ApplicationDefault()
    # cred = credentials.Certificate('C:\\Users\\Jeongin\\Downloads\\personal-sideprojects.json')
    return cred

def crawling_lib(location = None):
    string = ""
    if (not len(firebase_admin._apps)):
        cred = get_cred()
        initialize_app(cred, {'projectId': 'personal-sideprojects'})
    db = firestore.client()
    erica_collec = db.collection('libinfo').document('ERICA')
    libinfo = erica_collec.collection('library_list').stream()
    if location == 0:
        for x in libinfo:
            string += x.id + " "
            totalseat = x.to_dict()['total']
            activeseat = x.to_dict()['active']
            remained = totalseat - activeseat
            string += f"잔여 {remained}석\n"
    elif location == 1:
        info = erica_collec.collection('library_list').document('제1열람실').get()
        string += info.id + "\n"
        string += f"총 좌석 : {info.to_dict()['total']}석\n"
        string += f"사용중 : {info.to_dict()['active']}석\n"
        remained = info.to_dict()['total'] - info.to_dict()['active']
        string += f"잔여좌석 : {remained}석\n"
        string += f"점유율 : {info.to_dict()['occupied']}\n"
    elif location == 2:
        info = erica_collec.collection('library_list').document('제2열람실').get()
        string += info.id + "\n"
        string += f"총 좌석 : {info.to_dict()['total']}석\n"
        string += f"사용중 : {info.to_dict()['active']}석\n"
        remained = info.to_dict()['total'] - info.to_dict()['active']
        string += f"잔여좌석 : {remained}석\n"
        string += f"점유율 : {info.to_dict()['occupied']}\n"
    elif location == 3:
        info = erica_collec.collection('library_list').document('제3열람실').get()
        string += info.id + "\n"
        string += f"총 좌석 : {info.to_dict()['total']}석\n"
        string += f"사용중 : {info.to_dict()['active']}석\n"
        remained = info.to_dict()['total'] - info.to_dict()['active']
        string += f"잔여좌석 : {remained}석\n"
        string += f"점유율 : {info.to_dict()['occupied']}\n"
    elif location == 4:
        info = erica_collec.collection('library_list').document('제4열람실').get()
        string += info.id + "\n"
        string += f"총 좌석 : {info.to_dict()['total']}석\n"
        string += f"사용중 : {info.to_dict()['active']}석\n"
        remained = info.to_dict()['total'] - info.to_dict()['active']
        string += f"잔여좌석 : {remained}석\n"
        string += f"점유율 : {info.to_dict()['occupied']}\n"
    return string.strip()


def crawling_lib2(location = None):
    string = ""
    if (not len(firebase_admin._apps)):
        cred = get_cred()
        initialize_app(cred, {'projectId': 'personal-sideprojects'})
    db = firestore.client()
    seoul_collec = db.collection('libinfo').document('Seoul')
    libinfo = seoul_collec.collection('library_list').stream()
    if location == 0:
        for x in libinfo:
            string += x.id + " "
            totalseat = x.to_dict()['total']
            activeseat = x.to_dict()['active']
            remained = totalseat - activeseat
            string += f"잔여 {remained}석\n"
    elif location == 1:
        info = seoul_collec.collection('library_list').document('제1열람실').get()
        string += info.id + "\n"
        string += f"총 좌석 : {info.to_dict()['total']}석\n"
        string += f"사용중 : {info.to_dict()['active']}석\n"
        remained = info.to_dict()['total'] - info.to_dict()['active']
        string += f"잔여좌석 : {remained}석\n"
        string += f"점유율 : {info.to_dict()['occupied']}\n"
    elif location == 2:
        info = seoul_collec.collection('library_list').document('제2열람실').get()
        string += info.id + "\n"
        string += f"총 좌석 : {info.to_dict()['total']}석\n"
        string += f"사용중 : {info.to_dict()['active']}석\n"
        remained = info.to_dict()['total'] - info.to_dict()['active']
        string += f"잔여좌석 : {remained}석\n"
        string += f"점유율 : {info.to_dict()['occupied']}\n"
    elif location == 3:
        info = seoul_collec.collection('library_list').document('제3열람실').get()
        string += info.id + "\n"
        string += f"총 좌석 : {info.to_dict()['total']}석\n"
        string += f"사용중 : {info.to_dict()['active']}석\n"
        remained = info.to_dict()['total'] - info.to_dict()['active']
        string += f"잔여좌석 : {remained}석\n"
        string += f"점유율 : {info.to_dict()['occupied']}\n"
    elif location == 4:
        info = seoul_collec.collection('library_list').document('제4열람실').get()
        string += info.id + "\n"
        string += f"총 좌석 : {info.to_dict()['total']}석\n"
        string += f"사용중 : {info.to_dict()['active']}석\n"
        remained = info.to_dict()['total'] - info.to_dict()['active']
        string += f"잔여좌석 : {remained}석\n"
        string += f"점유율 : {info.to_dict()['occupied']}\n"
    elif location == 5:
        info = seoul_collec.collection('library_list').document('법학 대학원열람실').get()
        string += info.id + "\n"
        string += f"총 좌석 : {info.to_dict()['total']}석\n"
        string += f"사용중 : {info.to_dict()['active']}석\n"
        remained = info.to_dict()['total'] - info.to_dict()['active']
        string += f"잔여좌석 : {remained}석\n"
        string += f"점유율 : {info.to_dict()['occupied']}\n"
    elif location == 6:
        info = seoul_collec.collection('library_list').document('법학 제1열람실').get()
        string += info.id + "\n"
        string += f"총 좌석 : {info.to_dict()['total']}석\n"
        string += f"사용중 : {info.to_dict()['active']}석\n"
        remained = info.to_dict()['total'] - info.to_dict()['active']
        string += f"잔여좌석 : {remained}석\n"
        string += f"점유율 : {info.to_dict()['occupied']}\n"
    elif location == 7:
        info = seoul_collec.collection('library_list').document('법학 제2열람실A').get()
        string += info.id + "\n"
        string += f"총 좌석 : {info.to_dict()['total']}석\n"
        string += f"사용중 : {info.to_dict()['active']}석\n"
        remained = info.to_dict()['total'] - info.to_dict()['active']
        string += f"잔여좌석 : {remained}석\n"
        string += f"점유율 : {info.to_dict()['occupied']}\n"
    elif location == 8:
        info = seoul_collec.collection('library_list').document('법학 제2열람실B').get()
        string += info.id + "\n"
        string += f"총 좌석 : {info.to_dict()['total']}석\n"
        string += f"사용중 : {info.to_dict()['active']}석\n"
        remained = info.to_dict()['total'] - info.to_dict()['active']
        string += f"잔여좌석 : {remained}석\n"
        string += f"점유율 : {info.to_dict()['occupied']}\n"
    return string.strip()

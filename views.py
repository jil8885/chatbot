import datetime
import json
import os

from copy import deepcopy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .food.food_main import make_string_food, make_string_food2
from .library.lib_main import crawling_lib, crawling_lib2
from .transport.shuttle_main import shuttle_main
from .transport.shuttle.strings import first_last
from .transport.shuttle.date import is_seasonal, is_semester

# Google firebase
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin

# global answer
base_response = {'version': '2.0', 'template': {'outputs': [], 'quickReplies': []}}

# Get firebase auth credential
def get_cred():
    cred = credentials.ApplicationDefault()
    # cred = credentials.Certificate('C:\\Users\\Jeongin\\Downloads\\personal-sideprojects.json')
    return cred



# Get users answer and user key.
def json_parser(request):
    answer = json.loads(request.body.decode("utf-8"))["userRequest"]["utterance"]
    user = json.loads(request.body.decode("utf-8"))["userRequest"]["user"]['id']
    return answer, user


# Get User info.
def get_user(user_key):
    if (not len(firebase_admin._apps)):
        cred = get_cred()
        initialize_app(cred, {'projectId': 'personal-sideprojects'})
    db = firestore.client()
    users = db.collection('botuser').where('id', '==', user_key)
    for user in users.stream():
        return user.to_dict()


# Insert User Info
def create_user(user_key, campus):
    if (not len(firebase_admin._apps)):
        cred = get_cred()
        initialize_app(cred, {'projectId': 'personal-sideprojects'})
    db = firestore.client()
    user = db.collection('botuser').document(user_key)
    user.set({'id' : user_key, 'campus' : campus})


# Update User Info
def update_user(user_key, campus):
    if (not len(firebase_admin._apps)):
        cred = get_cred()
        initialize_app(cred, {'projectId': 'personal-sideprojects'})
    db = firestore.client()
    user = db.collection('botuser').document(user_key)
    user.update({'campus' : campus})


# Make Image Answer
def insert_image(image_url, alt_text):
    new_response = deepcopy(base_response)
    new_response['template']['outputs'] = [{"simpleImage": {"imageUrl": image_url, "altText": alt_text}}]
    return new_response


# Make Text Answer
def insert_text(text):
    new_response = deepcopy(base_response)
    new_response['template']['outputs'] = [{"simpleText": {"text": text}}]
    return new_response


# Make Card Answer
def insert_card(title, description, image_url=None, width=None, height=None):
    new_response = deepcopy(base_response)
    if image_url != None:
        if width != None and height != None:
            new_response['template']['outputs'] = [{'basicCard':{
                'title' : title,
                'description' : description,
                'thumbnail': {"imageUrl" : image_url, 'fixedRatio': True, 'width': width, 'height': height},
                'buttons' : []
            }}]
        else:
            new_response['template']['outputs'] = [{'basicCard':{
                'title' : title,
                'description' : description,
                'thumbnail': {"imageUrl" : image_url},
                'buttons' : []
            }}]
    else:
        new_response['template']['outputs'] = [{'basicCard':{
            'title' : title,
            'description' : description,
            'buttons' : []
        }}]
    return new_response


def insert_button(new_response, label, webUrl):
    new_response['template']['outputs'][0]['basicCard']['buttons'].append({
        "action":  "webLink",
        "label": label,
        "webLinkUrl": webUrl
    })
    return new_response

# Insert Quick Replies
def insert_replies(new_response, reply):
    new_response['template']['quickReplies'].append(reply)
    return new_response


# Make Reply
def make_reply(label, message, block_id):
    return {'action': 'block', 'label': label, 'messageText': message, 'blockId': block_id}


# Get CampusInfo
def is_seoul(user_info):
    return user_info['campus'] == 1


@csrf_exempt
def shuttle_photo(request):
    now = datetime.datetime.now()
    base_link = "https://raw.githubusercontent.com/jil8885/chatbot/release/hyuabot/templates/"
    if is_semester(now.month, now.day):
        path = "semester.jpg"
        string = "학기중입니다."
    elif is_seasonal(now.month, now.day):
        path = "seasonal.jpg"
        string = "계절학기 입니다."
    else:
        path = "vacation.jpg"
        string = "방학중입니다."
    response = insert_image(base_link + path, string)
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def shuttle(request):
    answer, _ = json_parser(request)
    stop_list = {"셔틀콕": "shuttle_o", "한대앞역": "station", "예술인A": "terminal", "기숙사": "dormitory", "셔틀콕 건너편": "shuttle_i"}
    emoji = {"셔틀콕": '🏫 ', "한대앞역": '🚆 ', "예술인A": '🚍 ', "기숙사": '🏘️ ', "셔틀콕 건너편": '🏫 '}
    block_id = '5cc3dc8ee82127558b7e6eba'
    if "도착 정보입니다" in answer:
        stop_korean = answer.split("의")[0]
    else:
        stop_korean = answer.split(" ")[1]
    if stop_korean == "셔틀콕":
        if "건너편" in answer:
            stop_korean = "셔틀콕 건너편"
        else:
            stop_korean = "셔틀콕"
    stop = stop_list[stop_korean]
    now = datetime.datetime.now()
    rest_date = [(12, 25), (1, 1)]
    if (now.month, now.day) in rest_date:
        string = "당일, %d월 %d일은 셔틀 미운행합니다." % (now.month, now.day)       
    else:
        if is_semester(now.month, now.day):
            string = "학기중 시간표입니다.\n"
        elif is_seasonal(now.month, now.day):
            string = "계절학기 시간표입니다.\n"
        else:
            string = "방학중 시간표입니다.\n"
        # 셔틀콕 도착 정보
        if stop == "shuttle_o":
            string += '셔틀콕 → 한대앞(직행)\n'
            string += shuttle_main('shuttleOut', 'DH') + '\n\n'
            string += '셔틀콕 → 예술인A(직행)\n'
            string += shuttle_main('shuttleOut', 'DY') + '\n\n'
            string += '셔틀콕 → 한대앞 → 예술인A(순환)\n'
            string += shuttle_main('shuttleOut', 'C') + '\n\n'
            string += '한대앞, 예술인 방면' + '\n'
            string += first_last('shuttleOut')
        elif stop == "shuttle_i":
            string += '셔틀콕 건너편 → 기숙사\n'
            string += shuttle_main('shuttleIn', 'R') + '\n\n'
            string += '셔틀콕 건너편 종착\n'
            string += shuttle_main('shuttleIn', 'NA') + '\n\n'
            string += '기숙사 방면' + '\n'
            string += first_last('shuttleIn')            
        # 한대앞역 도착 정보
        elif stop == "station":
            string += '한대앞 → 셔틀콕(직행)\n'
            string += shuttle_main('subway', '') + '\n\n'
            string += '한대앞 → 예술인A → 셔틀콕(순환)\n'
            string += shuttle_main('subway', 'C') + '\n\n'
            string += first_last('subway')
        # 예술인A 도착 정보
        elif stop == "terminal":
            string += shuttle_main('terminal') + '\n\n'
            string += first_last('terminal')
        # 창의인재원 도착 정보
        elif stop == "dormitory":
            string += '기숙사 → 셔틀콕, 한대앞\n'
            string += shuttle_main('dorm', 'DH') + '\n\n'
            string += '기숙사 → 셔틀콕, 예술인A\n'
            string += shuttle_main('dorm', 'DY') + '\n\n'
            string += '기숙사 → 셔틀콕, 한대앞, 예술인A(순환)\n'
            string += shuttle_main('dorm', 'C') + '\n\n'
            string += first_last('dorm')
    response = insert_text(string)
    reply = make_reply('🔍 정류장', f'{stop_korean} 정류장 정보입니다.', '5ebf702e7a9c4b000105fb25')
    response = insert_replies(response, reply)
    reply = make_reply('🚫 오류제보', '셔틀 오류 제보하기','5cc3fced384c5508fceec5bb')
    response = insert_replies(response, reply)
    for stop_name in stop_list.keys():
        if stop_name != stop_korean:
            message = f"{stop_name}의 셔틀버스 도착 정보입니다"

            reply = make_reply(emoji[stop_name] + stop_name, message, block_id)
            response = insert_replies(response, reply)

    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def stop_detail(request):
    answer, _ = json_parser(request)
    stop_list = {"셔틀콕": "shuttle", "셔틀콕 건너편": "shuttle", "한대앞역": "station", "예술인A": "terminal", "기숙사": "dormitory"}
    stop_view = {"shuttle" : "http://kko.to/Kf-ZqboYH", "station" : "http://kko.to/h9ROqsoDM", "dormitory" : "http://kko.to/vClEubBDj", "terminal": "http://kko.to/guG2uboYB"}
    stop_name = answer.split('정류장 정보입니다')[0].strip()
    stop_key = stop_list[stop_name]
    response = insert_card('정류장 정보', stop_name)
    # response = insert_button(response, '🗺️ 카카오맵에서 보기', stop_map[stop_key])
    response = insert_button(response, '👀 로드뷰로 보기', stop_view[stop_key])
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})



@csrf_exempt
def food(request):
    answer, user = json_parser(request)
    user_info = get_user(user)
    block_id = '5eaa9b11cdbc3a00015a23fb'
    seoul_restaurant = ['학생식당', '신학생식당', '교직원식당', '신교직원식당', '제1생활관식당', '제2생활관식당', '사랑방', '행원파크']
    erica_restaurant = ['학생식당', '교직원식당', '창의인재원식당', '창업보육센터', '푸드코트']
    if not user_info:
        if '서울' in answer:
            create_user(user, 1)
            response = insert_text('서울캠퍼스로 전환되었습니다.')
            for restaurant in seoul_restaurant:
                reply = make_reply(restaurant, f"{restaurant}의 식단입니다", block_id)
                response = insert_replies(response, reply)
        elif 'ERICA' in answer:
            create_user(user, 0)
            response = insert_text('ERICA 캠퍼스로 전환되었습니다.')
            for restaurant in erica_restaurant:
                reply = make_reply(restaurant, f"{restaurant}의 식단입니다", block_id)
                response = insert_replies(response, reply)
        else:
            block_id = '5cc3effc384c5508fceec584'
            campuses = ['서울', 'ERICA']
            response = insert_text('캠퍼스를 지정해주십시오')
            for campus in campuses:
                reply = make_reply(campus, f"{campus}로 지정되었습니다.", block_id)
                response = insert_replies(response, reply)
    elif "의 식단입니다" in answer:
        store = answer.split("의 식단")[0]
        if not is_seoul(user_info):
            string = make_string_food(store)
            response = insert_text(string)
            for restaurant in erica_restaurant:
                reply = make_reply(restaurant, f"{restaurant}의 식단입니다", block_id)
                response = insert_replies(response, reply)
        else:
            string = make_string_food2(store)
            response = insert_text(string)
            for restaurant in seoul_restaurant:
                reply = make_reply(restaurant, f"{restaurant}의 식단입니다", block_id)
                response = insert_replies(response, reply)
    elif "메뉴" in answer:
        string = '원하시는 식당을 선택해주세요'
        if not is_seoul(user_info):
            response = insert_text(string)
            for restaurant in erica_restaurant:
                reply = make_reply(restaurant, f"{restaurant}의 식단입니다", block_id)
                response = insert_replies(response, reply)
        else:
            response = insert_text(string)
            for restaurant in seoul_restaurant:
                reply = make_reply(restaurant, f"{restaurant}의 식단입니다", block_id)
                response = insert_replies(response, reply)
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def library(request):
    answer, user = json_parser(request)
    user_info = get_user(user)
    block_id = '5e0df82cffa74800014bc838'
    seoul_lib = ['제1열람실', '제2열람실', '제3열람실', '제4열람실', '법학 대학원열람실', '법학 제1열람실', '법학 제2열람실A', '법학 제2열람실B']
    erica_lib = ['제1열람실', '제2열람실', '제3열람실', '제4열람실']
    if not user_info:
        if '서울' in answer:
            create_user(user, 1)
            response = insert_text('서울캠퍼스로 지정되었습니다.')
            for lib in seoul_lib:
                reply = make_reply('📖 ' + lib, f"{lib}의 좌석정보입니다.", block_id)
                response = insert_replies(response, reply)
        elif 'ERICA' in answer:
            create_user(user, 0)
            response = insert_text('ERICA 캠퍼스로 지정되었습니다.')
            for lib in erica_lib:
                reply = make_reply('📖 ' + lib, f"{lib}의 좌석정보입니다.", block_id)
                response = insert_replies(response, reply)
        else:
            campuses = ['서울', 'ERICA']
            response = insert_text('캠퍼스를 지정해주십시오')
            for campus in campuses:
                reply = make_reply(campus, f"{campus}로 지정되었습니다.", block_id)
                response = insert_replies(response, reply)
    elif is_seoul(user_info):
        if "열람실 정보" in answer:
            location = 0
        elif "법학" in answer:
            if "대학원" in answer:
                location = 5
            elif "제1" in answer:
                location = 6
            elif "A" in answer:
                location = 7
            elif "B" in answer:
                location = 8
        else:
            if "제1" in answer:
                location = 1
            elif "제2" in answer:
                location = 2
            elif "제3" in answer:
                location = 3
            elif "제4" in answer:
                location = 4
        string = crawling_lib2(int(location))
        response = insert_text(string)
        for lib in seoul_lib:
            reply = make_reply('📖 ' + lib, f"{lib}의 좌석정보입니다.", block_id)
            response = insert_replies(response, reply)
    else:
        if "열람실 정보" in answer:
            location = 0
        elif "좌석정보입니다." in answer:
            location = answer[1]
        string = crawling_lib(int(location))
        response = insert_text(string)
        for lib in erica_lib:
            reply = make_reply('📖 ' + lib, f"{lib}의 좌석정보입니다.", block_id)
            response = insert_replies(response, reply)
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def update_campus(request):
    answer, user = json_parser(request)
    user_info = get_user(user)
    block_id = '5eaa9bf741559f000197775d'
    if not user_info:
        if '서울' in answer:
            create_user(user, 1)
            response = insert_text('서울캠퍼스로 전환되었습니다.')
        elif 'ERICA' in answer:
            create_user(user, 0)
            response = insert_text('ERICA 캠퍼스로 전환되었습니다.')

        else:
            campuses = ['서울', 'ERICA']
            response = insert_text('캠퍼스를 지정해주십시오')
            for campus in campuses:
                reply = make_reply(campus, f"{campus}로 지정되었습니다.", block_id)
                response = insert_replies(response, reply)
    elif is_seoul(user_info):
        update_user(user, 0)
        response = insert_text('ERICA 캠퍼스로 전환되었습니다.')
    else:
        update_user(user, 1)
        response = insert_text('서울 캠퍼스로 전환되었습니다.')
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

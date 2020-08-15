import requests, os
from bs4 import BeautifulSoup
import datetime

from .food_crawl import Cafeteria, get_recipe
def make_string_food(cafeteria):
    string = crawling(cafeteria)
    return string

def crawling(cafeteria, date=None):
    string=""
    cafeterias = {
        "학생식당" : Cafeteria.student_erica, 
        "창의인재원식당" : Cafeteria.dorm_erica, 
        "교직원식당": Cafeteria.teacher_erica, 
        "창업보육센터": Cafeteria.changbo_erica, 
        "푸드코트" : Cafeteria.foodcoart_erica}
    if "학식메뉴" in cafeteria:
        return "ERICA캠퍼스의 식당 목록입니다"
    today = datetime.datetime.now()
    # 시간별 조식, 중식, 석식을 나눔
    string += "%s년%s월%s일 "%(today.year, today.month, today.day)
    cafeteria_code = cafeterias[cafeteria]
    recipe = get_recipe(cafeteria_code)
    if "중식" in recipe.keys():
        if today.hour < 10:
            if "조식" in recipe.keys():
                string += "조식\n"
                menus = recipe["조식"]
            else:
                string += "중식\n"
                menus = recipe["중식"]            
        elif today.hour < 15:
            string += "중식\n"
            menus = recipe["중식"]
        elif today.hour < 19:
            if "석식" in recipe.keys():
                string += "석식\n"
                menus = recipe["석식"]
            else:
                string += "중식\n"
                menus = recipe["중식"]  
        else:
            menus = [{"info": "미운영 시간입니다."}]
            string = "식당 운영시간이 아닙니다."
    else:
        menus = []

    # 식단이 없을 때
    if not menus:
        string = '식단이 제공되지 않습니다'
    if "info" not in menus[0].keys():
        for x in menus:
            string += x["menu"] + "\n"
            string += x["price"] + "원\n"
            string += '\n'
        if string[-1] == '\n':
            string = string[:-1]
    return string.strip()


# 서울캠퍼스
def make_string_food2(cafeteria):
    string = crawling2(cafeteria)
    return string

def crawling2(cafeteria, date=None):
    string=""
    cafeterias = {
        "학생식당" : Cafeteria.student_seoul_1, 
        "교직원식당" : Cafeteria.teacher_seoul_1, 
        "신학생식당": Cafeteria.student_seoul_2, 
        "신교직원식당": Cafeteria.teacher_seoul_2,
        "제1생활관식당": Cafeteria.dorm_seoul_1,
        "제2생활관식당": Cafeteria.dorm_seoul_2,
        "사랑방" : Cafeteria.sarang_seoul,
        "행원파크" : Cafeteria.hangwon_seoul
        }
    if "학식메뉴" in cafeteria:
        return "서울캠퍼스의 식당 목록입니다"
    today = datetime.datetime.now()
    # 시간별 조식, 중식, 석식을 나눔
    string += "%s년%s월%s일 "%(today.year, today.month, today.day)
    cafeteria_code = cafeterias[cafeteria]
    recipe = get_recipe(cafeteria_code)
    if "중식" in recipe.keys():
        if today.hour < 10:
            if "조식" in recipe.keys():
                string += "조식\n"
                menus = recipe["조식"]
            else:
                string += "중식\n"
                menus = recipe["중식"]            
        elif today.hour < 15:
            string += "중식\n"
            menus = recipe["중식"]
        elif today.hour < 19:
            if "석식" in recipe.keys():
                string += "석식\n"
                menus = recipe["석식"]
            else:
                string += "중식\n"
                menus = recipe["중식"]  
        else:
            menus = [{"info": "미운영 시간입니다."}]
            string = "식당 운영시간이 아닙니다."
    else:
        if "중식/석식" in recipe.keys():
            string += "중식/석식\n"
            menus = recipe["중식/석식"]
    if "분식" in recipe.keys():
        string += "분식\n"
        menus = recipe["분식"]            
    # 식단이 없을 때
    if not menus:
        string = '식단이 제공되지 않습니다'
    if "info" not in menus[0].keys():
        for x in menus:
            string += x["menu"] + "\n"
            string += x["price"] + "원\n"
            string += '\n'
        if string[-1] == '\n':
            string = string[:-1]
    return string.strip()


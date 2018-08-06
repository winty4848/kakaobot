import json, datetime
from kakaobot.models import Menu
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

def create_menu_db(cafe_name, menu,today):
    Menu.objects.create(
        cafe_name=cafe_name,
        menu=menu,
        date=today
    )

today = datetime.date.today().strftime("%Y년 %m월 %d일".encode('unicode-escape').decode()).encode().decode('unicode-escape')
menu_db = Menu.objects.filter(date=today)
menu_db.delete()
html = Request('http://dgucoop.dongguk.edu/store/store.php?w=4&l=2&j=0')
webpage = urlopen(html).read()
soup = BeautifulSoup(webpage, "lxml")
table_div = soup.find(id="sdetail")
tables = table_div.find_all("table")
menu_table = tables[1]
trs = menu_table.find_all('tr')
month_day = trs[0]
month_day_tds = month_day.find_all('td')

today_date = datetime.date.today().strftime("%m월 %d일".encode('unicode-escape').decode()).encode().decode(
    'unicode-escape')
date_number = 0

for i in range(1, 8):
    if today_date == month_day_tds[i].get_text()[1:]:
        date_number = i
        break

sangrock_rice = trs[8]
tds = sangrock_rice.find_all('td')
sangrock_rice_menu = tds[date_number + 1].get_text()
create_menu_db('상록원_백반코너', sangrock_rice_menu,today)

sangrock_oneplate = trs[10]
tds = sangrock_oneplate.find_all('td')
sangrock_oneplate_menu = tds[date_number + 1].get_text()
create_menu_db('상록원_일품코너', sangrock_oneplate_menu,today)

sangrock_cutlet = trs[12]
tds = sangrock_cutlet.find_all('td')
sangrock_cutlet_menu = tds[date_number + 1].get_text()
create_menu_db('상록원_양식코너', sangrock_cutlet_menu,today)

sangrock_head = trs[14]
tds = sangrock_head.find_all('td')
sangrock_head_menu = tds[date_number + 1].get_text()
create_menu_db('상록원_뚝배기코너', sangrock_head_menu,today)

dorm = trs[26]
tds = dorm.find_all('td')
dorm_menu = tds[date_number + 1].get_text()
create_menu_db('기숙사_A코너', dorm_menu,today)

employee_house = trs[2]
tds = employee_house.find_all('td')
employee_house_menu = tds[date_number + 1].get_text()
create_menu_db('교직원_집밥', employee_house_menu,today)

employee_oneplate = trs[4]
tds = employee_oneplate.find_all('td')
employee_oneplate_menu = tds[date_number + 1].get_text()
create_menu_db('교직원_한그릇', employee_oneplate_menu,today)
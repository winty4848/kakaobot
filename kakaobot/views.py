from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json, datetime
from dguyummy.models import Menu
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


def keyboard(request):

    return JsonResponse({
        'type' : 'buttons',
        'buttons' : ['학식', '가위바위보 게임', '자기소개']
    })

'''
POST 방식을 사용하기 때문에 Django에서는 CSRF Token 에러가 발생하며,
@csrf_exempt를 이용해 에러가 발생하지 않도록 해야 한다.
'''

@csrf_exempt
def answer(request):
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    player_choice = received_json_data['content']
    now_user_key = received_json_data['user_key']
    today_date = datetime.date.today().strftime("%m월 %d일".encode('unicode-escape').decode()).encode().decode('unicode-escape')
    '''
    위의 strtime('~~~한글~~~')때문에 계속 http 에러 500이 나왔었다.
    https://github.com/sphinx-doc/sphinx/issues/2102
    '''

    if player_choice=='학식':
        return JsonResponse({
            'message': {
                '메뉴를 보고싶은 식당은 어디인가요?'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['상록원', '그루터기', '기숙사식당', '교직원식당', '그만보기']
            }
        })
    elif player_choice == '그만보기':
        return JsonResponse({
            'message': {
                'text': '그만보기를 선택하셨습니다.'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['학식', '가위바위보 게임', '자기소개']
            }
        })
    elif player_choice=='그루터기':
        return JsonResponse({
            'message': {
                '방학 중에는 그루터기를 운영하지 않습니다...'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['상록원', '그루터기', '기숙사식당', '교직원식당', '그만보기']
            }
        })
    elif player_choice=='상록원' or player_choice=='기숙사식당' or player_choice=='교직원식당':
        return JsonResponse({
            'message': {
                'text': today_date + '의 ' + player_choice + ' 중식 메뉴입니다.'+ get_menu(player_choice)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['상록원', '그루터기', '기숙사식당', '교직원식당', '그만보기']
            }
        })


## 누른 버튼의 이름을 파라미터로 받아 DB에서 메뉴를 가져옴.
def get_menu(cafeteria_name):
    if cafeteria_name == '상록원':
        sangrock_rice = Menu.objects.get(cafe_name='상록원_백반코너').menu
        sangrock_oneplate= Menu.objects.get(cafe_name='상록원_일품코너').menu
        sangrock_cutlet = Menu.objects.get(cafe_name='상록원_양식코너').menu
        sangrock_head = Menu.objects.get(cafe_name='상록원_뚝배기코너').menu

        return "------------\n" +  "백반코너 \n" + sangrock_rice \
               + "------------\n" + "일품코너 \n" + sangrock_oneplate \
               + "------------\n" + "양식코너 \n" + sangrock_cutlet \
               + "------------\n" + "뚝배기코너 \n" + sangrock_head

    elif cafeteria_name == '그루터기':
        tree_A = Menu.objects.get(cafe_name='그루터기_A코너').menu
        tree_B=Menu.objects.get(cafe_name='그루터기_B코너').menu

        return "------------\n" + "A코너 \n" + tree_A \
               + "------------\n" + "B코너 \n" + tree_B

    elif cafeteria_name == '기숙사식당':
        dorm = Menu.objects.get(cafe_name='기숙사_A코너').menu

        return "------------\n" + "A코너 \n" + dorm

    elif cafeteria_name == '교직원식당':
        employee_house = Menu.objects.get(cafe_name='교직원_집밥').menu
        employee_oneplate = Menu.objects.get(cafe_name='교직원_한그릇').menu

        return "------------\n" + "집밥 \n" + employee_house \
               + "------------\n" + "한그릇 \n" + employee_oneplate

def crawl(request):
    menu_db = Menu.objects.all()
    # 최신상태유지위해 DB모조리 삭제
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
    create_menu_db('상록원_백반코너', sangrock_rice_menu)

    sangrock_oneplate = trs[10]
    tds = sangrock_oneplate.find_all('td')
    sangrock_oneplate_menu = tds[date_number + 1].get_text()
    create_menu_db('상록원_일품코너', sangrock_oneplate_menu)

    sangrock_cutlet = trs[12]
    tds = sangrock_cutlet.find_all('td')
    sangrock_cutlet_menu = tds[date_number + 1].get_text()
    create_menu_db('상록원_양식코너', sangrock_cutlet_menu)

    sangrock_head = trs[14]
    tds = sangrock_head.find_all('td')
    sangrock_head_menu = tds[date_number + 1].get_text()
    create_menu_db('상록원_뚝배기코너', sangrock_head_menu)

    dorm = trs[26]
    tds = dorm.find_all('td')
    dorm_menu = tds[date_number + 1].get_text()
    create_menu_db('기숙사_A코너', dorm_menu)

    employee_house = trs[2]
    tds = employee_house.find_all('td')
    employee_house_menu = tds[date_number + 1].get_text()
    create_menu_db('교직원_집밥', employee_house_menu)

    employee_oneplate = trs[4]
    tds = employee_oneplate.find_all('td')
    employee_oneplate_menu = tds[date_number + 1].get_text()
    create_menu_db('교직원_한그릇', employee_oneplate_menu)

#DB에 저장해주는 녀석
def create_menu_db(cafe_name, menu):
    Menu.objects.create(
        cafe_name=cafe_name,
        menu=menu
    )
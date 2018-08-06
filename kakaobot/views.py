from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from kakaobot.models import Game
import json, datetime
## model에서 integer 값을 증가시키기위한 함수
from django.db.models import F
from .game import rcpgame
from .today_menu import get_menu

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

    if player_choice == '학식':
        return JsonResponse({
            'message': {
                'text': '메뉴를 보고싶은 식당은 어디인가요?'
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
    elif player_choice == '그루터기':
        return JsonResponse({
            'message': {
                'text': '방학 중에는 그루터기를 운영하지 않습니다...'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['상록원', '그루터기', '기숙사식당', '교직원식당', '그만보기']
            }
        })
    elif player_choice == '상록원' or player_choice=='기숙사식당' or player_choice=='교직원식당':
        return JsonResponse({
            'message': {
                'text': today_date + '의 ' + player_choice + ' 중식 메뉴입니다.'+ get_menu(player_choice)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['상록원', '그루터기', '기숙사식당', '교직원식당', '그만보기']
            }
        })


    elif player_choice == '가위바위보 게임':
        return JsonResponse({
            'message': {
                'text': '안내면 진거 가위바위보!'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['가위', '바위', '보', '전적 초기화']
            }
        })

    elif player_choice == '전적 초기화':
        return JsonResponse({
            'message': {
                'text': '정말로 전적을 초기화하시겠습니까? 돌이킬수 없어요...'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['초기화 가즈아', '안하겠습니다']
            }
        })

    elif player_choice == '초기화 가즈아':
        Game.objects.filter(user_key=now_user_key).update(win=0)
        Game.objects.filter(user_key=now_user_key).update(draw=0)
        Game.objects.filter(user_key=now_user_key).update(lose=0)
        return JsonResponse({
            'message': {
                'text': '전적이 초기화되었습니다..'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['학식', '가위바위보 게임', '자기소개']
            }
        })

    elif player_choice == '안하겠습니다':
        return JsonResponse({
            'message': {
                'text': '잘 생각하셨어요 ^.^'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['학식', '가위바위보 게임', '자기소개']
            }
        })

    elif player_choice == '가위' or player_choice == '바위' or player_choice == '보':
        check = Game.objects.filter(user_key=now_user_key)
        # filter 결과가 empty면 False로 출력되나봄.
        if not check:
            Game.objects.create(
                user_key=now_user_key,
                win=0,
                draw=0,
                lose=0
            )

        result = rcpgame(player_choice)
        if result == 'win':
            Game.objects.filter(user_key=now_user_key).update(win=F('win') + 1)
        elif result == 'draw':
            Game.objects.filter(user_key=now_user_key).update(draw=F('draw') + 1)
        elif result == 'lose':
            Game.objects.filter(user_key=now_user_key).update(lose=F('lose') + 1)

        return JsonResponse({
            'message': {
                'text': result + ' 현재 전적은 ' + str(Game.objects.get(user_key=now_user_key).win) + '승 ' + str(Game.objects.get(user_key=now_user_key).draw) + '무 ' + str(Game.objects.get(user_key=now_user_key).lose) + '패 입니다.'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['학식', '가위바위보 게임', '자기소개']
            }
        })

    elif player_choice == '자기소개':
        return JsonResponse({
            'message': {
                'text': '저를 소개하겠습니다'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['생일', '취미', '기억에 남는 학교 수업', '그만보기']
            }
        })

    elif player_choice == '생일':
        return JsonResponse({
            'message': {
                'text': '저의 생일은 2월 14일입니다! 초콜렛 선물은 그만 주세요 ★'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['저의 생일', '취미', '기억에 남는 학교 수업', '가위바위보 게임']
            }
        })

    elif player_choice == '취미':
        return JsonResponse({
            'message': {
                'text': '저는 게임을 좋아하지만, 직접하기보다는 유튜버들의 플레이를 감상하는 편입니다.'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['저의 생일', '취미', '기억에 남는 학교 수업', '가위바위보 게임']
            }
        })

    elif player_choice == '기억에 남는 학교 수업':
        return JsonResponse({
            'message': {
                'text': '생각해보니 들은 학교수업이 꽤 많군요... 다음 중 어느 과목의 후기가 궁금하신가요?'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['환경법', '법학과 졸업논문', '자료구조', '빅데이터', '그만보기']
            }
        })

    elif player_choice == '환경법':
        return JsonResponse({
            'message': {
                'text': '환경법은 법학과 수업중에서 가장 혁신적인(?)수업이었습니다. 법조문을 외우는 것이 아니라 세계 기후 협정과 각종 통계자료를 보며 환경 파괴가 얼마나 심각한지 느낄 수 있었습니다.'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['환경법', '법학과 졸업논문', '자료구조', '빅데이터', '그만보기']
            }
        })

    elif player_choice == '법학과 졸업논문':
        return JsonResponse({
            'message': {
                'text': '이건 수업은 아닌데, 그냥 기억에 남아 포함시켰습니다. 저는 남소방지를 위한 무고죄의 개정방안에 대해서 연구했었는데요, 참고할만한 논문이 별로 없어서 고생한 기억이 나네요 ...'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['환경법', '법학과 졸업논문', '자료구조', '빅데이터', '그만보기']
            }
        })

    elif player_choice == '자료구조':
        return JsonResponse({
            'message': {
                'text': '저는 프로그래밍에 입문한 언어가 자바여서 포인터라는 개념을 몰랐습니다. 그런데 자료구조 과목에서는 C언어의 포인터를 이용하여 구현하다보니 애를 먹었던 기억이 있네요.'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['환경법', '법학과 졸업논문', '자료구조', '빅데이터', '그만보기']
            }
        })

    elif player_choice == '빅데이터':
        return JsonResponse({
            'message': {
                'text': '빅데이터 과목에서는 교수님이 강의를 하는게 아니라 현업에 있는 실무진들을 초청하여 강의를 듣게 했습니다. 다양한 회사의 실무진들의 이야기를 들으면서 데이터마이닝, AI가 재미있을것 같다는 생각이 들게해준 과목입니다. '
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['환경법', '법학과 졸업논문', '자료구조', '빅데이터', '그만보기']
            }
        })

import json, datetime
from kakaobot.models import Menu
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

def crawl(request):
    '''
    일단은 DB삭제하는걸로 구현해놓고, 완성한 후에 년월일로 필터링하여 출력하는 걸로... 그럼 식단 정보도 계속 저장됨.
    datetime.date.today().strftime("%Y년 %m월 %d일".encode('unicode-escape').decode()).encode().decode('unicode-escape')
    '''
    today = datetime.date.today().strftime("%Y년 %m월 %d일".encode('unicode-escape').decode()).encode().decode(
        'unicode-escape')
    menu_db = Menu.objects.filter(date=today)
    # 최신상태유지위해 해당 날짜의 DB만 삭제해보자.
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

    employee_house = trs[2]
    tds = employee_house.find_all('td')
    employee_house_menu = tds[date_number + 1].get_text()
    create_menu_db('교직원_집밥', employee_house_menu,today)

    employee_oneplate = trs[4]
    tds = employee_oneplate.find_all('td')
    employee_oneplate_menu = tds[date_number + 1].get_text()
    create_menu_db('교직원_한그릇', employee_oneplate_menu,today)

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

#DB에 저장해주는 녀석
def create_menu_db(cafe_name, menu,today):
    Menu.objects.create(
        cafe_name=cafe_name,
        menu=menu,
        date=today
    )
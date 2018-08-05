import datetime
from kakaobot.models import Menu

## 누른 버튼의 이름을 파라미터로 받아 DB에서 메뉴를 가져옴.
def get_menu(cafeteria_name):
    today = datetime.date.today().strftime("%Y년 %m월 %d일".encode('unicode-escape').decode()).encode().decode(
        'unicode-escape')
    today_menu = Menu.objects.filter(date=today)
    if cafeteria_name == '상록원':
        sangrock_rice = today_menu.get(cafe_name='상록원_백반코너').menu
        sangrock_oneplate= today_menu.get(cafe_name='상록원_일품코너').menu
        sangrock_cutlet = today_menu.get(cafe_name='상록원_양식코너').menu
        sangrock_head = today_menu.get(cafe_name='상록원_뚝배기코너').menu

        return "------------\n" +  "백반코너 \n" + sangrock_rice \
               + "------------\n" + "일품코너 \n" + sangrock_oneplate \
               + "------------\n" + "양식코너 \n" + sangrock_cutlet \
               + "------------\n" + "뚝배기코너 \n" + sangrock_head

    elif cafeteria_name == '그루터기':
        tree_A = today_menu.get(cafe_name='그루터기_A코너').menu
        tree_B=today_menu.get(cafe_name='그루터기_B코너').menu

        return "------------\n" + "A코너 \n" + tree_A \
               + "------------\n" + "B코너 \n" + tree_B

    elif cafeteria_name == '기숙사식당':
        dorm = today_menu.get(cafe_name='기숙사_A코너').menu

        return "------------\n" + "A코너 \n" + dorm

    elif cafeteria_name == '교직원식당':
        employee_house = today_menu.get(cafe_name='교직원_집밥').menu
        employee_oneplate = today_menu.get(cafe_name='교직원_한그릇').menu

        return "------------\n" + "집밥 \n" + employee_house \
               + "------------\n" + "한그릇 \n" + employee_oneplate
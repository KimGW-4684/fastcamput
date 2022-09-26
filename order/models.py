from django.db import models

class Shop(models.Model):
    shop_name = models.CharField(max_length=20)
    shop_address = models.CharField(max_length=40)

class Menu(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    # 메뉴 테이블에서는 각각의 메뉴가 하나의 상점에 종속이 되니까 외래키 칼럼키 넣어줌.
    food_name = models.CharField(max_length=20)
    # 메뉴 테이블 안에는 1번 shop 에 해당하는 여러 개의 행이 있을 수 있음.

class Order(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    # 외래키로 shop table 받아오기

    order_date = models.DateTimeField('date ordered')
    address = models.CharField(max_length=40)
    estimated_time = models.IntegerField(default=-1)
    # 배송 예상 시간
    # 사장님이 예상 시간 입력하기 전에는 기본값 -1 로 설정

    deliver_finish = models.BooleanField(default=0)
    # 배달 기사가 배달 완료했다는 상태 보여줌

class Orderfood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # order table 을 외래키로 받음

    food_name = models.CharField(max_length=20)
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from order.models import Shop, Menu, Order, Orderfood
from order.serializer import ShopSerializer, MenuSerializer

@csrf_exempt
def shop(request):
    if request.method == 'GET':
       # shop = Shop.objects.all()
       # serializer = ShopSerializer(shop, many=True)
       # return JsonResponse(serializer.data, safe=False)
    # request.method == 'GET' 이면 shop db 에 모든 object는 다 shop에 저장을 하고,
    # 그 데이터들을 serializer 을 통해 json 형식으로 파싱(변환)해줌.

       shop = Shop.objects.all()
       return render(request, 'order/shop_list.html',{'shop_list':shop})

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ShopSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def menu(request, shop):
    if request.method == 'GET':
        menu = Menu.objects.filter(shop=shop)
        #serializer = MenuSerializer(menu, many=True)
        # many=True : '메뉴' 라는 데이터가 여러 개여도 상관을 안하겠다. 라는 의미, 없애면 상관을 하겠다
        #return JsonResponse(serializer.data, safe=False)
        return render(request, 'order/menu_list.html', {'menu_list': menu,'shop':shop})

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MenuSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

from django.utils import timezone

@csrf_exempt
def order(request):
    if request.method == 'POST':
        address = request.POST['address']
        shop = request.POST['shop']
        order_date = timezone.now()
        food_list = request.POST.getlist('menu')

        shop_item = Shop.objects.get(pk=int(shop))

        shop_item.order_set.create(address=address, order_date=order_date, shop=int(shop))

        order_item = Order.objects.get(pk=shop_item.order_set.latest('id').id)

        for food in food_list:
            order_item.orderfood_set.create(food_name=food)

        # return HttpResponse(status=200)
        return render(request, 'order/success.html')

    elif request.method == 'GET':
        order_list = Order.objects.all()
        return render(request, 'order/order_list.html', {'order_list': order_list})
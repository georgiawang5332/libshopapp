from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from store.models import *
from .utils import cookieCart, cartData, guestOrder
# from django .contrib.auth.decorators import login_required


# Create your views here.
# @receiver(sender=User) # @login_required

# 如何設置視圖以使用數據值並調用購物車數據功能 我們可以使用購物車數據 會在views這邊導入
# 所以store cart checkout 會刪除(viewsssss->views內容)變成
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {
        'products': products,
        'cartItems': cartItems,
    }
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

# 以下被刪除了
#         try:
#             cart = json.loads(request.COOKIES['cart'])
#         except:
#             cart = {}
#         print('Cart: ', cart)
#         items = []
#         order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
#         cartItems = order['get_cart_items']
#
#         for i in cart:
#             try:#如果我在後台刪除一個商品，此時我在畫面上會出錯所以必須添加try...
#                 cartItems += cart[i]["quantity"]
#                 product = Product.objects.get(id=i)
#                 total = (product.price * cart[i]["quantity"])
#
#                 order['get_cart_total'] += total
#                 order['get_cart_items'] += cart[i]["quantity"]
#
#                 item = {
#                     'product': {
#                         'id': product.id,
#                         'name': product.name,
#                         'price': product.price,
#                         'imageURL': product.imageURL,
#                         },
#                     'quantity': cart[i]['quantity'],
#                     'get_total': total,
#                 }
#                 items.append(item)  # 上面的->items = []
#
#                 if product.digital == False:
#                     order['shipping'] = True
#             except:
#                 pass
    #以上被刪除了

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

#
# def checkout(request):
#     data = cartData(request)  # cookiesData 量改為數據變 -> cookieData = cookieCart(request)
#     cartItems = data['cartItems']  # cartItems = cookieData['cartItems']
#     order = data['order']  # order = cookieData['order']
#     items = data['items']  # items = cookieData['items']
#
#     context = {'items': items, 'order': order, 'cartItems': cartItems}
#     return render(request, {{store: checkout}}, context)
#
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    #
    # data = cartData(request)
    #
    # cartItems = data['cartItems']
    # order = data['order']
    # items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)

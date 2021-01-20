import json
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


def cookieCart(request):
    # Create empty cart for now for non-logged in user
    # 現在為未登錄的用戶創建空購物車
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print('CART:', cart)

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        # We use try block to prevent items in cart that may have been removed from causing error
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'id': product.id,
                'product':
                    {
                        'id': product.id, 'name': product.name, 'price': product.price,
                        'imageURL': product.imageURL},
                'quantity': cart[i]['quantity'],
                'digital': product.digital, 'get_total': total,
            }

            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}


# @login_required(login_url='login') # 會檢測使用者是否已經登入，若已登入才會執行 cartData() 的程式
def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        # customer = Customer.objects.filter(user=request.user)
        # customer = get_object_or_404(Customer, user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # cookieData = cookieCart(request)
        # cartItems = cookieData['cartItems']
        # order = cookieData['order']
        # items = cookieData['items']
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        print('CART:', cart)
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
        cartItems = order['get_cart_items']

        for i in cart:
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
    #         登入用戶 可以轉到購物車頁面 總數就更新了


    return {'cartItems': cartItems, 'order': order, 'items': items}


def guestOrder(request, data):
    print('User is not logged in ...')
    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )
    return customer, order

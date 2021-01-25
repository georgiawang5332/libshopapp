import datetime
import json

from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ProductForms
from .models import *
from .models import Product
from .utils import cartData, guestOrder


def productCreate(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = ProductForms(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()  # 這樣就可以儲存了
        # message success
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully Created")

    # 購物車購買數量
    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        "form": form,
        'cartItems': cartItems,
    }
    return render(request, "store/form.html", context)


# def productUpdate(request, id=None):
#     # basic use permissions 基本使用權限
#     if not request.user.is_staff or not request.user.is_superuser:
#         raise Http404
#
#     context = {}
#     if request.POST:
#         form = ProductForms(request.POST)
#         if form.is_valid():
#             instance = get_object_or_404(Product, id=id)
#             form = ProductForms(data=request.POST, instance=instance)
#             form.save()
#             # updating our context
#             context.update({'instance': instance})
#             # message success
#             messages.success(request, "<a href='#'>Item</a> Saved",
#                              extra_tags='html_safe')
#             return HttpResponseRedirect(instance.get_absolute_url())
#
#     else:
#         form = ProductForms()  # if request isn't POST we initialize an empty form
#
#     data = cartData(request)
#     cartItems = data['cartItems']
#
#     context.update({
#         'form': form,
#         'cartItems': cartItems,
#     })
#     return render(request, 'store/form.html', context)


# def productUpdate(request, id=id):
#     if request.method == 'POST':
#         instance = Product.objects.get(Product, id=id)
#         form = ProductForms(request.POST or None, instance=instance)
#         if request.method == 'POST':
#             form = ProductForms(request.POST, instance=instance)
#             if form.is_valid():
#                 form.save()
#                 # return HttpResponseRedirect(instance.get_absolute_url())
#                 return redirect('/')

def productUpdate(request, id=None):
    # 購物車購買數量
    data = cartData(request)
    cartItems = data['cartItems']

    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404

    instance = get_object_or_404(Product, id=id)
    form = ProductForms(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # message success
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'instance': instance,
        'form': form,
        'cartItems': cartItems,
    }
    return render(request, 'store/form.html', context)


def productDelete(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Product, id=id)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("store:store")


def productDetail(request, id=None):
    data = cartData(request)
    instance = get_object_or_404(Product, id=id)
    cartItems = data['cartItems']

    context = {
        'instance': instance,
        'cartItems': cartItems
    }
    return render(request, "store/detail.html", context)


def searchbar(request):
    searchNum = Product.objects.all().count()
    data = cartData(request)
    cartItems = data['cartItems']

    if request.method == 'GET':
        searchNum = request.GET.get('search').count
        search = request.GET.get('search')
        product = Product.objects.all().filter(name=search)
        # searchNum = Product.objects.all().count(number=searchNum)

        context = {
            'searchNum': searchNum,
            'product': product,
            'cartItems': cartItems
        }

        return render(request, 'store/searchbar.html', context)


# -----------------------------------------------------------

def store(request):
    products = Product.objects.all()  # .order_by("-timestamp")

    paginator = Paginator(products, 25)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    try:
        queryset = paginator.page(page_obj)
    except PageNotAnInteger:
        queryset = paginator.page(1)

    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    #
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        # new
        'object_list': queryset,
        'page_obj': page_obj,
        'queryset': queryset,
        #
        'products': products,
        'cartItems': cartItems,
    }
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

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

    return JsonResponse('付款已提交/Payment submitted..', safe=False)

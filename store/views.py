import datetime
import json

from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ProductForms
from .models import *
from .utils import cartData, guestOrder

from django.utils import timezone


def productCreate(request):
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    form = ProductForms(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()  # 這樣就可以儲存了
        # message success
        messages.success(request,
                         "<div id='msg' class='alert alert-success' role='alert'><strong>Success!</strong>Successfully Created.</div>",
                         extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    # else:
        # messages.error(request, "Not successfully Created")

    # 購物車購買數量
    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'title': '建立商品',
        "form": form,
        'cartItems': cartItems,
    }
    return render(request, 'store/form.html', context)


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
        # messages.info(request, 'this is a info message!')
        # messages.error(request, 'ERROR!ERROR!')
        # messages.warning(request, 'Be careful!!!')
        messages.success(request,
                         "<div id='msg' class='alert alert-success col-lg-12' role='alert'><strong>Success!</strong>Success Saved for your edit.</div>",
                         extra_tags='html_safe')
        # messages.success(request, "<a href='#'><strong>疑問通知</strong></a> Success Saved thank you for add join", extra_tags='html_safe')
        # messages.success(request,"{% if messages %}<div class='row'><div class='col-sm-6 col-sm-offset-3'>{% for message in messages %}<div class='alert alert-{{ message.tags }} alert-dismissible fade show' role='alert'>{{ message }}<button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button></div>{% endfor %}</div></div>{% endif %}", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    # else:
    #     #error message success
    #     messages.success(request, "<a href='#'>通知作者</a> 錯誤儲存 ", extra_tags='html_safe')

    context = {
        'title':'商品編輯',
        'instance': instance,
        'form': form,
        'cartItems': cartItems,
    }
    return render(request, 'store/form.html', context)


# def productDelete(request, id=None):
#     if not request.user.is_staff or not request.user.is_superuser:
#         raise Http404
#     instance = get_object_or_404(Product, id=id)
#     instance.delete()
#     messages.success(request, "Successfully deleted")
#     return redirect("store:store")

def productDelete(request, id=None):
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    obj = get_object_or_404(Product, id=id)
    # "POST" request
    if request.method == "POST":
        # confirming del
        obj.delete()
        return redirect('../../')
    context = {
        'title': '刪除商品',
        "object": obj,
    }
    return render(request, 'store/delete.html', context)

def productDetail(request, id=None):
    instance = get_object_or_404(Product, id=id)
    if instance.draft or instance.timestamp > timezone.now():
        # 登入並且是員工狀況下，就會看到草稿中商品，如果不是員工則看不到。
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'name': instance.name,
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
            'title': '搜尋商品',
            'searchNum': searchNum,
            'product': product,
            'cartItems': cartItems
        }
        return render(request, 'store/searchbar.html', context)


# -----------------------------------------------------------
def store(request):
    today = timezone.now().date()
    # products = Product.objects.filter(draft=False).filter(timestamp__lte=timezone.now())#all()  # .order_by("-timestamp")
    products = Product.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        products = Product.objects.all()

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
        'title': '商品首頁',
        # new
        'object_list': queryset,
        'page_obj': page_obj,
        'queryset': queryset,
        #
        "today": today,
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

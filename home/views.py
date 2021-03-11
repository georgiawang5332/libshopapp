from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# def login(request):
#
#     context = {
#         'title': '登入',
#     }
#
#     return render(request, 'registration/login.html', context=context)

def index(request):
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'title': '首頁',
        'num_visits': num_visits,
    }
    # return HttpResponse("hello world!")
    # return render(request, 'index.html')
    # return render(request, 'registration/login.html')
    # setting = Setting.objects.get(pk=1)
    return render(request, 'index.html', context=context)

def contact(request):
    # return HttpResponse("hello world!")
    return render(request, 'home/contact.html')

def aboutview(request, *args, **kwargs):
    my_context ={
        "my_text": "this is about us",
        "my_num":  123,
        "my_list":  ["左三圈", 456, 7899],
    }
    return render(request, "home/about.html", my_context)

def socialview(request, *args, **kwargs):
    return HttpResponse("<h5> Socail Page </h5>")
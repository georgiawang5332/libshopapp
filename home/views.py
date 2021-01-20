from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    # return HttpResponse("hello world!")
    # return render(request, 'index.html')
    # return render(request, 'registration/login.html')
    # setting = Setting.objects.get(pk=1)
    return render(request, 'index.html')

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
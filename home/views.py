from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from .forms import RegisterForm
from django.core.mail import send_mail

# Create your views here.
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, authenticate


def email(request):
    subject = '感謝您註冊到我們的網站 / Thank you for registering to our site'
    message = '對我們來說意味著一個世界 / it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['receiver@gmail.com', ]  # recipient_list:收件人清單
    send_mail(subject, message, email_from, recipient_list)
    return redirect('redirect to a new page') #重定向到新頁面


def secretPage(request):
    context = {}
    return render(request, 'registration/secretPage.html', context)


def register(request):  # 20210325
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print("Errors", form.errors)
        if form.is_valid():
            form.save()
            #
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')

            user = authenticate(username=username, password=raw_password, first_name=first_name, last_name=last_name,
                                email=email)
            login(request, user)
            #
            print('user created!!!')
            messages.success(request, 'Account created successfully')
            return render(request, 'index.html')
        else:
            messages.success(request, 'Account created " NOT " successfully')
            context = {'form': form}
            return render(request, 'registration/signup.html', context)
    else:
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'registration/signup.html', context)


@csrf_protect
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
    my_context = {
        "my_text": "this is about us",
        "my_num": 123,
        "my_list": ["左三圈", 456, 7899],
    }
    return render(request, "home/about.html", my_context)


def socialview(request, *args, **kwargs):
    return HttpResponse("<h5> Socail Page </h5>")

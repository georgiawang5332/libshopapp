from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class RegisterForm(UserCreationForm):#20210325
    # first_name = forms.CharField(
    #     max_length=30,
    #     required=False,
    #     help_text='*必填',
    #     label="姓",
    # )
    # last_name = forms.CharField(
    #     max_length=30,
    #     required=False,
    #     help_text='*必填',
    #     label="名字",
    # )
    email = forms.CharField(
        max_length=254,
        help_text='*必填。 通知有效的電子郵件地址。',
        label="電子郵件",
    )

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("密碼不匹配")

        return password2

    class Meta:
        model = User
        fields = ["username", "email", 'password1', 'password2'] #, 'first_name', 'last_name'

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['first_name'],
            self.cleaned_data['last_name'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
            self.cleaned_data['password2'],
        )
        return user

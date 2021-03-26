from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Create your forms here.

class RegisterForm(UserCreationForm):#20210325
    # email = forms.EmailField(required=True)
    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='*必填。郵寄、付款需真實姓名。',
        label="名字",
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='*必填。郵寄、付款需真實姓名。',
        label="姓氏",
    )
    email = forms.CharField(
        required=True,
        max_length=254,
        help_text='*必填。 通知有效的電子郵件地址。',
        label="電子郵件",
    )

    class Meta:
        model = User
        fields = (
            'username',
            'last_name',
            'first_name',
            'email',
            'password1',
            'password2',
        ) #, 'first_name', 'last_name'

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
           user.save()
        return user

    # def clean_username(self):
    #     username = self.cleaned_data['username'].lower()
    #     r = User.objects.filter(username=username)
    #     if r.count():
    #         raise ValidationError("Username already exists")
    #     return username
    #
    # def clean_email(self):
    #     email = self.cleaned_data['email'].lower()
    #     r = User.objects.filter(email=email)
    #     if r.count():
    #         raise ValidationError("Email already exists")
    #     return email
    #
    # def clean_password2(self):
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')
    #
    #     if password1 and password2 and password1 != password2:
    #         raise ValidationError("密碼不匹配")
    #
    #     return password2



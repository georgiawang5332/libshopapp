from django import forms

from .models import Product, RegistrationData


class ProductForms(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'price',
            'draft',
            'digital',
            'image',
            'width_field',
            'height_field',
            'content',
        ]


class RegistrationModelProductForm(forms.Form):
    title = forms.CharField(label='',
                            widget=forms.TextInput(attrs={"placeholder": "Your title"}))
    email = forms.EmailField()
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Your description",
                "class": "new-class-name two",
                "id": "my-id-for-textarea",
                "rows": 20,
                'cols': 120
            }
        )
    )
    price = forms.DecimalField(initial=199.99)

    class Meta:
        model = RegistrationData
        fields = [
            'email',
        ]
        widgets = {
            'email':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'email',
            }),
        }
    def clean_email(self, *args, **kwargs):
        email = self.clean_data.get("email")
        if not email.endswith("gmail"):
            raise forms.ValidationError("this is not a valid email")
        return email

    # def clean_title(self, *args, **kwargs):
    #     title = self.clean_data.get("title")
    #     if "CEF" in title:
    #     if not "CEF" in title:
    #         return title
    #     else:
    #         return title
    #         or
    #         raise forms.ValidationError("This is not a valid title")
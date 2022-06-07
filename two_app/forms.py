from django import forms
from two_app.models import Shop


class ShopNameForm(forms.ModelForm):
    class Meta:
        model=Shop
        fields = ['shop_name']

        widgets = {
            'shop_name': forms.TextInput(attrs={'size':'40'}),
        }
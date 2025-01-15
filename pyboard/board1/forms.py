# forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','user', 'content']

class StockForm(forms.Form):
    symbol = forms.CharField(max_length=100)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
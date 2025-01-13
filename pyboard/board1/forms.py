# forms.py
from django import forms
from .models import Post,Event

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','user', 'content']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
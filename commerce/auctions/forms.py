from cProfile import label
from django import forms

class comment_form(forms.Form):
    comment = forms.CharField(widget=forms.textarea)
    your_name = forms.CharField(label='Your name', max_length=100)

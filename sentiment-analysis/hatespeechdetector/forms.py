from django import forms

class QueryForm(forms.Form):
    query = forms.CharField(label='search tweets', max_length=100)
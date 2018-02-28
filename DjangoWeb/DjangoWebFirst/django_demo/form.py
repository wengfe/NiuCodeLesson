from django import forms


class CommentForm(forms.Form):
    comment = forms.CharField()
    name = forms.CharField(max_length=50)

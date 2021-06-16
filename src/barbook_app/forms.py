from django import forms

from barbook_app.models import Message
from barbook_app.models.user import BarbookUser


class RegistrationForm(forms.Form):
    email = forms.EmailField(max_length=50)
    role = forms.CharField(max_length=50, required=False)
    img = forms.ImageField(required=False)
    name = forms.CharField(max_length=255)
    second_name = forms.CharField(max_length=255, required=False)
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)


class AuthForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=50, required=True)


class LikeForm(forms.Form):
    user_id = forms.IntegerField()
    cockt_id = forms.IntegerField()


class CryForHelpForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("message_text", "author_email", "author_name")


class CommentForm(forms.Form):
    user_id = forms.IntegerField()
    cocktail_id = forms.IntegerField()
    text = forms.CharField(max_length=200)


class EmailForDroppingPassword(forms.Form):
    email = forms.EmailField(required=True)


class NewPassword(forms.Form):
    password = forms.CharField(max_length=255, required=True)

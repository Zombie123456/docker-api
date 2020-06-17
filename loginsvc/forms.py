from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=32, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class RetSetPassword(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True, min_length=5, max_length=16)
    con_password = forms.CharField(widget=forms.PasswordInput, required=True)

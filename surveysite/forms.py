from django import forms

class Loginform(forms.Form):
    name = forms.CharField(label='your name', max_length=128)
    password = forms.CharField(widget=forms.PasswordInput())

class Registerform(forms.Form):
    name = forms.CharField(label='your name', max_length=128)
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(label='your email')

class CreateSurveyForm(forms.Form):
    question = forms.CharField(label="Question",widget=forms.Textarea(attrs={'class':'form-control'}))

class FindUniqueIDForm(forms.Form):
    unique_id = forms.CharField(max_length=6) 

class ResponseForm(forms.Form):
    response = forms.CharField(label="Your response", widget=forms.Textarea(attrs={'class':'form-control'}))
    
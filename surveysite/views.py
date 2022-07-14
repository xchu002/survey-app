from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from . import forms, models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
import random
import nltk
from nltk.stem import WordNetLemmatizer
import datetime
from django.utils import timezone
import schedule

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Create your views here.


def delete():
    for survey in models.Survey.objects.all():
        if type(survey.expiry_date) == type(timezone.now()):
            if survey.expiry_date < timezone.now():
                survey.delete()
delete()



def create_number(user):
    numbers = [0,1,2,3,4,5,6,7,8,9]
    session_id = "No ID"
    survey_objects = models.Survey.objects.filter(user=user)
    number_of_surveys = len(survey_objects)

    number_found = False

    while number_found == False:
        #if more than 99 surveys, then can stop generate numbers and make a warning
        if len(survey_objects) >= 999999:
            session_id = "memory exceeded"
            print("memory exceeded")
            break
        #create numbers
        session_id = ""
        for i in range(6):
            session_id += str(random.choice(numbers))
        #check if number is in survey already. if already used, return to top of while loop again
        count = 0

        if number_of_surveys == 0:
            return session_id

        for survey in survey_objects:
            count += 1
            if survey.unique_id == session_id:
                count = 0
                break
        # if no repeats found, then close while loop
        if count == number_of_surveys:
            number_found = True
    
    return session_id
        



def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    session_id = create_number(request.user)

    surveys = models.Survey.objects.filter(user=request.user)      
    return render(request, "surveysite/index.html", {
        "name":request.user.username,
        "surveys": surveys,
        "session_id": session_id
    })


def create(request, session_id):
    if request.user.username == "test_length":
        for i in range(50):
            session_id = create_number(request.user)
            if session_id == "memory exceeded":
                break
            survey = models.Survey(unique_id=session_id,user=request.user,survey_question="Dummy ques")
            print(survey.unique_id)
            survey.save()
    if session_id == "memory exceeded":
        return HttpResponseRedirect('warning')

    print(f"session id 1: {session_id}")
    if request.method == "POST" and request.user.username != "test_length":
        create_form = forms.CreateSurveyForm(request.POST)
        if create_form.is_valid():
            question = create_form.cleaned_data["question"]
            print(f"session id 2: {session_id}")
            survey = models.Survey(unique_id=session_id,user=request.user,survey_question=question,expiry_date=timezone.now() + datetime.timedelta(days=365))
            survey.save()
            return HttpResponseRedirect(reverse('index'))

    print(f"session id 3: {session_id}")

    create_form = forms.CreateSurveyForm()
    return render(request, "surveysite/create.html", {
        "unique_id": session_id,
        "create_form": create_form,
    })

def warning(request):
    return render(request, "surveysite/warning.html", {})

def login_view(request):
    login_form = forms.Loginform()
    session_form = forms.FindUniqueIDForm()
    found = False
    if request.method == "POST":
        login_form  = forms.Loginform(request.POST)
        session_form = forms.FindUniqueIDForm(request.POST)

        if login_form.is_valid():
            name = login_form.cleaned_data["name"]
            password = login_form.cleaned_data["password"]
            user = authenticate(request, username=name, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            elif not user:
                return render(request, "surveysite/login.html", {
                    "invalid": "Invalid Credentials",
                    "login_form": login_form,
                    "session_form": session_form
                })

        session = ""
        if session_form.is_valid():
            session = session_form.cleaned_data["unique_id"]

            for survey in models.Survey.objects.all():
                if session == survey.unique_id:
                    found = True
        if found == True:
            return redirect(response, session=session)
        elif found ==  False:
            return render(request, "surveysite/login.html", {
                "session": "Cannot find session.",
                "login_form": login_form,
                "session_form": session_form
            })


    return render(request, "surveysite/login.html", {
        "login_form": login_form,
        "session_form": session_form,
    })

def response(request, session):
    response = ''
    survey = models.Survey.objects.get(unique_id=session)
    question = survey.survey_question
    if "submit" in request.POST:
        response_form = forms.ResponseForm(request.POST)
        if response_form.is_valid():
            response = response_form.cleaned_data["response"]
            response = models.Response(question=survey, answer=response)
            response.save()
            return HttpResponseRedirect(reverse('login'))
    elif "cancel" in request.POST:
        return HttpResponseRedirect(reverse(login))
    response_form = forms.ResponseForm()
    return render(request, "surveysite/response.html", {
        "session": session,
        "question": question,
        "response_form": response_form,
        "response": response
        })

def analytics(request, session):
    lemmatizer = WordNetLemmatizer()
    survey = models.Survey.objects.get(unique_id=session)
    expiry_date = survey.expiry_date
    question = survey.survey_question
    answers = survey.answers.all()
    word_list_unprocessed = []
    word_list_processed = []
    vocabs = []
    punctuations = [",",".","?","!","(",")","-","+","=","/"]
    for answer in answers:
        word_list_unprocessed.extend(nltk.tokenize.word_tokenize(answer.answer))
    for word in word_list_unprocessed:
        if word not in punctuations:
            word_list_processed.append(lemmatizer.lemmatize(word.lower()))
    vocabs = sorted(list(set(word_list_processed)))
    analysis_dict = {}
    for vocab in vocabs:
        count = 0
        for word in word_list_processed:
            if word == vocab:
                count += 1
        analysis_dict[vocab] = str(round(count / len(word_list_processed) * 100, 2)) + "%"
    return render(request, "surveysite/analytics.html", {
        "session": session,
        "question": question,
        "answers": answers,
        "dictionary": analysis_dict,
        "expiry": expiry_date
    })

def register(request):
    if request.method == "POST":
        form = forms.Registerform(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            password = form.cleaned_data["password"]
            password_confirm = form.cleaned_data["password_confirm"]
            email = form.cleaned_data["email"]
            #check if user exists already
            exists = False
            for user in User.objects.all():
                if name == user.username:
                    exists = True
            if exists == True:
                form = forms.Registerform()
                return render(request, "surveysite/register.html", {
                    "invalid": "User Already Exists. Sign up using a different username",
                    "form": form
                })
            else:
                if password == password_confirm:
                    User.objects.create_user(username=name, email=email, password=password)
                    user = authenticate(request, username=name, password=password)
                    if user:
                        login(request, user)
                        return HttpResponseRedirect(reverse('index'))
    else:
        form = forms.Registerform()

    return render(request, "surveysite/register.html", {
        "form": form
    })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))
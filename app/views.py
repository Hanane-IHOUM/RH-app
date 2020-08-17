from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from app.forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
import PyPDF2
import io
from io import StringIO
import re
import nltk
#import spacy
import os
import pymongo
from pymongo import MongoClient
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords 
from nltk.stem.snowball import FrenchStemmer
from nltk.util import ngrams
import nltkdownload


cluster = MongoClient("mongodb+srv://amine1:thebestof*@cluster0.mvqg4.mongodb.net/rh?retryWrites=true&w=majority") 
db = cluster["rh"]
collection = db["cv"]
User = get_user_model()


def remove_SpeChar(text):
    tokenizer = RegexpTokenizer(r'\w+')
    text = tokenizer.tokenize(text)
    text = " ".join(text)
    return text


def remove_StopWords(text):
   text_tokens = word_tokenize(text)
   tokens_without_sw = [word for word in text_tokens if not word in stopwords.words('french')]
   text = " ".join(tokens_without_sw)
   return text


def get_lem(text):
    stemmer = FrenchStemmer()
    text_tokens = word_tokenize(text)
    text =""
    for word in text_tokens :
        text += " "+stemmer.stem(word)
    return text


def get_low(text):
    return text.lower()


def unigram(text):
    uni = word_tokenize(text)
    return uni 


def bigram(unig):
    #bi = list(nltk.bigrams(text.split()))
    bi = list(ngrams(unig,2))
    return bi


def trigam(unig):
    trigam_string=[]
    phrase=""
    tri = list(ngrams(unig,3))
    for liste in tri :
        for mot in liste:
            phrase = phrase + mot + " "
        trigam_string.append(phrase)
        phrase =""   
    return trigam_string         



# Create your views here.
@login_required(login_url='/login/')
def index(request):
    return render(request, 'app/index.html', {})


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        'form': form
    }
    print(request.user.is_authenticated)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            print("error.......")

    return render(request, "auth/login.html", context=context)


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        'form': form,
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password_first")
        new_user = User.objects.create_user(username, email, password)
    return render(request, "auth/register.html", context=context)


def logout_page(request):
    print(request)
    logout(request)
    return redirect('/')


def profil_page(request):
    if request.method=="POST":
        if request.FILES['cv']:  
            pdfFileObj = request.FILES['cv'].read() 
            pdfReader = PyPDF2.PdfFileReader(io.BytesIO(pdfFileObj))
            NumPages = pdfReader.numPages
            i = 0
            cv = ""
            while (i<NumPages):
                text = pdfReader.getPage(i)
                cv = cv +"/n"+ text.extractText()
                i +=1
            #print(cv)
            text_extracted = cv
            cv = remove_SpeChar(cv)
            cv = remove_StopWords(cv) 
            #cv = get_lem(cv)
            cv = get_low(cv)
            unigra = unigram(cv)
            bigra = bigram(unigra)
            trigra = trigam(unigra)
            print(trigra)
            post = {
                    "text_extracted": text_extracted,
                    "text_without_SC_SW_Stemm": cv,
                    "unigram": unigra,
                    "bigram": bigra,
                    "trigam": trigra
                    }
            collection.insert_one(post)

    return render(request, "app/profil.html")

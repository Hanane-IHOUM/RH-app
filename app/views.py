from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from app.forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
import PyPDF2
import io
from io import StringIO
import re
import nltk
import spacy
import os
nlp = spacy.load("en_core_web_md")

def remove_SpeChar(text):
    text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text, flags=re.MULTILINE)
    text = re.sub('\S*@\S*\s?', '', text)
    text = re.sub('\[.*?\]', '', text)
    text = re.sub(r'[^\w]', ' ', text)
    text = re.sub('[!"#$%&()*+,./:;<=>?@[\]^_`{|}~‘’•]', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = " ".join(text.split())
    return text


def remove_StopWords(text):
    sentence = nlp(text)
    filtered_sentence = ''
    token_list = []
    for token in sentence : 
        token_list.append(token.text)
    for word in token_list:
        lexeme = nlp.vocab[word]
        if lexeme.is_stop == False :
            filtered_sentence += ' '+word
    return filtered_sentence


def get_lem(text):
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    return text

def remove_Ent(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'DATE' : 
            text = re.sub(ent.text,' ',text)
        elif ent.label_ == 'PERSON' : 
            text = re.sub(ent.text,' ',text)
        elif ent.label_ == 'GPE' : 
            text = re.sub(ent.text,' ',text)
        
    return text

def get_low(text):
    return text.lower()
            


User = get_user_model()

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
            print(cv)

    return render(request, "app/profil.html")

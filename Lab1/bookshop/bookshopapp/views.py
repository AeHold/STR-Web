from django.shortcuts import render, redirect
from django.views import View
from bookshopapp.forms import SignUpForm, LoginForm
import bookshopapp.models as models
import datetime
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
import requests
import json

class AboutUsView(View):
    def get(self, req, *args, **kwargs):
        return render(req,'bookshop/about.html',{})

class FAQView(View):
    def get(self, req, *args, **kwargs):
        return render(req,'bookshop/faq.html',{})

class ContactsView(View):
    def get(self, req, *args, **kwargs):
        return render(req,'bookshop/contacts.html',{})

class NewsView(View):
    def get(self, req, *args, **kwargs):
        return render(req,'bookshop/news.html',{})

class ReviewView(View):
    def get(self, req, *args, **kwargs):
        return render(req,'bookshop/review.html',{})

class PrivacyPolicyView(View):
    def get(self, req, *args, **kwargs):
        return render(req,'bookshop/privacypolicy.html',{})

class ShopView(View):
    def get(self, req, *args, **kwargs):
        return render(req,'bookshop/privacypolicy.html',{})


class MainView(View):
    def get(self, req, *args, **kwargs):
        if(req.user.is_anonymous):
            cat = requests.get("https://cataas.com/cat/says/Welcome to our bookshop")
        else:
            cat = requests.get("https://cataas.com/cat/says/You must work,{0} %0AWhy do you proCATstinating%3F".format(req.user.username))
        cat_fact = json.loads(requests.get("https://catfact.ninja/fact").content.decode())['fact']
        return render(req, 'bookshopapp/main.html', {'fact':cat_fact, "cat":cat})

class LoginView(View):
    form_class = LoginForm

    def post(self, req, *args, **kwargs):
        form = self.form_class(data = req.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            us = User.objects.filter(email=email)
            if len(us) != 0:

                user = authenticate(req, username =us[0].username ,email = email, password = password)
                if user is not None:
                    login(req, user)
                    return redirect('/')
                else:
                    return render(req, 'bookshopapp/login.html', {"form":form, "error":"User not found"})
            else:
                return render(req, 'bookshopapp/login.html', {"form":form, "error":"User not found"})

        else:
            return render(req, 'bookshopapp/login.html', {"form":form, "error":form.errors.values()})

    def get(self, req, *args, **kwargs):
        if(req.user.is_authenticated):
            return redirect('/')
        form = self.form_class()
        return render(req, 'bookshopapp/login.html', {"form":form})

class SignUpView(View):
    form_class = SignUpForm

    def post(self, req, *args, **kwargs):
        form = self.form_class(data = req.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(email=email, password=password, username=first_name + " " + last_name)
            models.Profile.objects.create(phone_number=phone_number, user=user, post = models.Post.objects.get(name='intern'))
            login(req, user)
            
            return redirect('/')

        else:
            return render(req, 'bookshopapp/sign-up.html', {"form":form, "errors":form.errors.values()})

    def get(self, req, *args, **kwargs):
        if(req.user.is_authenticated):
            return redirect('/')

        form = self.form_class()
        return render(req, 'bookshopapp/sign-up.html', {"form":form})

class ProfileView(View):
    def get(self, req, *args, **kwargs):
        user = req.user
        profile = models.Profile.objects.get(user=user)
        if(profile.post!=None):
            order = models.Order.objects.filter(is_send=False)
            return render(req, 'bookshopapp/stuffprofile.html', {"profile":profile, "orders":order})
        else:
            order = models.Order.objects.filter(is_recieved=False,user=user)
            return render(req, 'bookshopapp/profile.html', {"profile":profile, "orders":order})

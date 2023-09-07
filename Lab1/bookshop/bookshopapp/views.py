from django.shortcuts import render, redirect
from django.views import View
from bookshopapp.forms import SignUpForm, LoginForm
import bookshopapp.models as models
import datetime
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
import requests
import json

class MainView(View):
    def get(self, req, *args, **kwargs):
        if(req.user.is_anonymous):
            cat = requests.get("https://cataas.com/cat/says/Welcome to our bookshop")
        else:
            cat = requests.get("https://cataas.com/cat/says/You must work,{0} %0AWhy do you proCATstinating%3F".format(req.user.username))
        cat_fact = json.loads(requests.get("https://catfact.ninja/fact").content.decode())['fact']
        excursions = models.Excursion.objects.filter(date__date=datetime.datetime.today().date())
        return render(req, 'bookshopapp/main.html', {'fact':cat_fact, "cat":cat, "excursions":excursions})

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

class ExhibitionsView(View):
    def get(self, req, *args, **kwargs):
        exhibitions = models.Exhibition.objects.all()
        return render(req, 'bookshopapp/exhibitions.html', {"exhibitions":exhibitions})

class ProfileView(View):
    def get(self, req, *args, **kwargs):
        user = req.user
        profile = models.Profile.objects.get(user=user)
        exponates = profile.exponates.all()
        cat = requests.get("https://cataas.com/cat/says/Hi,{0}".format(user.username))
        excursions = models.Excursion.objects.filter(guide=profile, date__gte=datetime.datetime.today())
        return render(req, 'bookshopapp/profile.html', {"profile":profile, "exponates":exponates, "excursions":excursions,"cat":cat})

class ScheduleView(View):
    def get(self, req, *args, **kwargs):
        exhibitions = models.Exhibition.objects.all()
        excursions = models.Excursion.objects.filter(date__gte=req.GET.get("dfrom") if req.GET.get("dfrom",'')!=''
                else datetime.datetime.today(), date__lte=req.GET.get("dto") 
                        if req.GET.get("dto",'')!='' else datetime.datetime.strptime(req.GET.get("dfrom"),'%Y-%m-%d').date() + datetime.timedelta(days=7)
                                if req.GET.get("dfrom",'')!='' else datetime.datetime.today() + datetime.timedelta(days=7))
        if len(req.GET) > 2:
            exh_filter = []
            for i in exhibitions:
                if req.GET.get(str(i)):
                    exh_filter.append(i)

            excursions = excursions.filter(exhibition__in = exh_filter).distinct()
        return render(req, 'bookshopapp/schedule.html', {"excursions":excursions, "exhibitions":exhibitions})

class ExhibitionView(View):
    def get(self, req, *args, exhibition_id, **kwargs):
        exhibition = models.Exhibition.objects.get(id=exhibition_id)
        return render(req, 'bookshopapp/exhibition.html', {"exhibition":exhibition})

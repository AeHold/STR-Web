from django.shortcuts import render, redirect
from django.views import View
from bookshopapp.forms import SignUpForm, LoginForm
import bookshopapp.models as models
import datetime
import plotly.express as x
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db.models import Count
import requests
import json

class AboutUsView(View):
    def get(self, req, *args, **kwargs):
        return render(req,'bookshopapp/about.html',{})

class FAQView(View):
    def get(self, req, *args, **kwargs):
        faq = reversed(models.FAQ.objects.all().order_by("date"))
        return render(req,'bookshopapp/faq.html',{"faq":faq})

class VacancyView(View):
    def get(self, req, *args, **kwargs):
        return render(req,'bookshopapp/vacancy.html',{})

class PromosView(View):
    def get(self, req, *args, **kwargs):
        return render(req,'bookshopapp/promos.html',{})

class CssView(View):
    def get(self, req, *args, **kwargs):
        return render(req,'bookshopapp/css.html',{})

class ContactsView(View):
    def get(self, req, *args, **kwargs):
        contacts = models.Profile.objects.exclude(post=None)
        return render(req,'bookshopapp/contacts.html',{"contacts":contacts})

class NewsView(View):
    def get(self, req, *args, **kwargs):
        article = reversed(models.Article.objects.all().order_by("date"))
        return render(req,'bookshopapp/news.html',{"news":article})

class ArticleView(View):
    def get(self, req, *args, **kwargs):
        article = models.Article.objects.get(id=kwargs['article_id'])
        return render(req,'bookshopapp/article.html',{"article":article})

class PrivacyPolicyView(View):
    def get(self, req, *args, **kwargs):
        return render(req,'bookshopapp/privacypolicy.html',{})

class ShopView(View):
    def get(self, req, *args, **kwargs):
        context = {}
        products = models.Product.objects.all()

        types = models.Type.objects.all()
        if(len(req.GET)>2):
            type_filter=[]
            for type in types:
                if(req.GET.get('type'+str(type))):
                    type_filter.append(type)

            if(len(type_filter)!=0):
                print(type_filter)
                print(products)
                products = products.filter(type__in = type_filter).distinct()
                print(products)

        genres = models.Genre.objects.all()
        if(len(req.GET)>2):
            genre_filter=[]
            for genre in genres:
                if(req.GET.get('genre'+str(genre))):
                    genre_filter.append(genre)
            
            if(len(genre_filter)!=0):
                products = products.filter(genre__in = genre_filter).distinct()


        if(req.GET.get('pfrom','')!=''):
            context['pfrom']=req.GET.get('pfrom')
            products=products.filter(price__gte=context['pfrom'])

        
        if(req.GET.get('pto','')!=''):
            context['pto']=req.GET.get('pto')
            products=products.filter(price__lte=context['pto'])
        
        context['types']=types
        context['genres']=genres
        context['products']=products

        return render(req,'bookshopapp/shop.html',context)


class MainView(View):
    def get(self, req, *args, **kwargs):
        if(req.user.is_anonymous):
            cat = requests.get("https://cataas.com/cat/says/Welcome to our bookshop")
        else:
            cat = requests.get("https://cataas.com/cat/says/You must work,{0} %0AWhy do you proCATstinating%3F".format(req.user.username))
        cat_fact = json.loads(requests.get("https://catfact.ninja/fact").content.decode())['fact']
        article = models.Article.objects.all().order_by("date")[0:3]
        return render(req, 'bookshopapp/main.html', {'fact':cat_fact, "cat":cat, "news":article})

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
            models.Profile.objects.create(phone_number=phone_number, user=user, post = None)
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
            orders = models.Order.objects.filter(is_send=False)
            print(orders)
            return render(req, 'bookshopapp/stuffprofile.html', {"profile":profile, "orders":orders})
        else:
            orders = models.Order.objects.filter(is_recieved=False,client=profile)
            return render(req, 'bookshopapp/profile.html', {"profile":profile, "orders":orders})

class ProductView(View):
    def post(self,req,*args,**kwargs):
        models.Review.objects.create(product =models.Product.objects.get(id=kwargs['product_id'])
                             ,text = req.POST.get('text')
                             ,date = datetime.date.today()
                             ,author = models.Profile.objects.get(user=req.user)
                             ,rate = req.POST.get('rating'))
        return redirect('/product/{0}'.format(kwargs['product_id']))

    def get(self, req, *args, **kwargs):
        product = models.Product.objects.get(id=kwargs['product_id'])
        reviews = models.Review.objects.filter(product =models.Product.objects.get(id=kwargs['product_id']))
        return render(req,'bookshopapp/product.html',{'product':product,'reviews':reviews})

class OrderConfirmView(View):

    def post(self, req, *args, **kwargs):
        print(models.Order.objects.create(client=models.Profile.objects.get(user=req.user),
                                            product= models.Product.objects.get(id=req.POST.get('product')),
                                            city=req.POST.get('city'),
                                            street=req.POST.get('street'),
                                            house=req.POST.get('house'),
                                            appartments=req.POST.get('appartments'),
                                            order_date=datetime.date.today(),
                                            deliver_date=datetime.date.today(),
                                            is_recieved=False,
                                            is_send=False))
        return redirect('/profile')

    def get(self,req,*args,**kwargs):
        product = models.Product.objects.get(id=kwargs['product_id'])
        return render(req,'bookshopapp/order.html',{'product':product})

class StatisticsView(View):

    def get(self, req, *args, **kwargs):
        if(not User.objects.get(id=req.user.id).is_superuser):
            return redirect("/")

        product_orders_q= models.Order.objects.values('product').annotate(pcount=Count('product')).order_by('pcount')
        day_orders_q = models.Order.objects.values('order_date').annotate(dcount=Count('order_date')).order_by('dcount')
        product_orders={}
        day_orders={}
        for i in product_orders_q:
            if(product_orders.get(str(models.Product.objects.get(id=i['product'])),0)==0):
                product_orders[str(models.Product.objects.get(id=i['product']))]=i['pcount']
            else:
                product_orders[str(models.Product.objects.get(id=i['product']))]+=i['pcount']
                
        print(product_orders)

        money = 0
        for i in models.Order.objects.all():
            money = i.product.price

        money = round(money,2)

        po = x.bar(
            x = product_orders.keys(),
            y = product_orders.values(),
            title = 'Amount of orders per product',
            labels={'x':'Product','y':'orders amount'}
        )

        #do = x.bar(
        #    x = day_orders.keys(),
        #    y = day_orders.values(),
        #    title = 'Amount of orders per day',
        #    labels={'x':'Day','y':'orders amount'}
        #)

        return render(req,'bookshopapp/statistic.html',{'po':po.to_html(),'money':money})

        
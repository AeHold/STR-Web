from django.urls import path, re_path
from bookshopapp import views

urlpatterns = [
    path('', views.MainView.as_view(), name = "main"),
    path('login/', views.LoginView.as_view(), name = "login"),
    path('sign-up/', views.SignUpView.as_view(), name = "sign-up"),
    path('profile/', views.ProfileView.as_view(), name = "profile"),
    path('shop/', views.ShopView.as_view(), name = "shop"),
    path('about-us/', views.AboutUsView.as_view(), name = 'about-us'),
    path('faq/', views.FAQView.as_view(), name = 'faq'),
    path('contacts/', views.ContactsView.as_view(), name = 'contacts'),
    path('news/', views.NewsView.as_view(), name = 'news'),
    path('reviews/', views.ReviewView.as_view(), name = 'reviewes'),
    path('privacy policy/', views.PrivacyPolicyView.as_view(), name = 'privacy policy'),
    path('promos/', views.FAQView.as_view(), name = 'promos'),
]
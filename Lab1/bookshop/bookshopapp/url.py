from django.urls import path, re_path
from bookshopapp import views

urlpatterns = [
    path('', views.MainView.as_view(), name = "main"),
    path('login/', views.LoginView.as_view(), name = "login"),
    path('sign-up/', views.SignUpView.as_view(), name = "sign-up"),
    path('profile/', views.ProfileView.as_view(), name = "profile"),
    path('schedule/', views.ScheduleView.as_view(), name = "schedule"),
    path('exhibitions/', views.ExhibitionsView.as_view(), name = "exhibitions"),
    re_path(r'^exhibition/(?P<exhibition_id>\d+)/$', views.ExhibitionView.as_view(), name = "exhibition"),
]
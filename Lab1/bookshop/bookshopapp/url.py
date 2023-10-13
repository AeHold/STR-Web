from django.urls import path, re_path
from bookshopapp import views

urlpatterns = [
    path('', views.MainView.as_view(), name = "main"),
    path('login/', views.LoginView.as_view(), name = "login"),
    path('sign-up/', views.SignUpView.as_view(), name = "sign-up"),
    path('profile/', views.ProfileView.as_view(), name = "profile"),
    path('shop/', views.ShopView.as_view(), name = "shop"),
    path('about/', views.AboutUsView.as_view(), name = 'about-us'),
    path('faq/', views.FAQView.as_view(), name = 'faq'),
    path('contacts/', views.ContactsView.as_view(), name = 'contacts'),
    path('news/', views.NewsView.as_view(), name = 'news'),
    path('privacypolicy/', views.PrivacyPolicyView.as_view(), name = 'privacy policy'),
    path('promos/', views.PromosView.as_view(), name = 'promos'),
    path('vacancy/', views.VacancyView.as_view(), name = 'vacancy'),
    path('stat/', views.StatisticsView.as_view(), name='statistic'),
    path('css/', views.CssView.as_view(), name='css'),
    re_path(r'product/(?P<product_id>\d+)/$',views.ProductView.as_view(), name='product'),
    re_path(r'orderConfirm/(?P<product_id>\d+)/$',views.OrderConfirmView.as_view(), name='orderConfirm'),
    re_path(r'article/(?P<article_id>\d+)/$',views.ArticleView.as_view(), name='article')
]
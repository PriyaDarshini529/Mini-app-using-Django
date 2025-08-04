from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_page,name="login_page"),
    path('register_page/',views.register_page,name='register_page'),
    path('home_page/',views.home_page,name="home_page"),
    path('logout_page/',views.logout_page,name="logout_page"),
    path('base/', views.home_view, name='base'),  # Homepage with links
    path('predict/', views.predict_image, name='predict_image'),  # Brain tumor detection
    path('calculator/', views.calculator, name='calculator'),  # Calculator form
    path('hello/<str:result>/', views.hello, name='hello'),  # Calculator result page
    path('predict/<str:prediction>/', views.predict, name='predict'),  # Calculator result page
    path('test/', views.test, name='test'),
    path('decision/<str:report>/', views.decision, name='decision')
    
]

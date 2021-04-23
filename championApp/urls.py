from django.urls import path
from . import views

urlpatterns = [
    path("", views.frontpage),
    path("champions", views.champion),
    path("login", views.loginPage),
    path("logout", views.logout),
    path("shopping", views.shoppingPage),
    path("register/submit", views.register),
    path("login/redirect", views.loginUser),
    path("champion/ability/<int:champion_id>", views.championAbility),
    path("add/Champion", views.addChamps)
    
    
    

]
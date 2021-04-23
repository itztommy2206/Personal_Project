from django.shortcuts import render, redirect
import requests
from .models import *
import bcrypt
from django.contrib import messages
from django.db.models import Count

# Create your views here.
def frontpage(request):
    if "user_id" not in request.session:
        return redirect("/login")
    context={
        "current_user":User.objects.get(id=request.session['user_id'])
    }
    return render(request, "frontPage.html", context)
def champion(request):
    if "user_id" not in request.session:
        return redirect("/login")
    url = "http://ddragon.leagueoflegends.com/cdn/11.7.1/data/en_US/champion/{}.json" 
    champion_data = []
    champions = Champion.objects.all().order_by("name")
    ordered_list = Champion.objects.order_by("word")
    
    for champion in champions:
        r = requests.get(url.format(champion)).json()
        champion_stats = {
            "champion_name":champion.name,
            "champs_id": champion.id,
            "champion_id":r['data'][champion.name]["id"],
            "champion_title":r['data'][champion.name]['title'],
            "champion_img": "http://ddragon.leagueoflegends.com/cdn/img/champion/splash/" + champion.name + "_0.jpg",
            "lore":r['data'][champion.name]['lore'],
        }
        champion_data.append(champion_stats)
        
    context = {
        "current_user":User.objects.get(id=request.session['user_id']),
        'champion_data': champion_data,
        
        }
    return render(request, "champion.html", context)

def championAbility(request, champion_id):
    if "user_id" not in request.session:
        return redirect("/login")
    url = "http://ddragon.leagueoflegends.com/cdn/11.7.1/data/en_US/champion/{}.json" 
    champion_stat = []
    champion = Champion.objects.get(id = champion_id)
    r = requests.get(url.format(champion)).json()
    champion_statistic = r['data'][champion.name]['stats'] #STATS{DICTIONARY}
    champion_spells = r['data'][champion.name]['spells'] 
    champion_stat.append(champion_statistic)
    champion_skins = r['data'][champion.name]['skins']
    
    context = {
        "current_user":User.objects.get(id=request.session['user_id']),
        "champion_name":champion.name,
        "champion_stat":champion_stat,
        "champion_spell":champion_spells,
        "skin_info":champion_skins,
        "passive":r['data'][champion.name]['passive'],
        "allytips":r['data'][champion.name]['allytips'],
        "enemytips":r['data'][champion.name]['enemytips'],
        "tags":r['data'][champion.name]['tags']
    }
    
    return render(request, "champAbility.html", context)


def loginPage(request):
    if messages:
        error_messages = messages
        
    return render(request, "loginPage.html")
def shoppingPage(request):
    if "user_id" not in request.session:
        return redirect("/login")
    context={
        "current_user":User.objects.get(id=request.session['user_id'])
    }
    return render(request, "shoppingPage.html", context)

def register(request):
    if request.method =="POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/login")
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email= request.POST['email'], birthday=request.POST['birthday'], password = pw_hash)
            request.session['user_id'] = user.id
            return redirect('/')
    return redirect("/")

def loginUser(request):
    if request.method =="POST":
        user_email = User.objects.filter(email = request.POST['email'])
        if user_email:
            user = user_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect("/")
        messages.error(request, "Email or Password are incorrect")
    return redirect("/login")

def logout(request):
    request.session.flush()
    return redirect("/login")

def addChamps(request):
    if request.method=="POST":
        champion_name = Champion.objects.create(name=request.POST['champion'].title())
        return redirect("/champions")
    return redirect("/champions")
        
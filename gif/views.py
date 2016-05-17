from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import UserForm
from django.contrib.auth import login
from django.shortcuts import render

from .models import Gif
from django.contrib.auth.models import User


def index(request):
    latest_gif_list = Gif.objects.all()
    template = loader.get_template('gif/index.html')
    context = {
        'latest_gif_list': latest_gif_list,
    }
    return HttpResponse(template.render(context, request))


def post_gif(request):
    if request.method == 'GET':
        # GET c'est quand tu accèdes à la page avec le formulaire
        template = loader.get_template('gif/post_gif.html')
        context = {}
        # Même si "context" est vide, on doit le passer en argument pour générer la réponse sinon on ne peut pas générer le token anti-CSRF (d'où ton bug)
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        # POST c'est quand tu cliques sur "Envoyer" le formulaire
        newly_created_gif = Gif.objects.create(
            url=request.POST.get('gif_url')) # On va chercher "gif_url" car c'est la valeur qu'on a donné à l'attribut "name" du formulaire dans "post_gif.html"
        if newly_created_gif:
            # Dans le cas où le GIF a bien été ajouté à la table :
            return HttpResponseRedirect('/')
            # Retour sur la page d'accueil pour voir le résultat
        else:
            # Si, pour une raison ou une autre, le GIF n'a pas été ajouté à la table,
            # On envoie ce message d'erreur pour avertir l'utilisateur :
            return HttpResponse('Failed to add this GIF', request)


def add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            # redirect, or however you want to get to the main view
            return HttpResponseRedirect('/')
    else:
        form = UserForm()
    template = loader.get_template('gif/create_account.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))

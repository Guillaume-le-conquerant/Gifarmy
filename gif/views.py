from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .models import Gif


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

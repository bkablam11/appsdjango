from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Album, Artist, Contact, Booking
#from django.template import loader
from .form import ContactForm, ParagraphErrorList
# Create your views here.


def index(request):
    albums = Album.objects.filter(available=True).order_by('-created_at')[:23]
    # formated_albums = ["<li>{}</li>".format(album.title) for album in albums]
    # message = """<ul>{}</ul>""".format("\n".join(formated_albums))
    # return HttpResponse(message)
    formated_albums = [f"<li>{album.title}</li>" for album in albums]
    #message = f"""<ul>{"".join(formated_albums)}</ul>"""
    template = loader.get_template('ecomapps\index.html')
    #return HttpResponse(message)
    context = {'albums': albums}
    #return HttpResponse(template.render(context, request=request))
    return render(request, 'ecomapps\index.html', context)

def listing(request):
    albums = Album.objects.filter(available=True)
    #formated_albums = ["<li>{}</li>".format(album.title) for album in albums]
    #message = """<ul>{}</ul>""".format("\n".join(formated_albums))
    #return HttpResponse(message)
    context = {'albums': albums}
    #return HttpResponse(template.render(context, request=request))
    return render(request, 'ecomapps\listing.html', context)


def detail(request, album_id):
    #album = Album.objects.get(pk=album_id)
    album = get_object_or_404(Album, pk=album_id)
    artists_name = " ".join([artist.name for artist in album.artist.all()])
    # message = f"Le nom de l'album est {album.title}. Il a été écrit par {artists} "
    # return HttpResponse(message)
    context = {
        'album_title': album.title,
        'album_name': artists_name,
        'album_id': album.id,
        'thumbnail': album.picture
               }
    if request.method == 'POST':
        form = ContactForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            #email = request.POST.get('email')
            #name = request.POST.get('name')
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']

            contact = Contact.objects.filter(email=email)
            if not contact.exists():
                # If a contact is not registered, create a new one.
                contact = Contact.objects.create(
                    email=email,
                    name=name
                )
            else:
                contact = contact.first()

            album = get_object_or_404(Album, id=album_id)
            booking = Booking.objects.create(
                contact=contact,
                album=album
            )
            album.available = False
            album.save()
            context = {
                'album_title': album.title
            }
            return render(request, 'ecomapps/merci.html', context)
        else:
            context['errors'] = form.errors.items()
    else:
        form = ContactForm()

    context['form'] = form

    # context = {
    #     'album_title': album.title,
    #     'album_name': artists_name,
    #     'album_id': album.id,
    #     'thumbnail': album.picture,
    #     'form':form
    #            }
    #return HttpResponse(template.render(context, request=request))
    return render(request, 'ecomapps\detail.html', context)


def search(request):
    # obj = str(request.GET)
    # query = request.GET['query']
    # message = f"propriété GET : {obj} et requête : {query}"
    # #http: // 127.0.0.1: 8000 / ecomapps / search /?query = Celine
    # return HttpResponse(message)

    query = request.GET.get('query')
    if not query:
        albums = Album.objects.all()
    else:
        # title contains the query is and query is not sensitive to case.
        albums = Album.objects.filter(title__icontains=query) #pas de correspondance exacte

        if not albums.exists(): # items exist True or false
            albums = Album.objects.filter(artist__name__icontains=query) #search with name artist

        # if not albums.exists(): # items exist True or false
        #     message = "Misere de Misere, nous n'avons trouver aucun resultat"
        #
        # else:
        #     albums = [f"<li>{album}</li>" for album in albums]
        #     message = f""" Nous avons trouver les correspondances, a votre requete ! les voici :<ul>{"<li></li>".join(albums)}</ul>"""

    title = "Resultats pour la requête %s"%query
    context = {
        'albums': albums,
        'title': title
    }

    #return HttpResponse(message)
    return render(request, 'ecomapps\search.html', context)










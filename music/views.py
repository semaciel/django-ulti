from django.http import Http404
# from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render, get_object_or_404
# from django.views.generic import TemplateView
from .models import Album

# Create your views here.
def index(request):
    all_albums = Album.objects.all()
    context = {'all_albums': all_albums,}
    return render(request, 'music/index.html', context)


def detail(request, pk):
    album = get_object_or_404(Album, pk=pk)
    context = {'album': album,}

    return render(request, 'music/detail.html', context)

def favorite(request, pk):
    album = get_object_or_404(Album, pk=pk)
    context = {'album': album}

    try:
        selected_song = album.song_set.get(pk=request.POST['song'])
    except (KeyError, Song.DoesNotExist):
        context['error_msg'] = "No song selected!!"
        return render(request, 'music/detail.html', context)
    else:
        selected_song.is_favorite = True
        selected_song.save()
        return render(request, 'music/detail.html', context)

# def <modelname>(request, pk):
    # template = loader.get_template('music/index.html')
    # return HttpResponse(template.render(context, request))

    # try:
    #     album = Album.objects.get(pk=pk)
    #     context = {
    #             'album': album,
    #     }
    # except Album.DoesNotExist:
    #     raise Http404('Album does not exist!!')
    # return render(request, 'music/detail.html', context)

    # return HttpResponse("<h1> Music  - Details for album ID : {}</h1>".format(pk))

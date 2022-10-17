from django.http import Http404
# from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render, get_object_or_404
# from django.views.generic import TemplateView
# from .models import Album

from datetime import datetime, date, timezone, timedelta
# import calendar

# Create your views here.
def index(request):
    time_UTC = datetime.now(timezone.utc)
    time_AMSC = datetime.now(timezone(timedelta(hours=-5)))
    # all_albums = Album.objects.all()
    context = {'all_albums': "Test",
               'time_utc':  "{}".format(time_UTC.strftime('%A %b (%m) %d, %Y Time: %H:%M:%S')),
               'time_amsc': "{}".format(time_AMSC.strftime('%A %b (%m) %d, %Y Time: %H:%M:%S')),}
    return render(request, 'radio/index.html', context)

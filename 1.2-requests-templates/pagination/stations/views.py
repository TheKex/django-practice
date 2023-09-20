from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings
import csv


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    page_number = request.GET.get("page", 1)
    csv_stations = []
    with open(settings.BUS_STATION_CSV, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            csv_stations.append(row)

    stations = Paginator(csv_stations, 10)
    bus_station_page = stations.get_page(page_number)
    context = {
        'bus_stations': bus_station_page.object_list,
        'page': bus_station_page,
    }
    return render(request, 'stations/index.html', context)

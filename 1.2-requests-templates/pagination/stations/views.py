from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
import csv

from pagination.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    page_number = int(request.GET.get('page', 1))
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    with open(BUS_STATION_CSV, 'r', newline='', encoding='utf-8') as file:
        bus_load = list(csv.reader(file))
    bus_list = []
    for row in bus_load:
        if row[0] != "ID":
            elem = dict()
            elem['Name'] = row[1]
            elem['Street'] = row[4]
            elem['District'] = row[6]
            bus_list.append(elem)
    paginator = Paginator(bus_list, 10)
    page = paginator.get_page(page_number)
    context = {
              'bus_stations': page,
              'page': page,
    }
    return render(request, 'stations/index.html', context)

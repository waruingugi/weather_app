# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import requests
from .models import City

# Create your views here
from django.shortcuts import render
from forms import CityForm

def index(request):
    url = '''http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=fd1ddc9ac4c6b84d80efc1908d3d0944'''
    cities = City.objects.all() #return all the cities in the database
    
    if request.method == 'POST': #only true if form is submitted
        form = CityForm(request.POST) #add actual request data to form for processing

        if not City.objects.filter(name=form['name'].value()).exists(): #only saves if city does not exist
            form.save() # will validate and save if validate

    form = CityForm()

    weather_data = []

    for city in cities:
    
        city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

        weather = {
            'city' : city,
            'temperature' : round((city_weather['main']['temp']  - 32)* 5/9, 1),#covert Fahrenheit to Celsius
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }

        weather_data.append(weather) #add the data for the current city into our list

    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'weather/index.html', context) #return index.html template

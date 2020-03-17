import requests
from django.shortcuts import render,redirect
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
     url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=3b04504088ae23eff48b4a1877ed8315'

     msg = ''
     message = ''
     message_class = ''

     if request.method == 'POST':
         form = CityForm(request.POST)

         if form.is_valid():
             new_city = form.cleaned_data['name']
             city_count = City.objects.filter(name=new_city).count()

             if city_count == 0:
                 r = requests.get(url.format(new_city)).json()

                 if r['cod'] == 200:
                     form.save()

                 else:
                     msg = 'city do not exist in API'
             else:
                 msg = 'City Exists'

         if msg:
             message = msg
             message_class = 'is-danger'
         else:
             message = 'successful'
             message_class = 'is-success'




     form = CityForm()

     cities = City.objects.all()

     weather_data = []

     for city in cities:
          r = requests.get(url.format(city)).json()

          # to check what type data are  inside the  api
          # r = requests.get(url.format(city))
          # print(r.text)


          city_weather = {
              'city' : city.name,
              'temperature' : r['main']['temp'],
              'description' : r['weather'][0]['description'],
              'icon' : r['weather'][0]['icon'],
          }

          weather_data.append(city_weather)




     context = {
     'weather_data': weather_data,
     'form':form,
     'message':message,
     'message_class':message_class}

     return render(request,'index.html',context)

def city_delete(request, city_name):
    City.objects.get(name=city_name).delete()

    return redirect('index')

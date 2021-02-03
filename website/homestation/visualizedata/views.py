from django.shortcuts import render
from django.views import View

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound

from .models import Sensor, Values


def index(request):
    return HttpResponse("Hello, world. You're at the <b>Home Monitoring Station</b> index.")


# def insertvalues(request, sensor, value):
#
#     if request.method == 'GET':
#         # v = request.GET.get('v', '')
#         # return HttpResponse("Stai inserendo il valore {}".format(request.GET.get('v')))
#         return HttpResponse("Il sensore {} sta inserendo il valore {}".format(sensor, value))

class insertvalues(View):

    def get(self, request, sensor, value):
        s = Sensor.objects.get(name=sensor)
        v = Values(sensor=s, temperature=value, humidity=value, pressure=value, timestamp='2021-01-17 13:21')
        v.save()
        return HttpResponse("Il sensore {} sta inserendo il valore {}".format(sensor, value))

    def post(self, request):
        pass


class insertSensor(View):

    def get(self, request, sensor):
        s = Sensor(name=sensor)
        s.save()


def settings(request):

    pass
    # if request.method == 'GET':
    #     do_something()
    # elif request.method == 'POST':
    #     do_something_else()
    # hs = HandleSettings()
    # context = {
    #     'Temperature': hs.get_temperature()
    # }

    return render(request, 'index.html', context=context)

    # template = loader.get_template('polls/index.html')
    # return HttpResponse(template.render(context, request))

    # return HttpResponse("Settings of the Home Monitoring Station")


def sensors(request):
    context = {
        'temperature': 35,
        'temperature_min': 22,
        'temperature_max': 38,
        'humidity': 45,
        'humidity_min': 32,
        'pressure': 1010,
        'no2': 23,
        'pm25': 55,
        'pm10': 90,
    }
    return render(request, 'sensors.html', context=context)


def sensors_live(request):
    return render(request, 'sensors_live.html')


class DynamicData(View):
    def post(self, request, data_type):
        # data_type = request.POST.get('data_type')
        print(data_type)
        if data_type not in ('sensors', 'air_quality', 'weather'):
            return HttpResponseNotFound('Data type not found')

        context = {
            'temperature': 35,
            'temperature_min': 22,
            'temperature_max': 38,
            'humidity': 45,
            'humidity_min': 54,
            'pressure': 1010,
            'pm25': 55,
            'pm10': 20,
        }

        return render(request, 'dynamic/%s.html' % data_type, context)

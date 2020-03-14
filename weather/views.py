import requests
from django.shortcuts import render
from .models import City, Notification
from .forms import CityForm, ConfigurationForm
from django.core import serializers
import http.client
import json
from bs4 import BeautifulSoup

def index(request):
    context = {}
    return render(request, 'weather/weather.html', context)

def indexNotification(request):
    isCorrect = False
    context = {}
    if request.method == "POST":
        form = CityForm(request.POST)
        # print(request, "request aqui")
        if form.is_valid:
            print(form.is_valid, "DSADAS")
            print(form, "JSON")
            context = {form: form}
        #     print(context, "context")
    return render(request, 'weather/notification.html', context)

def indexConfiguration(request):
    context = {}
    if request.method == "POST":
        print(request, "REQUEST")
        form = ConfigurationForm(request.POST)
        if form.is_valid():
            conn = http.client.HTTPSConnection('www.httpbin.org')
            headers = {'Content-type': 'application/json'}
            # print(form['ServidorPagoEfectivo'].value, "ServidorPagoEfectivo value")
            aux = str(form)
            aux1 = str(form.__getitem__('ServidorPagoEfectivo'))
            aux2 = str(form.__getitem__('AccessKey'))
            aux3 = str(form.__getitem__('SecretKey'))
            aux4 = str(form.__getitem__('IDComercio'))
            aux5 = str(form.__getitem__('NombreComercio'))
            aux6 = str(form.__getitem__('EmailComercio'))
            aux7 = str(form.__getitem__('ModoIntegracion'))
            aux8 = str(form.__getitem__('TiempoExpiracionPago'))
            aux9 = str(form.__getitem__('Pais'))
            aux10 = str(form.__getitem__('TipoMoneda'))
            aux11 = str(form.__getitem__('Monto'))
            # print(str(form.__getitem__('ServidorPagoEfectivo')))
            soup = BeautifulSoup(aux1)
            soup2 = BeautifulSoup(aux2)
            soup3 = BeautifulSoup(aux3)
            soup4 = BeautifulSoup(aux4)
            soup5 = BeautifulSoup(aux5)
            soup6 = BeautifulSoup(aux6)
            soup7 = BeautifulSoup(aux7)
            soup8 = BeautifulSoup(aux8)
            soup9 = BeautifulSoup(aux9)
            soup10 = BeautifulSoup(aux10)
            soup11 = BeautifulSoup(aux11)
            print(soup7.prettify())

            print(soup.prettify(), "prettify")
            value1 = soup.find('input').get('value')
            print(value1, "value1")
            value2 = soup2.find('input').get('value')
            print(value2, "value2")
            value3 = soup3.find('input').get('value')
            print(value3, "value3")
            value4 = soup4.find('input').get('value')
            print(value4, "value4")
            value5 = soup5.find('input').get('value')
            print(value5, "value5")
            value6 = soup6.find('input').get('value')
            print(value6, "value6")
            value7 = soup7.find('input').get('value')
            print(value7, "value7")
            value8 = soup8.find('input').get('value')
            print(value8, "value8")
            value9 = soup9.find('input').get('value')
            print(value9, "value9")
            value10 = soup10.find('input').get('value')
            print(value10, "value10")
            value11 = soup11.find('input').get('value')
            print(value11, "value11")
            

            # value2 = soup.find(id='AccessKey').get('value')
            # print(value2, "value2")
            body = {
                        "ServidorPagoEfectivo": value1,
                        "AccessKey":value2,
                        "SecretKey":value3,
                        "IDComercio":value4,
                        "NombreComercio":value5,
                        "EmailComercio":value6,
                        "ModoIntegracion":value7,
                        "TiempoExpiracionPago":value8,
                        "Pais":value9,
                        "TipoMoneda": value10,
                        "Monto":value11
                    }
            print(body, "body")
            foo = {'text': aux}
            json_data = json.dumps(body)
            conn.request('POST', '/post', json_data, headers)
            
            response = conn.getresponse()
            if response.status == 200:
                isCorrect = True
                print(response.read().decode(), "response POST")
            else:
                isCorrect = False
            print(isCorrect, "isCorrect")
            conn.close()

    return render(request, 'weather/configuration.html', context)
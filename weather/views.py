import requests
from django.shortcuts import render
from .models import City, Notification
from .forms import ConfigurationForm, NotificationForm
from django.core import serializers
from time import sleep
import http.client
import json
from django.http import HttpResponseRedirect, HttpResponse
from bs4 import BeautifulSoup
from django.views.decorators.csrf import csrf_exempt
import time

@csrf_exempt
def index(request):
    body = {}
    countryLoaded = ""
    montoLoaded = ""
    currencyLoaded = ""

    
    if request.COOKIES.get('TipoMoneda'):
        currencyLoaded  = request.COOKIES['TipoMoneda']
        print(currencyLoaded, "currencyLoaded")
    
    
    if request.COOKIES.get('Monto'):
        montoLoaded  = request.COOKIES['Monto']
        print(montoLoaded, "montoLoaded")

    if request.method == "GET":
        print("GET HOME")
        if request.COOKIES.get('pais'):
            countryLoaded  = request.COOKIES['pais']
    
    if request.method == 'POST':
        body = {
                "currency": currencyLoaded,
                "amount": montoLoaded,
                "transactionCode": "208",
                "dateExpiry": "",
                "paymentConcept": "Prueba 200",
                "additionalData": "datos adicionales de prueba",
                "adminEmail": "",
                "userEmail": "ealvarado@gmail.com",
                "userName": "Chester",
                "userLastName": "Alvarado",
                "userUbigeo": 150101,
                "userCountry": "PERU",
                "userDocumentType": "DNI",
                "userDocumentNumber": "40226700",
                "userCodeCountry": "+51",
                "userPhone": "9988776650",
                "userId": 200,
                "serviceId": 20
            }
    if body:
        data = {'title':'Python Requests','body':'Requests are awesome','userId':1}
        response = requests.post('https://jsonplaceholder.typicode.com/posts', data)
        if response.status_code == 201:
            print(body, "EEnvio exitoso de pago")
        else:
            print("Error al enviar pago. Intente nuevamente")

    context = {"country": countryLoaded, "montoFromConfg": montoLoaded}
    return render(request, 'weather/weather.html', context)

@csrf_exempt
def indexNotification(request):  
    isSaved = "0"
    currencyLoaded = ""
    montoLoaded = ""
    form = ""
    if request.method == "GET":
        if request.COOKIES.get('TipoMoneda'):
            currencyLoaded  = request.COOKIES['TipoMoneda']

        if request.COOKIES.get('Monto'):
            montoLoaded  = request.COOKIES['Monto']

            context = {'key_filed': isSaved, "currencyFromConfig": currencyLoaded, "montoFromConfig": montoLoaded}
            return render(request, 'weather/notification.html', context)

    if request.method == "POST":
        if request.POST.get("btnLimpiar"):
            context = {}
            return render(request, 'weather/notification.html', context)            

        form = NotificationForm(request.POST)  
        if form.is_valid():
            if request.COOKIES.get('TipoMoneda'):
                currencyLoaded  = request.COOKIES['TipoMoneda']
                print(currencyLoaded, "currencyLoaded")

            if request.COOKIES.get('Monto'):
                montoLoaded  = request.COOKIES['Monto']
                print(montoLoaded, "countryLoaded")

            aux1 = str(form.__getitem__('requestBody'))
            aux2 = str(form.__getitem__('signature'))

            parse1 = BeautifulSoup(aux1)
            parse2 = BeautifulSoup(aux2)

            value1 = parse1.find('input').get('value')
            value2 = parse2.find('input').get('value')
            body = {
                'PE-Signature': value2,
                'requestBody': value1
            }
            print(body, 'FORM VALIDO')
            # SENT TO API REST
            data = {'title':'Python Requests','body':'Requests are awesome','userId':1}
            response = requests.post('https://jsonplaceholder.typicode.com/posts', data) 
            # API REST
            print(response.status_code)
            if response.status_code == 201:
                form.save()
                isSaved = "1"
                emptyField = ""
                print(isSaved,"is Valid")
                context = { 'form': form, 'key_filed': isSaved, "emptyField": emptyField, "currencyFromConfig": currencyLoaded, "montoFromConfig": montoLoaded }
                return render(request, 'weather/notification.html', context)
            else:
                form.save()
                isSaved = "2"
                context = { 'form': form, 'key_filed': isSaved, "montoFromConfig": montoLoaded, "currencyFromConfig": currencyLoaded }
                return render(request, 'weather/notification.html', context)

    context = {'form': form, 'key_filed': isSaved}
    return render(request, 'weather/notification.html', context)

@csrf_exempt
def indexConfiguration(request):
    isSaved = "0"
    form = ""
    form2 = ""
    countryLoaded = ""
    ModoIntegracionLoaded = ""
    TipoMonedaLoaded = ""
    formLoaded = ""
    ServidorPagoEfectivoLoaded = ""
    AccessKeyLoaded = ""
    SecretKeyLoaded = ""
    IDComercioLoaded = ""
    NombreComercioLoaded = ""
    EmailComercioLoaded = ""
    MontoLoaded = ""
    TiempoExpiracionPagoLoaded = ""
    TipoMonedaLoaded = ""
    value1 = ""
    value2 = ""
    value3 = ""
    value4 = ""
    value5 = ""
    value6 = ""
    value7 = ""
    value8 = ""
    value9 = ""
    value10 = ""
    value11 = ""

    if request.COOKIES.get('pais'):
        countryLoaded  = request.COOKIES['pais']

    if request.COOKIES.get('ServidorPagoEfectivo'):
        ServidorPagoEfectivoLoaded  = request.COOKIES['ServidorPagoEfectivo']

    if request.COOKIES.get('AccessKey'):
        AccessKeyLoaded  = request.COOKIES['AccessKey']

    if request.COOKIES.get('SecretKey'):
        SecretKeyLoaded  = request.COOKIES['SecretKey']

    if request.COOKIES.get('IDComercio'):
        IDComercioLoaded  = request.COOKIES['IDComercio']

    if request.COOKIES.get('NombreComercio'):
        NombreComercioLoaded  = request.COOKIES['NombreComercio']

    if request.COOKIES.get('EmailComercio'):
        EmailComercioLoaded  = request.COOKIES['EmailComercio']

    if request.COOKIES.get('Monto'):
        MontoLoaded  = request.COOKIES['Monto']

    if request.COOKIES.get('TiempoExpiracionPago'):
        TiempoExpiracionPagoLoaded  = request.COOKIES['TiempoExpiracionPago']

    if request.COOKIES.get('TipoMoneda'):
        TipoMonedaLoaded  = request.COOKIES['TipoMoneda']

    if request.COOKIES.get('ModoIntegracion'):
        ModoIntegracionLoaded  = request.COOKIES['ModoIntegracion']

    if request.method == 'POST':
        if request.POST.get("btnCancelar"):
            print("LIMPIAR CONFIG")
            form = ""
            context = {
                'form': form,
                "countryLoaded": "",
                "ServidorPagoEfectivoLoaded": "",
                "AccessKeyLoaded": "",
                "SecretKeyLoaded": "",
                "IDComercioLoaded": "",
                "NombreComercioLoaded": "",
                "EmailComercioLoaded": "",
                "MontoLoaded": "",
                "TiempoExpiracionPagoLoaded": "",
                "TipoMonedaLoaded": "",
                "ModoIntegracionLoaded": ""
            }
            return render(request, 'weather/configuration.html', context)            

    if request.method == "GET":
        request.COOKIES.get('form')

        if request.COOKIES.get('form'):
            formLoaded  = request.COOKIES['form']     

        context = {"countryLoaded": countryLoaded,
                   "ServidorPagoEfectivoLoaded": ServidorPagoEfectivoLoaded,
                   "AccessKeyLoaded": AccessKeyLoaded,
                   "SecretKeyLoaded": SecretKeyLoaded,
                   "IDComercioLoaded": IDComercioLoaded,
                   "NombreComercioLoaded": NombreComercioLoaded,
                   "EmailComercioLoaded": EmailComercioLoaded,
                   "MontoLoaded": MontoLoaded,
                   "TiempoExpiracionPagoLoaded": TiempoExpiracionPagoLoaded,
                   "TipoMonedaLoaded": TipoMonedaLoaded,
                   "ModoIntegracionLoaded": ModoIntegracionLoaded
                }
        return render(request, 'weather/configuration.html', context)

    if request.method == 'POST':
        form2 = ConfigurationForm(request.POST)
        if form2.is_valid():
            print("form2 is valid")
            aux1 = str(form2.__getitem__('ServidorPagoEfectivo'))
            aux2 = str(form2.__getitem__('AccessKey'))
            aux3 = str(form2.__getitem__('SecretKey'))
            aux4 = str(form2.__getitem__('IDComercio'))
            aux5 = str(form2.__getitem__('NombreComercio'))
            aux6 = str(form2.__getitem__('EmailComercio'))
            aux8 = str(form2.__getitem__('TiempoExpiracionPago'))
            aux11 = str(form2.__getitem__('Monto'))
            aux7 = str(form2.__getitem__('ModoIntegracion'))
            aux9 = str(form2.__getitem__('Pais'))
            aux10 = str(form2.__getitem__('TipoMoneda'))

            soup = BeautifulSoup(aux1)
            soup2 = BeautifulSoup(aux2)
            soup3 = BeautifulSoup(aux3)
            soup4 = BeautifulSoup(aux4)
            soup5 = BeautifulSoup(aux5)
            soup6 = BeautifulSoup(aux6)
            soup8 = BeautifulSoup(aux8)
            soup11 = BeautifulSoup(aux11)
            soup7 = BeautifulSoup(aux7)
            soup9 = BeautifulSoup(aux9)
            soup10 = BeautifulSoup(aux10)

            value1 = soup.find('input').get('value')
            value2 = soup2.find('input').get('value')
            value3 = soup3.find('input').get('value')
            value4 = soup4.find('input').get('value')
            value5 = soup5.find('input').get('value')
            value6 = soup6.find('input').get('value')
            value8 = soup8.find('input').get('value')
            value11 = soup11.find('input').get('value')
            value7 = soup7.find('input').get('value')
            value9 = soup9.find('input').get('value')
            value10 = soup10.find('input').get('value')

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
            data = {'title':'Python Requests','body':'Requests are awesome','userId':1}
            print(body)
            response = requests.post('https://jsonplaceholder.typicode.com/posts', data)
            print(response.status_code)
            if response.status_code == 201:
                print("201 AQUI")
                isSaved = "1"
                context = { 'form': form2, 'key_filed': isSaved }
                response = render(request, 'weather/configuration.html', context)
                response.set_cookie('form', form2)
                response.set_cookie('pais', value9)
                response.set_cookie('ServidorPagoEfectivo', value1)
                response.set_cookie('AccessKey', value2)
                response.set_cookie('SecretKey', value3)
                response.set_cookie('IDComercio', value4)
                response.set_cookie('NombreComercio', value5)
                response.set_cookie('EmailComercio', value6)
                response.set_cookie('ModoIntegracion', value7)
                response.set_cookie('Monto', value11)
                response.set_cookie('TiempoExpiracionPago', value8)
                response.set_cookie('TipoMoneda', value10)
                return response
            else:                
                form2.save()
                isSaved = "2"
                context = { 'form': form2, 'key_filed': isSaved }
                print("is INValid AQUI")
                return render(request, 'weather/configuration.html', context)

        if (form2.is_valid() == False or countryLoaded or ModoIntegracionLoaded or TipoMonedaLoaded):
            data = {'title':'Python Requests','body':'Requests are awesome','userId':1}
            response = requests.post('https://jsonplaceholder.typicode.com/posts', data) 
            if response.status_code == 201:
                print("201 AL FINAL")
                isSaved = "1"
                aux1 = str(form2.__getitem__('ServidorPagoEfectivo'))
                aux2 = str(form2.__getitem__('AccessKey'))
                aux3 = str(form2.__getitem__('SecretKey'))
                aux4 = str(form2.__getitem__('IDComercio'))
                aux5 = str(form2.__getitem__('NombreComercio'))
                aux6 = str(form2.__getitem__('EmailComercio'))                
                aux7 = str(form2.__getitem__('TiempoExpiracionPago'))
                aux8 = str(form2.__getitem__('Monto'))
                aux9 = str(form2.__getitem__('Pais'))
                aux10 = str(form2.__getitem__('TipoMoneda'))
                aux11 = str(form2.__getitem__('ModoIntegracion'))

                parse1 = BeautifulSoup(aux1)
                parse2 = BeautifulSoup(aux2)
                parse3 = BeautifulSoup(aux3)
                parse4 = BeautifulSoup(aux4)
                parse5 = BeautifulSoup(aux5)
                parse6 = BeautifulSoup(aux6)
                parse7 = BeautifulSoup(aux7)
                parse8 = BeautifulSoup(aux8)
                parse9 = BeautifulSoup(aux9)
                parse10 = BeautifulSoup(aux10)
                parse11 = BeautifulSoup(aux11)

                value1 = parse1.find('input').get('value')
                value2 = parse2.find('input').get('value')
                value3 = parse3.find('input').get('value')
                value4 = parse4.find('input').get('value')
                value5 = parse5.find('input').get('value')
                value6 = parse6.find('input').get('value')
                value7 = parse7.find('input').get('value')
                value8 = parse8.find('input').get('value')
                value9 = parse9.find('input').get('value')
                value10 = parse10.find('input').get('value')
                value11 = parse11.find('input').get('value')

                context = {
                    'key_filed': isSaved,
                    "ServidorPagoEfectivoLoaded": value1,
                    "AccessKeyLoaded": value2,
                    "SecretKeyLoaded": value3,
                    "IDComercioLoaded": value4,
                    "NombreComercioLoaded": value5,
                    "EmailComercioLoaded": value6,
                    "TiempoExpiracionPagoLoaded": value7,
                    "ModoIntegracionLoaded": value11 if value11 else ModoIntegracionLoaded,
                    "MontoLoaded": value8,
                    "countryLoaded": value9 if value9 else countryLoaded,
                    "TipoMonedaLoaded": value10 if value10 else TipoMonedaLoaded
                }
                response = render(request, 'weather/configuration.html', context)
                response.set_cookie('ServidorPagoEfectivo', value1)
                response.set_cookie('AccessKey', value2)
                response.set_cookie('SecretKey', value3)
                response.set_cookie('IDComercio', value4)
                response.set_cookie('NombreComercio', value5)
                response.set_cookie('EmailComercio', value6)
                response.set_cookie('TiempoExpiracionPago', value7)
                response.set_cookie('Monto', value8)
                if value9:
                    response.set_cookie('pais', value9)
                else:
                    response.set_cookie('pais', countryLoaded)

                if value10:
                    response.set_cookie('TipoMoneda', value10)
                else:
                    response.set_cookie('TipoMoneda', TipoMonedaLoaded)

                if value11:
                    response.set_cookie('ModoIntegracion', value11)
                else:
                    response.set_cookie('ModoIntegracion', ModoIntegracionLoaded)
                return response
            else:
                isSaved = "2"
                context = { 
                    'key_filed': isSaved,
                    "ServidorPagoEfectivoLoaded": ServidorPagoEfectivoLoaded,
                    "AccessKeyLoaded": AccessKeyLoaded,
                    "SecretKeyLoaded": SecretKeyLoaded,
                    "IDComercioLoaded": IDComercioLoaded,
                    "NombreComercioLoaded": NombreComercioLoaded,
                    "EmailComercioLoaded": EmailComercioLoaded,
                    "MontoLoaded": MontoLoaded,
                    "TiempoExpiracionPagoLoaded": TiempoExpiracionPagoLoaded,
                    "TipoMonedaLoaded": TipoMonedaLoaded,
                    "ModoIntegracionLoaded": ModoIntegracionLoaded,
                    "countryLoaded": countryLoaded
                }
                print("is INValid AL FINAL")
                return render(request, 'weather/configuration.html', context)


    context = { 'form': form2, 'key_filed': isSaved, "countryLoaded": countryLoaded, "ModoIntegracionLoaded": ModoIntegracionLoaded, "TipoMonedaLoaded": TipoMonedaLoaded }
    return render(request, 'weather/configuration.html', context)
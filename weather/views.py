import requests
from django.shortcuts import render
from .models import City, Notification
from .forms import ConfigurationForm, NotificationForm
from django.core import serializers
from time import sleep
from django.template import RequestContext
import http.client
import json
from django.http import HttpResponseRedirect, HttpResponse
from bs4 import BeautifulSoup
import threading
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    body = {}
    countryLoaded = ""
    if request.method == "GET":
        if request.COOKIES.get('pais'):
            countryLoaded  = request.COOKIES['pais']
            print(countryLoaded, "countryLoaded")
    
    if request.method == 'POST':
        body = {
                "currency": 0,
                "amount": 0,
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

    context = {"country": countryLoaded}
    return render(request, 'weather/weather.html', context)

@csrf_exempt
def indexNotification(request):  
    isSaved = "0"  
    form = ""
    if request.method == "POST":
        form = NotificationForm(request.POST)  
        if form.is_valid():
            aux1 = str(form.__getitem__('requestBody'))
            aux2 = str(form.__getitem__('signature'))

            parse1 = BeautifulSoup(aux1)
            parse2 = BeautifulSoup(aux2)

            value1 = parse1.find('input').get('value')
            print(value1, "value1")
            value2 = parse2.find('input').get('value')
            print(value2, "value2")
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
                emptyField = ""
                form.save()
                isSaved = "1"
                print(response.status_code) 
                print(response.text)
                print(isSaved,"is Valid")
                context = { 'form': form, 'key_filed': isSaved, "emptyField": emptyField }
                return render(request, 'weather/notification.html', context)
            else:
                form.save()
                isSaved = "2"
                context = { 'form': form, 'key_filed': isSaved }
                print("is INValid")
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
    # countryLoaded = ""
    ServidorPagoEfectivoLoaded = ""
    AccessKeyLoaded = ""
    SecretKeyLoaded = ""
    IDComercioLoaded = ""
    NombreComercioLoaded = ""
    EmailComercioLoaded = ""
    MontoLoaded = ""
    TiempoExpiracionPagoLoaded = "",
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

    if request.method == 'POST':
        if request.POST.get("btnCancelar"):
            context = {}
            s = requests.session()
            s.cookies.clear()
            print("PRESIONO BUTTON LIMPIAR")
            return render(request, 'weather/configuration.html', context)            

    if request.method == "GET":
        print("ENTRO")
        request.COOKIES.get('form')

        if request.COOKIES.get('form'):
            formLoaded  = request.COOKIES['form']
            print(formLoaded, "formLoaded")

        if request.COOKIES.get('pais'):
            countryLoaded  = request.COOKIES['pais']
            print(countryLoaded, "countryLoaded")

        if request.COOKIES.get('ServidorPagoEfectivo'):
            ServidorPagoEfectivoLoaded  = request.COOKIES['ServidorPagoEfectivo']
            print(ServidorPagoEfectivoLoaded, "ServidorPagoEfectivoLoaded")

        if request.COOKIES.get('AccessKey'):
            AccessKeyLoaded  = request.COOKIES['AccessKey']
            print(AccessKeyLoaded, "AccessKeyLoaded")

        if request.COOKIES.get('SecretKey'):
            SecretKeyLoaded  = request.COOKIES['SecretKey']
            print(SecretKeyLoaded, "SecretKeyLoaded")

        if request.COOKIES.get('IDComercio'):
            IDComercioLoaded  = request.COOKIES['IDComercio']
            print(IDComercioLoaded, "IDComercioLoaded")

        if request.COOKIES.get('NombreComercio'):
            NombreComercioLoaded  = request.COOKIES['NombreComercio']
            print(NombreComercioLoaded, "NombreComercioLoaded")

        if request.COOKIES.get('EmailComercio'):
            EmailComercioLoaded  = request.COOKIES['EmailComercio']
            print(EmailComercioLoaded, "EmailComercioLoaded")

        if request.COOKIES.get('Monto'):
            MontoLoaded  = request.COOKIES['Monto']
            print(MontoLoaded, "MontoLoaded")

        if request.COOKIES.get('TiempoExpiracionPago'):
            TiempoExpiracionPagoLoaded  = request.COOKIES['TiempoExpiracionPago']
            print(TiempoExpiracionPagoLoaded, "TiempoExpiracionPagoLoaded")

        if request.COOKIES.get('TipoMoneda'):
            TipoMonedaLoaded  = request.COOKIES['TipoMoneda']
            print(TipoMonedaLoaded, "TipoMonedaLoaded")

        if request.COOKIES.get('ModoIntegracion'):
            ModoIntegracionLoaded  = request.COOKIES['ModoIntegracion']
            print(ModoIntegracionLoaded, "ModoIntegracionLoaded")

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
        # create a form instance and populate it with data from the request:
        # check whether it's valid:

        if request.COOKIES.get('pais'):
            countryLoaded  = request.COOKIES['pais']
            print(countryLoaded, "countryLoaded")

        if request.COOKIES.get('ServidorPagoEfectivo'):
            ServidorPagoEfectivoLoaded  = request.COOKIES['ServidorPagoEfectivo']
            print(ServidorPagoEfectivoLoaded, "ServidorPagoEfectivoLoaded")

        if request.COOKIES.get('AccessKey'):
            AccessKeyLoaded  = request.COOKIES['AccessKey']
            print(AccessKeyLoaded, "AccessKeyLoaded")

        if request.COOKIES.get('SecretKey'):
            SecretKeyLoaded  = request.COOKIES['SecretKey']
            print(SecretKeyLoaded, "SecretKeyLoaded")

        if request.COOKIES.get('IDComercio'):
            IDComercioLoaded  = request.COOKIES['IDComercio']
            print(IDComercioLoaded, "IDComercioLoaded")

        if request.COOKIES.get('NombreComercio'):
            NombreComercioLoaded  = request.COOKIES['NombreComercio']
            print(NombreComercioLoaded, "NombreComercioLoaded")

        if request.COOKIES.get('EmailComercio'):
            EmailComercioLoaded  = request.COOKIES['EmailComercio']
            print(EmailComercioLoaded, "EmailComercioLoaded")

        if request.COOKIES.get('Monto'):
            MontoLoaded  = request.COOKIES['Monto']
            print(MontoLoaded, "MontoLoaded")

        if request.COOKIES.get('TiempoExpiracionPago'):
            TiempoExpiracionPagoLoaded  = request.COOKIES['TiempoExpiracionPago']
            print(TiempoExpiracionPagoLoaded, "TiempoExpiracionPagoLoaded")

        if request.COOKIES.get('TipoMoneda'):
            TipoMonedaLoaded  = request.COOKIES['TipoMoneda']
            print(TipoMonedaLoaded, "TipoMonedaLoaded")

        if request.COOKIES.get('ModoIntegracion'):
            ModoIntegracionLoaded  = request.COOKIES['ModoIntegracion']
            print(ModoIntegracionLoaded, "ModoIntegracionLoaded")

        print(form2, "form2")
        if form2.is_valid():
            print("PASo")
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
            # if (form2.is_valid() and countryLoaded == "" and ModoIntegracionLoaded == "" and TipoMonedaLoaded == ""):
            soup7 = BeautifulSoup(aux7)
            soup9 = BeautifulSoup(aux9)
            soup10 = BeautifulSoup(aux10)

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
            value8 = soup8.find('input').get('value')
            print(value8, "value8")
            value11 = soup11.find('input').get('value')
            print(value11, "value11")

            value7 = soup7.find('input').get('value')
            print(value7, "value7")
            value9 = soup9.find('input').get('value')
            print(value9, "value9")
            value10 = soup10.find('input').get('value')
            print(value10, "value10")

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
            if response.status_code == 201:
                print("201")
                # if (form2.is_valid() and countryLoaded == "" and ModoIntegracionLoaded == "" and TipoMonedaLoaded == ""):
                # form2.save()
                # form.cleaned_data['ServidorPagoEfectivo'] 
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
                # if value7:
                response.set_cookie('ModoIntegracion', value7)
                # else:                    
                #     response.set_cookie('ModoIntegracion', ModoIntegracionLoaded)
                response.set_cookie('Monto', value11)
                response.set_cookie('TiempoExpiracionPago', value8)
                response.set_cookie('TipoMoneda', value10)
                return response
            else:                
                form2.save()
                isSaved = "2"
                context = { 'form': form2, 'key_filed': isSaved }
                print("is INValid")
                return render(request, 'weather/configuration.html', context)

        if (form2.is_valid() == False or countryLoaded or ModoIntegracionLoaded or TipoMonedaLoaded):
            print("REENVIA FORMULARIO PERO SE MOVIO D VISTA ANTES")
            data = {'title':'Python Requests','body':'Requests are awesome','userId':1}
            response = requests.post('https://jsonplaceholder.typicode.com/posts', data) 
            if response.status_code == 201:
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

                print(value9, "value9")
                print(countryLoaded, "countryLoaded")
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
                print("201")
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
                # response.set_cookie('ModoIntegracion', value7)
                return response
            else:
                isSaved = "2"
                context = { 'key_filed': isSaved }
                print("is INValid")
                return render(request, 'weather/configuration.html', context)

    print(form)
    context = { 'form': form2, 'key_filed': isSaved, "countryLoaded": countryLoaded, "ModoIntegracionLoaded": ModoIntegracionLoaded, "TipoMonedaLoaded": TipoMonedaLoaded }
    return render(request, 'weather/configuration.html', context)
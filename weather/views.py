import requests
from django.shortcuts import render
from .models import City, Notification
from .forms import ConfigurationForm, NotificationForm
import http.client
import json
from django.http import HttpResponseRedirect, HttpResponse
from bs4 import BeautifulSoup
from django.views.decorators.csrf import csrf_exempt
import time
import hmac
import hashlib
import os
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta
import pytz
from django.utils import timezone
# djangorest framework
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
from django.template.loader import get_template 

# FUNCION PARA GENERAR O HOME "/"
@csrf_exempt
def index(request):
    bodyAuthorization = {}
    bodyCips = {}
    countryLoaded = ""
    montoLoaded = ""
    currencyLoaded = ""
    AccessKeyLoaded = ""
    SecretKeyLoaded = ""
    IDComercioLoaded = ""
    timeExpiration = 0
    esPostBack = 0
    emailLoaded = ""
    auxMontGenerate = ""
    modoIntegrationLoaded = ""
    urlServerLoaded = ""
        
    if request.COOKIES.get('ServidorPagoEfectivo'):
        urlServerLoaded = request.COOKIES['ServidorPagoEfectivo']
    
    if request.COOKIES.get('ModoIntegracion'):
        modoIntegrationLoaded = request.COOKIES['ModoIntegracion']

    if request.COOKIES.get('pais'):
        countryLoaded  = request.COOKIES['pais']
    
    if request.COOKIES.get('TipoMoneda'):
        currencyLoaded  = request.COOKIES['TipoMoneda']
    
    
    if request.COOKIES.get('Monto'):
        montoLoaded  = request.COOKIES['Monto']
    
    if request.COOKIES.get('EmailComercio'):
        emailLoaded  = request.COOKIES['EmailComercio']

    if montoLoaded:
        auxMontGenerate = str(montoLoaded)
    else:
        auxMontGenerate = ""

    if request.method == "GET":
        context = {"esPostBack": esPostBack, "country": countryLoaded, "montoFromConfg": auxMontGenerate, "currencyLoaded": currencyLoaded}
        response = render(request, 'weather/weather.html', context)
        return response
    
    if request.method == 'POST':
        if request.POST.get("btnGuardar"):
            if request.COOKIES.get('AccessKey'):
                AccessKeyLoaded  = request.COOKIES['AccessKey']

            if request.COOKIES.get('SecretKey'):
                SecretKeyLoaded  = request.COOKIES['SecretKey']

            if request.COOKIES.get('IDComercio'):
                IDComercioLoaded  = request.COOKIES['IDComercio']

            if request.COOKIES.get('TiempoExpiracionPago'):
                timeExpiration  = request.COOKIES['TiempoExpiracionPago']

            # print(dateFinalFormated, "datetime.now() HORA EXACTA DE LA GENERACION DEL PROCESO")
            dateNowAddTimeToExpiration = datetime.now((pytz.timezone('America/Lima')))
            cutDateNowAddTimeToExpiration = str(dateNowAddTimeToExpiration)
            cutDateNowAddTimeToExpiration = cutDateNowAddTimeToExpiration.replace('.', " ")
            aux = cutDateNowAddTimeToExpiration.split(' ')
            dateFinalFormated = aux[0] + "T" + aux[1] + "-05:00"

            # CONVERSION DE FECHA A FORMATO ATOM (AMERICA/LATINA)
            houseAdded = int(timeExpiration)
            dateExpiryRequest = datetime.now((pytz.timezone('America/Lima'))) + timedelta(hours=houseAdded)
            cutDateExpiryNowAddTimeToExpiration = str(dateExpiryRequest)
            cutDateExpiryNowAddTimeToExpiration = cutDateExpiryNowAddTimeToExpiration.replace('.', " ")
            auxExpiry = cutDateExpiryNowAddTimeToExpiration.split(' ')
            dateExpiryFinalFormated = auxExpiry[0] + "T" + auxExpiry[1] + "-05:00"
            ####

            auxMont = str(montoLoaded)

            # GENERACION DE HASH sha256 PARA CABECERA 
            parametro = str(IDComercioLoaded) + "." + AccessKeyLoaded + "." + SecretKeyLoaded + "." + dateFinalFormated
            parametro = parametro.encode('utf-8')
            hash_object = hashlib.sha256(parametro).hexdigest()
            ######

            bodyAuthorization = {
                    "accessKey": AccessKeyLoaded,
                    "idService": int(IDComercioLoaded),
                    "dateRequest": dateFinalFormated,
                    "hashString": hash_object
                    }

            if bodyAuthorization:
                headers_data = { 
                    'Content-Type': 'application/json; charset=UTF-8',
                }
                
                # LLAMADA AL SERVICIO /AUTHORIZATIONS
                response = requests.post('https://pre1a.services.pagoefectivo.pe/v1/authorizations', json=bodyAuthorization, headers=headers_data)
                print(response.status_code, "response.status_code AUTHORIZATION")
                responseAuthJson = response.json()
                if response.status_code == 201:
                    print(responseAuthJson, "RESPONSE AUTH")
                    print("201 Auth")
                    if responseAuthJson["code"] == 100:
                        print(responseAuthJson, "responseAuthJson AUTORIZO Y GENERO TOKEN")
                        tokenAux = responseAuthJson["data"]["token"]

                        headers_data_cip = {
                            'Content-Type': 'application/json; charset=UTF-8',
                            'Accept-Language': 'es-PE',
                            'Authorization': 'Bearer' + " " + tokenAux
                            }

                        bodyCips = {
                            "currency": currencyLoaded,
                            "amount": auxMont,
                            "transactionCode": "208",
                            "dateExpiry": dateExpiryFinalFormated,
                            "paymentConcept": "Prueba 200",
                            "additionalData": "datos adicionales de prueba",
                            "userEmail": emailLoaded,
                            "userId": 200,
                            "userName": "Chester",
                            "userLastName": "Alvarado",
                            "userUbigeo": 150101,
                            "userCountry": "PERU" if countryLoaded == "PER" else "ECUADOR",
                            "userDocumentType": "DNI",
                            "userDocumentNumber": "40226700",
                            "userCodeCountry": "+51",
                            "userPhone": "9988776650",
                            "serviceId": int(IDComercioLoaded)
                        }

                        # LLAMADA AL SERVICIO /CIPS
                        responseCips = requests.post('https://pre1a.services.pagoefectivo.pe/v1/cips', json=bodyCips, headers=headers_data_cip)
                        print(responseCips.status_code, "status_code /cips")
                        responseCipsJson = responseCips.json()
                        if responseCips.status_code == 201:
                            print(responseCipsJson, "RESPONSE CIPS")
                            print("201 Cips")
                            if responseCipsJson["code"] == 100:
                                esPostBack = 1
                                amountByService = responseCipsJson["data"]["amount"]
                                enalceCip = responseCipsJson["data"]["cipUrl"]
                                context = {"modoIntegrationLoaded": modoIntegrationLoaded, "country": countryLoaded, "currencyLoaded": currencyLoaded, "montoFromConfg": amountByService, "enlaceCIP": enalceCip, "esPostBack": esPostBack}
                                response = render(request, 'weather/weather.html', context)
                                # ALMACENAMIENTO DE VARIABLES EN MEMORIA
                                response.set_cookie('token', tokenAux)
                                response.set_cookie('cipAuth', responseCipsJson["data"]["cip"])
                                response.set_cookie('cipUrlAuth', responseCipsJson["data"]["cipUrl"])
                                response.set_cookie('amountAuth', responseCipsJson["data"]["amount"])
                                response.set_cookie('penAuth', responseCipsJson["data"]["currency"])

                                if modoIntegrationLoaded == "RED":
                                    pth = os.path.abspath(os.path.dirname(__file__))
                                    with open(pth + '/static/cadmin/config.json') as f:
                                        dataAppResponse = json.load(f)
                
                                        print(dataAppResponse, "data")
                                        dataAppResponse['token'] = tokenAux
                                        dataAppResponse['cipAuth'] = responseCipsJson["data"]["cip"]
                                        dataAppResponse['cipUrlAuth'] = responseCipsJson["data"]["cipUrl"]
                                        dataAppResponse['amountAuth'] = responseCipsJson["data"]["amount"]
                                        dataAppResponse['penAuth'] = responseCipsJson["data"]["currency"]
                                        dataAppResponse['SecretKey'] = SecretKeyLoaded

                                    with open(pth + '/static/cadmin/configSaved.json', 'w') as f:
                                        print(dataAppResponse, "data saved")
                                        json.dump(dataAppResponse, f)
                                    return HttpResponseRedirect(enalceCip)
                                else:
                                    return response
                        else:
                            print("NO SE GENERO CIP")
                            context = {"country": countryLoaded, "montoFromConfg": auxMontGenerate, "currencyLoaded": currencyLoaded, "esPostBack": esPostBack}
                            response = render(request, 'weather/weather.html', context)
                            return response
                else:
                    print("No genero autorizacion ni TOKEN")
                    context = {"country": countryLoaded, "montoFromConfg": auxMontGenerate, "currencyLoaded": currencyLoaded, "esPostBack": esPostBack}
                    response = render(request, 'weather/weather.html', context)
                    return response
    

    context = {"country": countryLoaded, "montoFromConfg": auxMontGenerate, "currencyLoaded": currencyLoaded}
    return render(request, 'weather/weather.html', context)

# FUNCION PARA /NOTIFICATION
@csrf_exempt
def indexNotification(request):  
    isSaved = "0"
    currencyLoaded = ""
    montoLoaded = ""
    secretKeyLoaded = ""
    form = ""
    amountByService = 0
    cipByService = 0
    emptySignature = ""
    emptyRqBody = ""
    value1 = ""
    value2 = ""

    if request.method == "GET":
        if request.COOKIES.get('penAuth'):
            currencyLoaded  = request.COOKIES['penAuth']

        if request.COOKIES.get('Monto'):
            montoLoaded  = request.COOKIES['Monto']

        if request.COOKIES.get('amountAuth'):
            amountByService  = request.COOKIES['amountAuth']

        if request.COOKIES.get('cipAuth'):
            cipByService  = request.COOKIES['cipAuth']

            context = {'key_filed': isSaved, "currencyFromConfig": currencyLoaded, "montoFromConfig": amountByService, "cipByService": cipByService}
            return render(request, 'weather/notification.html', context)

    if request.method == "POST":
        if request.POST.get("btnLimpiar"):
            context = {}
            return render(request, 'weather/notification.html', context)

        form = NotificationForm(request.POST)
        
        aux1 = str(form.__getitem__('requestBody'))
        aux2 = str(form.__getitem__('signature'))

        soup = BeautifulSoup(aux1)
        soup2 = BeautifulSoup(aux2)

        value1 = soup.find('input').get('value')
        value2 = soup2.find('input').get('value')

        if value1 and value2:
            if not value1:
                emptySignature = "2"
            
            if not value2:
                emptyRqBody = "2"

            if request.COOKIES.get('penAuth'):
                currencyLoaded  = request.COOKIES['penAuth']

            if request.COOKIES.get('amountAuth'):
                montoLoaded  = request.COOKIES['amountAuth']

            if request.COOKIES.get('SecretKey'):
                secretKeyLoaded  = request.COOKIES['SecretKey']

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

            print(body, "BODY NOTIFICA ENVIADO")
            signatureAux = body["PE-Signature"]
            signature = hmac.new(bytes(str(secretKeyLoaded) , 'latin-1'), msg = bytes(body["requestBody"] , 'latin-1'), digestmod = hashlib.sha256).hexdigest()
            signatureAux = body["PE-Signature"]
            print(signature, "signature generado requestBody + secretkey")
            print(signatureAux, "PE-Signature enviado desde la aplicacion")

            if signature == str(signatureAux):
                form.save()
                isSaved = "1"
                emptyField = ""
                context = { 'form': form, 'key_filed': isSaved, "emptyField": emptyField, "currencyFromConfig": currencyLoaded, "montoFromConfig": montoLoaded }
                return render(request, 'weather/notification.html', context)
            else:
                form.save()
                isSaved = "2"
                context = { 'form': form, 'key_filed': isSaved, "montoFromConfig": montoLoaded, "currencyFromConfig": currencyLoaded }
                return render(request, 'weather/notification.html', context)
        else:
            if not value1:
                emptyRqBody = "1"
            
            if not value2:
                emptySignature = "1"

            context = {'form': form, 'key_filed': isSaved, "emptyRq": emptyRqBody, 'emptySigt': emptySignature}
            return render(request, 'weather/notification.html', context)

    context = {'form': form, 'key_filed': isSaved}
    return render(request, 'weather/notification.html', context)

# FUNCION PARA /CONFIGURATION
@csrf_exempt
def indexConfiguration(request):
    isSaved = "0"
    form = ""
    form2 = ""
    countryLoaded = ""
    ModoIntegracionLoaded = ""
    TipoMonedaLoaded = ""
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
    # VALUES FOR FIELDS VALIDATION
    empty1 = ""
    empty2 = ""
    empty3 = ""
    empty4 = ""
    empty5 = ""
    empty6 = ""
    empty7 = ""
    empty8 = ""
    empty9 = ""
    empty10 = ""
    empty11 = ""

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

        if not value9:
            if request.COOKIES.get('pais'):
                value9  = request.COOKIES['pais']

        if not value7:
            if request.COOKIES.get('ModoIntegracion'):
                value7  = request.COOKIES['ModoIntegracion']

        if not value10:
            if request.COOKIES.get('TipoMoneda'):
                value10  = request.COOKIES['TipoMoneda']


        if value1 and value2 and value3 and value4 and value5 and value6 and value7 and value8 and value9 and value10 and value11:

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
            if body:
                pth = os.path.abspath(os.path.dirname(__file__))
                with open(pth + '/static/cadmin/config.json') as f:
                    data = json.load(f)
                
                    print(data, "data")
                    data['SecretKey'] = value3

                with open(pth + '/static/cadmin/configSaved.json', 'w') as f:
                    json.dump(data, f)

                isSaved = "1"
                context = { 'form': form2, 'key_filed': isSaved, 'countryLoaded': value9, 'TipoMonedaLoaded': value10, "ModoIntegracionLoaded": value7 }
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
                auxMont1 = str(value11)
                if auxMont1.find(".") != -1:
                   splitMount = auxMont1.split(".")                                    
                   charctsMount = len(splitMount[1])
                   # VALIDACION DE CANTIDAD DE DECIMALES, SI TIENE UN DECIMAL, SE AUTOCOMPLETARA CON UN 0 AL FINAL
                   if charctsMount == 1:
                       auxMont1 = auxMont1 + "0"
                else:
                    auxMont1 = auxMont1 + ".00"
                response.set_cookie('Monto', auxMont1)
                response.set_cookie('TiempoExpiracionPago', value8)
                response.set_cookie('TipoMoneda', value10)
                return response
            else:                
                form2.save()
                isSaved = "2"
                context = { 'form': form2, 'key_filed': isSaved }
                return render(request, 'weather/configuration.html', context)
        else:
            if not value1:
                empty1 = "1"
            
            if not value2:
                empty2 = "1"

            if not value3:
                empty3 = "1"
            
            if not value4:
                empty4 = "1"

            if not value5:    
                empty5 = "1"
            
            if not value6:
                empty6 = "1"

            if not value7:    
                empty7 = "1"
            
            if not value8:
                empty8 = "1"

            if not value9:    
                empty9 = "1"
            
            if not value10:
                empty10 = "1"

            if not value11:    
                empty11 = "1"

            context = { 'form': form2, 'key_filed': isSaved, "empty1": empty1, "empty2": empty2, "empty3": empty3, "empty4": empty4, "empty5": empty5, "empty6": empty6, "empty8": empty8, "empty10": empty10, "empty7": empty7, "empty11": empty11, "empty9": empty9 }
            return render(request, 'weather/configuration.html', context)

        if ((value1 and value2 and value3 and value4 and value5 and value6 and value7 and value8 and value9 and value10 and value11) == False or countryLoaded or ModoIntegracionLoaded or TipoMonedaLoaded):
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
            if body:
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

                # grabar secretKey archivoConfig
                pth = os.path.abspath(os.path.dirname(__file__))
                with open(pth + '/static/cadmin/config.json') as f:
                    data = json.load(f)
                
                    print(data, "data")
                    data['SecretKey'] = value3

                with open(pth + '/static/cadmin/configSaved.json', 'w') as f:
                    json.dump(data, f)

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
                auxMont1 = float(value8)
                auxMont1 = "{:.2f}".format(auxMont1)
                response.set_cookie('Monto', str(auxMont1))

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
                return render(request, 'weather/configuration.html', context)


    context = { 'form': form2, 'key_filed': isSaved, "countryLoaded": countryLoaded, "ModoIntegracionLoaded": ModoIntegracionLoaded, "TipoMonedaLoaded": TipoMonedaLoaded }
    return render(request, 'weather/configuration.html', context)

# FUNCION PARA /VALIDATION, RETORNARA WEB EN BLANCO
def ValidationAux(request):
    if request.method == "GET":
        context = {}
        return render(request, 'weather/empty.html', context)

# FUNCION PARA /VALIDATION DESDE POSTMAN "/validation"
@api_view(["GET","POST"])
def IdealWeight(request):
    if request.method == "GET":
        template = get_template("weather/empty.html")
        return HttpResponse(template.render(), status=500)

    if request.method == 'POST':
        signatureReceived = str(request.META.get("HTTP_PE_SIGNATURE"))
        pth = os.path.abspath(os.path.dirname(__file__))
        json_data = open(pth + '/static/cadmin/configSaved.json')
        data1 = json.load(json_data)
        json_data.close()

        if signatureReceived:
            secretKeyLoadedConfig = data1["SecretKey"]
            body = json.loads(request.body)
            signatureHashed = hmac.new(bytes(str(body) , 'latin-1'), msg = bytes(str(secretKeyLoadedConfig) , 'latin-1'), digestmod = hashlib.sha256).hexdigest().upper()
            if str(signatureReceived) == str(signatureHashed):
                return JsonResponse({"code": "100", "message": "Solicitud con datos válidos"}, status=status.HTTP_200_OK, safe=False)
            else:
                return JsonResponse({"code": "111", "message": "Solicitud con datos inválidos"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)

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

    
    if request.COOKIES.get('ModoIntegracion'):
        modoIntegrationLoaded = request.COOKIES['ModoIntegracion']

    if request.COOKIES.get('pais'):
        countryLoaded  = request.COOKIES['pais']
    
    if request.COOKIES.get('TipoMoneda'):
        currencyLoaded  = request.COOKIES['TipoMoneda']
        print(currencyLoaded, "currencyLoaded")
    
    
    if request.COOKIES.get('Monto'):
        montoLoaded  = request.COOKIES['Monto']
        print(montoLoaded, "montoLoaded")
    
    if request.COOKIES.get('EmailComercio'):
        emailLoaded  = request.COOKIES['EmailComercio']
        print(emailLoaded, "emailLoaded")

    if montoLoaded:
        auxMontGenerate = float(montoLoaded)
        auxMontGenerate = "{:.2f}".format(auxMontGenerate)
        print(auxMontGenerate, "auxMontGenerate convert")
    else:
        auxMontGenerate = ""

    if request.method == "GET":
        print("AQUI GET HOME")
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

            print("entro boton PAGAR")
            # print(dateFinalFormated, "datetime.now() HORA EXACTA DE LA GENERACION DEL PROCESO")
            dateNowAddTimeToExpiration = datetime.now()

            cutDateNowAddTimeToExpiration = str(dateNowAddTimeToExpiration.replace(tzinfo=pytz.utc))
            cutDateNowAddTimeToExpiration = cutDateNowAddTimeToExpiration.replace('.', " ")                
            print(cutDateNowAddTimeToExpiration, "cutDateNowAddTimeToExpiration replace")
            aux = cutDateNowAddTimeToExpiration.split(' ')
            print(aux[0], "split")
            dateFinalFormated = aux[0] + "T" + aux[1] + "-05:00"
            print(dateFinalFormated, "dateFinalFormated")

            # CONVERT DATE EXPIRY FORMAT
            houseAdded = int(timeExpiration)
            dateExpiryRequest = datetime.now() + timedelta(hours=houseAdded)
            cutDateExpiryNowAddTimeToExpiration = str(dateExpiryRequest.replace(tzinfo=pytz.utc))
            cutDateExpiryNowAddTimeToExpiration = cutDateExpiryNowAddTimeToExpiration.replace('.', " ")                
            print(cutDateExpiryNowAddTimeToExpiration, "cutDateExpiryNowAddTimeToExpiration replace")
            auxExpiry = cutDateExpiryNowAddTimeToExpiration.split(' ')
            print(auxExpiry[0], "split")
            dateExpiryFinalFormated = auxExpiry[0] + "T" + auxExpiry[1] + "-05:00"
            print(dateExpiryFinalFormated, "dateExpiryFinalFormated")
            #FIN FORMAT DATE ATOM

            auxMont = float(montoLoaded)
            auxMont = "{:.2f}".format(auxMont)
            print(auxMont, "auxMont convert")

            parametro = str(IDComercioLoaded) + "." + AccessKeyLoaded + "." + SecretKeyLoaded + "." + dateFinalFormated
            print (parametro, "parametro")
            hash_object = hashlib.sha256(b'{{parametro}}')
            hex_dig = hash_object.hexdigest()
            print(hex_dig, "HASH")

            bodyAuthorization = {
                    "accessKey": AccessKeyLoaded,
                    "idService": int(IDComercioLoaded),
                    "dateRequest": dateFinalFormated,
                    "hashString": hex_dig
                    }

            if bodyAuthorization:
                headers_data = { 
                    'content-type': 'application/json; charset=UTF-8'
                }
                print(bodyAuthorization, "bodyAuthorization")
                response = requests.post('https://pre1a.services.pagoefectivo.pe/v1/authorizations', bodyAuthorization, headers=headers_data)
                print(response.status_code, "response.status_code AUTHORIZATION")
                print(response.text)
                print(response.headers, "HEADERS")
                #DESCOMENTAR CUANDO SE PRUEBA CON CREDENCIALES CORRECTAS
                responseAuthJson = response.json()
                resAux = {
                    "code": "100",
                    "message": "Solicitud exitosa.",
                    "data": {
                    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJCSzIiLCJqdGkiOiJiYWRkZjdjNC1hMjllLTRmNDYtYTgzMy0wMDZjOWI2MjA4MTMiLCJuYW1laWQiOiIxMDI4IiwiZXhwIjoxNTc1OTg5NTYzfQ.r7USRyoIoCrgJOsLvC41fN-aIcBQ2uHhNhsPBvFW-IQ",
                    "codeService": "SRV",
                    "tokenStart": "2019-12-09T16:15:19-05:00",
                    "tokenExpires": "2019-12-09T18:15:19-05:00",
                        }
                    }
                resAuxAuth = {
                    "code": "100",
                    "message": "Solicitud exitosa.",
                    "data": {
                        "cip": 2523136,
                        "currency": "PEN",
                        "amount": 201.01,
                        "transactionCode": "101",
                        "dateExpiry": "2020-12-31T23:59:59-05:00",
                        "cipUrl": "https://pre1a.payment.pagoefectivo.pe/AB803C1C-3266-4CFF-A236-4D9DD5AD260A.html"
                        }
                    }
                if response.status_code == 201:
                    print("201 Auth")
                    #DESCOMENTAR CUANDO SE PRUEBA CON CREDENCIALES CORRECTAS
                    if responseAuthJson["code"] == "100":
                    # if resAux["code"] == "100":
                        print(responseAuthJson, "responseAuthJson AUTORIZO Y GENERO TOKEN")
                        tokenAux = responseAuthJson["data"]["token"]
                        print(responseAuthJson["data"]["token"], "TOKEN")

                        headers_data_cip = {
                            'content-type': 'application/json; charset=UTF-8',
                            'Accept-Language': 'es-PE',
                            'Origin': 'web',
                            'Authorization': 'Bearer' + tokenAux
                            }

                        bodyCips = {
                            "currency": currencyLoaded,
                            "amount": float(auxMont),
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
                        print(bodyCips, "bodyCips")
                        responseCips = requests.post('https://pre1a.services.pagoefectivo.pe/v1/cips', bodyCips, headers=headers_data_cip)
                        print(responseCips.status_code, "status_code /cips")
                        print(responseCips.headers, "HEADERS")
                        responseCipsJson = responseCips.json()
                        if responseCips.status_code == 201:
                            print("201 Cips")
                            print(responseCipsJson, "RESPONSE AUTH 201 GENERO CIP Y SETEA EN COOKIES")
                            esPostBack = 1
                            if responseCipsJson["code"] == "100":
                            # if resAuxAuth["code"] == "100":
                                amountByService = responseCipsJson["data"]["amount"]
                                enalceCip = responseCipsJson["data"]["cipUrl"]
                                context = {"modoIntegrationLoaded": modoIntegrationLoaded, "country": countryLoaded, "montoFromConfg": amountByService, "enlaceCIP": enalceCip, "esPostBack": esPostBack}
                                response = render(request, 'weather/weather.html', context)
                                response.set_cookie('token', tokenAux)
                                response.set_cookie('cipAuth', responseCipsJson["data"]["cip"])
                                response.set_cookie('cipUrlAuth', responseCipsJson["data"]["cipUrl"])
                                response.set_cookie('amountAuth', responseCipsJson["data"]["amount"])
                                response.set_cookie('penAuth', responseCipsJson["data"]["currency"])
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

        print(form , "FORM NOTIFICA ENVIANDO")
        if value1 and value2:
            print("ENTRO NOTIFICA VALIDA")
            if not value1:
                print("REQUESTBODY COMPLETO")
                emptySignature = "2"
            
            if not value2:
                print("SIGNATURE COMPLETO")
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

            signature = hmac.new(bytes(body["requestBody"] , 'latin-1'), msg = bytes(str(secretKeyLoaded) , 'latin-1'), digestmod = hashlib.sha256).hexdigest().upper()
            print(signature, "hmac.new 256 signature en Validacion")
            signatureAux = body["PE-Signature"]
            print(signatureAux, "PE-Signature")

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
                print("REQUESTBODY VACIO")
                emptyRqBody = "1"
            
            if not value2:
                print("SIGNATURE VACIO")
                emptySignature = "1"

            print(emptySignature,"FORM INVALIDO O CAMPOS INCOMPLETOS")
            context = {'form': form, 'key_filed': isSaved, "emptyRq": emptyRqBody, 'emptySigt': emptySignature}
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
        # if form2.is_valid():
        if not value9:
            if request.COOKIES.get('pais'):
                value9  = request.COOKIES['pais']
                print(value9, "VALUE9 PAIS")

        if not value7:
            if request.COOKIES.get('ModoIntegracion'):
                value7  = request.COOKIES['ModoIntegracion']
            print(value7, "value7 INTEG")

        if not value10:
            if request.COOKIES.get('TipoMoneda'):
                value10  = request.COOKIES['TipoMoneda']
            print(value10, "value10 MONED")


        if value1 and value2 and value3 and value4 and value5 and value6 and value7 and value8 and value9 and value10 and value11:
            print("form2 is valid")

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
            print(body)
            if body:
                print("201 AQUI")
                pth = os.path.abspath(os.path.dirname(__file__))
                print(pth, "PATH CURRENT")
                # # with open('./static/cadmin/config.json') as f:
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
                auxMont1 = float(value11)
                auxMont1 = "{:.2f}".format(auxMont1)
                response.set_cookie('Monto', auxMont1)
                response.set_cookie('TiempoExpiracionPago', value8)
                response.set_cookie('TipoMoneda', value10)
                return response
            else:                
                form2.save()
                isSaved = "2"
                context = { 'form': form2, 'key_filed': isSaved }
                print("is INValid AQUI")
                return render(request, 'weather/configuration.html', context)
        else:
            print("FALTA ALGUN CAMPO")
            if not value1:
                print("servidor VACIO")
                empty1 = "1"
            
            if not value2:
                print("accsess VACIO")
                empty2 = "1"

            if not value3:
                print("secret VACIO")
                empty3 = "1"
            
            if not value4:
                print("SIGNATURE VACIO")
                empty4 = "1"

            if not value5:
                print("REQUESTBODY VACIO")
                empty5 = "1"
            
            if not value6:
                print("SIGNATURE VACIO")
                empty6 = "1"

            if not value7:
                print("REQUESTBODY VACIO")
                empty7 = "1"
            
            if not value8:
                print("SIGNATURE VACIO")
                empty8 = "1"

            if not value9:
                print("REQUESTBODY VACIO")
                empty9 = "1"
            
            if not value10:
                print("SIGNATURE VACIO")
                empty10 = "1"

            if not value11:
                print("REQUESTBODY VACIO")
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
            print(body)
            if body:
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

                # grabar secretKey archivoConfig
                # with open('./static/cadmin/config.json') as f:
                #     data = json.load(f)
                
                #     print(data, "data")
                #     data['SecretKey'] = value3

                # with open('./static/cadmin/configSaved.json', 'w') as f:
                #     json.dump(data, f)
                pth = os.path.abspath(os.path.dirname(__file__))
                print(pth, "PATH CURRENT")
                # # with open('./static/cadmin/config.json') as f:
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
                response.set_cookie('Monto', auxMont1)

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

def ValidationAux(request):
    if request.method == "GET":
        context = {}
        return render(request, 'weather/empty.html', context)

@api_view(["GET","POST"])
def IdealWeight(request):
    if request.method == "GET":
        print("INVOCO GET VALIDATION")
        return Response(template_name="templates/weather/empty.html", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'POST':
        signatureReceived = str(request.META.get("HTTP_PE_SIGNATURE"))
        pth = os.path.abspath(os.path.dirname(__file__))
        print(pth, "PATH CURRENT")
                # # # with open('./static/cadmin/config.json') as f:
                # with open(pth + './static/cadmin/config.json') as f:
                #     data = json.load(f)
                
                #     print(data, "data")
                #     data['SecretKey'] = value3

                # with open(pth + './static/cadmin/configSaved.json', 'w') as f:
                #     json.dump(data, f)
        json_data = open(pth + '/static/cadmin/configSaved.json')
        # "{% static 'cadmin/css/style.css' %}
        data1 = json.load(json_data) # deserialises it
        json_data.close()

        if signatureReceived:
            print(data1["SecretKey"], "SecretKeyLoaded DATA CONFIG.JSON LOADED")
            secretKeyLoadedConfig = data1["SecretKey"]
            body = json.loads(request.body)
            print(body, "body")
            signatureHashed = hmac.new(bytes(str(body) , 'latin-1'), msg = bytes(str(secretKeyLoadedConfig) , 'latin-1'), digestmod = hashlib.sha256).hexdigest().upper()
            print(signatureHashed, "signatureHashed GENERADO ")            
            print(signatureReceived, "SIGNATURE FROM POSTMAN")
            if str(signatureReceived) == str(signatureHashed):
                return JsonResponse({"code": "100", "message": "Solicitud con datos válidos"}, status=status.HTTP_200_OK, safe=False)
            else:
                return JsonResponse({"code": "111", "message": "Solicitud con datos inválidos"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)

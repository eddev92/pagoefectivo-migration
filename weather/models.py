from django.db import models

class City(models.Model):
    requestBody = models.CharField(max_length=25)

    def __str__(self):
        return self.requestBody

    class Meta:
        verbose_name_plural = 'cities'

class Notification(models.Model):
    ServidorPagoEfectivo = models.CharField(max_length=25)
    AccessKey = models.CharField(max_length=25)
    SecretKey = models.CharField(max_length=25)
    IDComercio = models.CharField(max_length=25)
    NombreComercio = models.CharField(max_length=25)
    EmailComercio = models.CharField(max_length=25)
    ModoIntegracion = models.CharField(max_length=25)
    TiempoExpiracionPago = models.CharField(max_length=25)
    Pais = models.CharField(max_length=25)
    TipoMoneda = models.CharField(max_length=25)
    Monto = models.CharField(max_length=25)
    TiempoExpiracionPago = models.CharField(max_length=25)
    TipoMoneda = models.CharField(max_length=25)
    Monto = models.CharField(max_length=25)
    Pais = models.CharField(max_length=25)

    def __str__(self):
        return self,
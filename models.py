from django.db import models

# Create your models here.
class TelemetryTracker(models.Model):
    tempInternal=models.FloatField(null=True)
    humInternal=models.FloatField(null=True)
    tempCab=models.FloatField(null=True)
    humCab=models.FloatField(null=True)

    batteryV=models.FloatField(null=True)
    batteryIP=models.FloatField(null=True)
    batteryIN=models.FloatField(null=True)
    SoC=models.FloatField(null=True)
    PVV=models.FloatField(null=True)
    PVI=models.FloatField(null=True)
    lightPWM=models.IntegerField(null=True)


    bInverter=models.BooleanField(default=False)
    bUVLO=models.BooleanField(default=False)
    bFridge=models.BooleanField(default=False)

    generatedTimestamp=models.DateTimeField(null=True)
    recievedTimestamp=models.DateTimeField(auto_now_add=True,null=True)

    synced=models.BooleanField(default=False)
class WeatherTracker(models.Model):
    tempExternal=models.FloatField(null=True)
    humExternal=models.FloatField(null=True)

    generatedTimestamp=models.DateTimeField(null=True)
    recievedTimestamp=models.DateTimeField(auto_now_add=True,null=True)
    synced=models.BooleanField(default=False)


class GeoTracker(models.Model):
    lat=models.FloatField(null=True)
    long=models.FloatField(null=True)
    precision=models.FloatField(null=True)

    generatedTimestamp=models.DateTimeField(null=True)
    recievedTimestamp=models.DateTimeField(auto_now_add=True,null=True)

    synced=models.BooleanField(default=False)

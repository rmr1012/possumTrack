from django.contrib import admin

# Register your models here.
from .models import TelemetryTracker

admin.site.register(TelemetryTracker)

class PossumAdmin(admin.ModelAdmin):
    model = TelemetryTracker
    list_display = [
        'tempInternal',
        'humInternal',
        'tempCab',
        'humCab',
        'batteryV',
        'batteryIP',
        'batteryIN',
        'SoC',
        'PVV',
        'PVI',
        'lightPWM',
        'bInverter',
        'bUVLO',
        'bFridge',
        'generatedTimestamp',
        'recievedTimestamp']
    list_editable = [
        'tempInternal',
        'humInternal',
        'tempCab',
        'humCab',
        'batteryV',
        'batteryIP',
        'batteryIN',
        'SoC',
        'PVV',
        'PVI',
        'lightPWM',
        'bInverter',
        'bUVLO',
        'bFridge',
        'generatedTimestamp',
        'recievedTimestamp']

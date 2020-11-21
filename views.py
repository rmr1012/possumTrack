from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden , HttpResponse
from django.urls import reverse
from possumTrack.models import *
from random import *



class HomeView(TemplateView): #some from 48
    template_name = 'possumTrack/possumTrack.html'
    def get(self, request):
        return render(request, self.template_name, context=None)


# @api_view(['GET','POST'])
@csrf_exempt
def toggleAPI(request):

    if request.method == 'POST':
        target=request.POST.get('target')
        state=request.POST.get('state')
        print("Toggle request! ",target,state)
        return HttpResponse(200)

@csrf_exempt
def telemetryAPI(request):

    if request.method == 'POST':

        entry=TelemetryTracker(
                tempInternal        =   request.POST.get('tempInternal'),
                humInternal         =   request.POST.get('humInternal'),
                tempCab             =   request.POST.get('tempCab'),
                humCab              =   request.POST.get('humCab'),
                batteryV            =   request.POST.get('batteryV'),
                batteryIP           =   request.POST.get('batteryIP'),
                batteryIN           =   request.POST.get('batteryIN'),
                SoC                 =   request.POST.get('SoC'),
                PVV                 =   request.POST.get('PVV'),
                PVI                 =   request.POST.get('PVI'),
                lightPWM            =   request.POST.get('lightPWM'),
                bInverter           =   request.POST.get('bInverter'),
                bUVLO               =   request.POST.get('bUVLO'),
                bFridge             =   request.POST.get('bFridge'),
                generatedTimestamp  =   request.POST.get('generatedTimestamp')
            )
        entry.save()
        return HttpResponse(200)


def geoAPI(request):

        if request.method == 'POST':

            entry=TelemetryTracker(
                    lat                 =   request.POST.get('lat'),
                    long                =   request.POST.get('long'),
                    precision           =   request.POST.get('precision'),
                    generatedTimestamp  =   request.POST.get('generatedTimestamp'),
                    recievedTimestamp   =   request.POST.get('recievedTimestamp')
                )
            entry.save()
            return HttpResponse(200)

def weatherAPI(request):

        if request.method == 'POST':

            entry=TelemetryTracker(
                    tempExternal        =   request.POST.get('tempExternal'),
                    humExternal         =   request.POST.get('humExternal'),
                    generatedTimestamp  =   request.POST.get('generatedTimestamp'),
                    recievedTimestamp   =   request.POST.get('recievedTimestamp')
                )
            entry.save()
            return HttpResponse(200)


def snapshotAPI(request):

    if request.method == 'GET':
        print(request.get_full_path())
        latestSnap = TelemetryTracker.objects.latest('generatedTimestamp')  # wrap in list(), because QuerySet is not JSON serializable

        data={
                "tempInternal"        :   latestSnap.tempInternal      ,
                "humInternal"         :   latestSnap.humInternal       ,
                "tempCab"             :   latestSnap.tempCab           ,
                "humCab"              :   latestSnap.humCab            ,
                "batteryV"            :   latestSnap.batteryV          ,
                "batteryIP"           :   latestSnap.batteryIP         ,
                "batteryIN"           :   latestSnap.batteryIN         ,
                "SoC"                 :   latestSnap.SoC               ,
                "PVV"                 :   latestSnap.PVV               ,
                "PVI"                 :   latestSnap.PVI               ,
                "lightPWM"            :   latestSnap.lightPWM          ,
                "bInverter"           :   latestSnap.bInverter         ,
                "bUVLO"               :   latestSnap.bUVLO             ,
                "bFridge"             :   latestSnap.bFridge           ,
                "generatedTimestamp"  :   latestSnap.generatedTimestamp,
                "recievedTimestamp"   :   latestSnap.recievedTimestamp
            }
        # print(data)
        return JsonResponse(data, safe=False)  # or JsonResponse({'data': data})



def timeseriesAPI(request):

    if request.method == 'GET':
        attribute= equest.POST.get('attribute'),
        SomeModel.objects.latest('generatedTimestamp')

        last_ten = TelemetryTracker.objects.filter().order_by('-id')[:100]
        last_ten_in_ascending_order = reversed(last_ten)

        return JsonResponse({"attribute":attribute,"timeseries":last_ten_in_ascending_order})

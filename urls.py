from django.urls import path, re_path
from possumTrack.views import  *
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  #as_view is methode in TemplateView
    path('snapshot', snapshotAPI, name='snapshotAPI'),  #loading end point, return 1 pair
    path('timeseries', timeseriesAPI, name='timeseriesAPI'), #loading end point, return 3 pair
    path('telemetry', telemetryAPI, name='telemetryAPI'),  #loading end point, return 1 pair
    path('geo', geoAPI, name='geoAPI'),  #loading end point, return 1 pair
    path('toggle', toggleAPI, name='toggleAPI'),  #loading end point, return 1 pair
    path('weather', weatherAPI, name='weatherAPI'),  #loading end point, return 1 pair

    # path('fetch', FetchAPI, name='home'), #loading end point, return 3 pair
]

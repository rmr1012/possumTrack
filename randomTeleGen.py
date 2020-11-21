
import datetime, random, requests
import pytz
data={
        "tempInternal"        :   random.randint(40,100),
        "humInternal"         :   random.randint(0,100),
        "tempCab"             :   random.randint(40,100),
        "humCab"              :   random.randint(0,100),
        "batteryV"            :   random.uniform(12,16),
        "batteryIP"           :   random.uniform(0,50),
        "batteryIN"           :   random.uniform(0,50),
        "SoC"                 :   random.uniform(0,100),
        "PVV"                 :   random.uniform(12,21),
        "PVI"                 :   random.uniform(0,8),
        "lightPWM"            :   random.randint(0,100),
        "bInverter"           :   0,
        "bUVLO"               :   random.randint(0,1),
        "bFridge"             :   random.randint(0,1),
        "generatedTimestamp"  :   datetime.datetime.now(pytz.timezone('US/Pacific'))
    }

r = requests.post('http://localhost:8000/possumTrack/telemetry', data = data)
print(r.content)


import datetime, random, requests
import pytz

import serial

class SerialWorker():
    '''
    Dedicated serial worker "lil jon" who always keeps an eye on the serial port
    '''
    def __init__(self):
        super().__init__()

        self.new=False
        self.command=''
        self.buff=''

        self.die=False
        print('lil jon was born but not setup')

        self.ready=False

    def setup(self,serialID):
        self.ser=serial.Serial(serialID,115200)
        self.serialID=serialID
        self.thread.start()
        print('lil jon is setup'+self.serialID)
        self.ready=True

    def writeLine(self,command):
        if not self.new:
            self.command=command
            self.new=True

    def clear(self):
        self.buff=''
    def getText(self):
        return self.buff
    def run(self):
        print('lil jon started working'+self.serialID)
        try:
            while True:
                if self.die==True:
                    print('lil jon just got killed :((('+self.serialID)
                    return True
                if self.new:
                    self.ser.write(bytes(self.command,'ascii'))
                    self.new=False
                else:
                    try:
                        if self.ser.inWaiting()>0: #if incoming bytes are waiting to be read from the self.serial input buffer
                            newContent=self.ser.read(self.ser.inWaiting()).decode('ascii') #read the bytes and convert from binary array to ASCII
                            self.buff += newContent

                            self.proocessBuffer()
                    except Exception as e:
                        print('lil jon oops'+self.serialID)
        except Exception as e:
            print('lil jon just died :((('+self.serialID)
            print(str(e))
    def proocessBuffer(self):
        if "\n" in self.buff:
            rows=self.buff.split("\n")

            if "\n" is not self.buff[-1]:
                self.buff=rows[-1]
                del rows[-1]
            else:
                self.buff=''

            for row in rows:
                up
        else:
            return



if __name__ == "__main__":

    ser = serial.Serial("/dev/ttypa",115200)

    while True:
        if self.die==True:
            print('lil jon just got killed :((('+self.serialID)
            return True
        if self.new:
            self.ser.write(bytes(self.command,'ascii'))
            self.new=False
        else:
            try:
                if self.ser.inWaiting()>0: #if incoming bytes are waiting to be read from the self.serial input buffer
                    newContent=self.ser.read(self.ser.inWaiting()).decode('ascii') #read the bytes and convert from binary array to ASCII
                    self.buff += newContent
            except Exception as e:
                print('lil jon oops'+self.serialID)

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

import requests
from matplotlib import pyplot as plt
from scipy.ndimage.filters import uniform_filter1d as ufd
import numpy as np
import time
import datetime

import scipy.stats as stats
from sklearn import preprocessing

### Parameters ###

timeStep = 120     # seconds interval between readings
year = 2021     # year readings began
windowSize = 5     # rolling average smoothing to be applied
dataRAW = requests.get("http://window.eu.ngrok.io/pull")     # location of data

### Initialise Data ###

init_time = dataRAW.json()[0]['time']
date_time = datetime.datetime(year, int(init_time[0]), int(init_time[1]), int(init_time[2]), 0, 0)
time_code = time.mktime(date_time.timetuple())

### Extract and clean time series datasets ###

i_temp = []
i_hum = []
o_temp = []
o_hum = []
o_rain = []
o_wind = []

allData = [i_temp, i_hum, o_temp, o_hum, o_rain, o_wind]

for time in dataRAW.json():

    i_temp.append(time['local']['temp'])
    i_hum.append(time['local']['hum'])
    o_temp.append(time['weather']['temp'])
    o_hum.append(time['weather']['hum'])
    o_rain.append(time['weather']['rain'])
    o_wind.append(time['weather']['wind'])

for set in allData:
    for i, point in enumerate(set):
        if point == "NaN":
            set[i] = float(0)
        else:
            set[i] = float(point)

### Rolling average smoothing ###

i_temp = ufd(i_temp, windowSize)
i_hum = ufd(i_hum, windowSize)
o_temp = ufd(o_temp, windowSize)
o_hum = ufd(o_hum, windowSize)
o_rain = ufd(o_rain, windowSize)
o_wind = ufd(o_wind, windowSize)

### Create differential data sets ###

d_i_temp = np. gradient(i_temp)
d_i_hum = np. gradient(i_hum)
d_o_temp = np. gradient(o_temp)
d_o_hum = np. gradient(o_hum)
d_o_rain = np. gradient(o_rain)
d_o_wind = np. gradient(o_wind)

d_allData = [d_i_temp, d_i_hum, d_o_temp, d_o_hum, d_o_rain, d_o_wind]

### Functions ###

def plotAll(list):
    for i, data in enumerate(list):
        plt.figure(i)
        plt.plot(data)
    plt.show()


def findSteep(data, threashold, direction):
    log = []
    if direction == "below":
        for i, point in enumerate(data):
            if point < threashold:
                log.append(i)
            else:
                pass
    elif direction == "above":
        for i, point in enumerate(data):
            if point > threashold:
                log.append(i)
            else:
                pass
    return log


def getTimes(data, dt = timeStep, t0 = time_code):
    newData = []
    for range in data:
        t_s = range[0] * dt + t0
        t_e = range[1] * dt + t0
        start = str(datetime.datetime.utcfromtimestamp(t_s))
        end = str(datetime.datetime.utcfromtimestamp(t_e))
        newData.append((start, end))
    return newData


def findGroups(data):
    record = {}
    middles = []
    for i, x in enumerate(data):
        try:
            next = data[i+1] -1
            prev = data[i-1] +1
            if x == next and x != prev:
                record[x] = 'start'
            elif x == next and x == prev:
                middles.append(x)
            elif x == prev and x != next:
                record[x] = 'end'
        except IndexError:
            record[x] = 'end'
    return record


def showTemperatureLoses(printOut=True):
    losses = findSteep(d_i_temp, -0.1, "below")
    record = findGroups(losses)
    eventsList = list(record)
    eventsList.reverse()
    events = []
    while len(eventsList) > 0:
        start = eventsList.pop()
        end = eventsList.pop()
        events.append((start,end))
    if printOut:
        events_readable = getTimes(events)
        for event in events_readable:
            print("Teperature Drop! from {} until {}".format(event[0], event[1]))
        print("")
    return events

def showHumiditySpikes(printOut=True):
    losses = findSteep(d_i_hum, 0.75, "above")
    record = findGroups(losses)
    eventsList = list(record)
    eventsList.reverse()
    events = []
    while len(eventsList) > 0:
        start = eventsList.pop()
        end = eventsList.pop()
        events.append((start,end))
    if printOut:
        events_readable = getTimes(events)
        for event in events_readable:
            print("Humidity Spike! from {} until {}".format(event[0], event[1]))
        print("")
    return events

def testPearson(setA, setB):
    r, p = stats.pearsonr(setA, setB)
    print(r)

    a_shaped = setA.reshape(1,-1)
    b_shaped = setB.reshape(1,-1)

    a_norm = preprocessing.normalize(a_shaped)
    b_norm = preprocessing.normalize(b_shaped)

    plt.plot(a_norm[0])
    plt.plot(b_norm[0])
    plt.show()

### Opperations ###

#plotAll(allData)
#plotAll(d_allData)
#showTemperatureLoses(printOut=False)
#showHumiditySpikes(printOut=False)
#testPearson(A, B)

datasets = {
    "i_temp": i_temp,
    "i_hum": i_hum,
    "o_temp": o_temp,
    "o_hum": o_hum,
    "o_rain": o_rain,
    "o_wind": o_wind,
    "d_i_temp": d_i_temp,
    "d_i_hum": d_i_hum,
    "d_o_temp": d_o_temp,
    "d_o_hum": d_o_hum,
    "d_o_rain": d_o_rain,
    "d_o_wind": d_o_wind,
}

running = True
while running:
    res = input("plot | plotD | temp | hum | test | end \n")
    if res == "plot":
        plotAll(allData)
    elif res == "plotD":
        plotAll(d_allData)
    elif res == "temp":
        showTemperatureLoses(printOut=True)
    elif res == "hum":
        showHumiditySpikes(printOut=True)
    elif res == "test":
        setA = datasets[input("<i_temp, i_hum, o_temp, o_hum, o_rain, o_wind, d_i_temp, d_i_hum, d_o_temp, d_o_hum, d_o_rain, d_o_wind>")]
        setB = datasets[input("<i_temp, i_hum, o_temp, o_hum, o_rain, o_wind, d_i_temp, d_i_hum, d_o_temp, d_o_hum, d_o_rain, d_o_wind>")]
        testPearson(setA, setB)
    elif res == "end":
        running = False
    else:
        print("invalid")



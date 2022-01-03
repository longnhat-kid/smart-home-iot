from Adafruit_IO import MQTTClient
import time
from mqttCallbacks import *
from ai_detect_person import *
from hiveMQTT import *


client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

ackTimer = g.TIMEOUT_MS
longSleepTimer = g.LONG_SLEEP_MS
goToSleep = False
timeToCallAI = g.TIME_TO_CALL_AI

def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[1] == "BEDROOMTEMP":
        g.buffer.append({"feed_id": "bedroom-temp", "payload": splitData[2], "numOfAttempt": 0})
    elif splitData[1] == "BEDROOMLIGHT":
        g.buffer.append({"feed_id": "bedroom-light", "payload": splitData[2], "numOfAttempt": 0})
    elif splitData[1] == "BEDROOMSMOKE":
        g.buffer.append({"feed_id": "bedroom-smoke", "payload": splitData[2], "numOfAttempt": 0})
    elif splitData[1] == "BEDROOMSPEAKER":
        g.buffer.append({"feed_id": "bedroom-speaker", "payload": splitData[2], "numOfAttempt": 0})
    elif splitData[1] == "HALLINFRARED":
        g.buffer.append({"feed_id": "hall-infrared", "payload": splitData[2], "numOfAttempt": 0})
    elif splitData[1] == "HALLLIGHT":
        g.buffer.append({"feed_id": "hall-light", "payload": splitData[2], "numOfAttempt": 0})
    else:
        g.buffer.append({"feed_id": "no-exist", "payload": splitData[2], "numOfAttempt": 0})

mess = ""
def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

while True:
    readSerial()
    if g.waitForSubscribe:
        time.sleep(3)
        g.waitForSubscribe = False

    if timeToCallAI == 0:
        detectPerson()
        timeToCallAI = g.TIME_TO_CALL_AI

    if g.numOfFailed >= g.MAX_NUM_OF_TOTAL_ATTEMPTS and ackTimer == 0 and g.buffer.__len__() > 0:
        print(str(g.numOfAttempts) + " attempts failed. Stop system for 60s then try again.")
        longSleepTimer = g.LONG_SLEEP_MS
        g.numOfFailed = 0
        goToSleep = True

    if g.numOfAttempts >= g.MAX_NUM_OF_PARTIAL_ATTEMPTS and ackTimer == 0 and g.buffer.__len__() > 0:
        if g.buffer[0]["numOfAttempt"] >= g.MAX_NUM_OF_REMOVE_ATTEMPTS:
            print("*******************")
            ser.write((g.lastFeedId + ":" + str(g.lastPayload) + ":" + "ERROR" + "#").encode())
            print("Attempt resent with topic " + g.lastFeedId + " failed, remove payload !!")
            g.buffer.pop(0)
            g.lastSentOK = True
            g.numOfFailed += 1
        else:
            g.buffer[0]["numOfAttempt"] += 1
            print("*******************")
            print("Move payload with topic " + g.lastFeedId + " to end of buffer !!")
            g.buffer.append(g.buffer[0])
            g.buffer.pop(0)
            g.numOfAttempts = 0
            g.lastSentOK = True

    if not g.lastSentOK and ackTimer == 0 and not goToSleep and g.buffer.__len__() > 0:
        ackTimer = g.TIMEOUT_MS
        send(client, g.lastFeedId, g.lastPayload, True)
        g.numOfAttempts += 1
        print("Attempt resent " + g.lastFeedId + ": " + str(g.numOfAttempts))

    if g.lastSentOK and g.buffer.__len__() > 0:
        g.lastPayload = g.buffer[0].get("payload")
        g.lastFeedId = g.buffer[0].get("feed_id")
        g.lastSentOK = False
        ackTimer = g.TIMEOUT_MS
        send(client, g.lastFeedId, g.lastPayload)

    if longSleepTimer == 0 and g.buffer.__len__() > 0:
        goToSleep = False

    if ackTimer > 0 and g.buffer.__len__() > 0:
        ackTimer -= 1
    if longSleepTimer > 0 and g.buffer.__len__() > 0:
        longSleepTimer -= 1
    if timeToCallAI > 0:
        timeToCallAI -= 1

    time.sleep(0.001)


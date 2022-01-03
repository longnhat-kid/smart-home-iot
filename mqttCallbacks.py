from aio_config import *
import sys
import globals as g
from iot_serial import *

def connected(client):
    print("Ket noi thanh cong...")
    for feed_id in AIO_FEEDS_ID:
        client.subscribe(feed_id)

def subscribe(client , userdata , mid , granted_qos):
    print("Subcribe thanh cong...")

def disconnected(client):
    print("Ngat ket noi...")
    sys.exit(1)

def message(client , feed_id , payload):
    print("ACK:  " + payload)
    if g.lastFeedId == feed_id and g.lastPayload == payload:
        print("success")
        g.lastSentOK = True
        g.numOfFailed = 0
        g.numOfAttempts = 0
        g.buffer.pop(0)
    if g.lastFeedId != feed_id:
        ser.write((feed_id + ":" + str(payload) + "#").encode())

def send(client, topic, payload, resend = False):
    print("-------------------")
    client.publish(topic, payload)
    if resend:
        print("Re-sent payload: " + str(payload) + " of topic: " + topic)
    else:
        print("Sent payload: " + str(payload) + " of topic: " + topic)

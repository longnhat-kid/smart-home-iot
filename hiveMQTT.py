import paho.mqtt.client as mqtt
from iot_serial import *

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected HiveMQTT successfully")
    else:
        print("Connect HiveMQTT returned result code: " + str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Received message from HiveMQTT: " + msg.topic + " -> " + msg.payload.decode("utf-8"))
    ser.write((msg.topic + ":" + str(msg.payload.decode("utf-8")) + "#").encode())

# create the client
clientHive = mqtt.Client()
clientHive.on_connect = on_connect
clientHive.on_message = on_message

# enable TLS
clientHive.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

# set username and password
clientHive.username_pw_set("lionelnhat26", "01679505953aaB")

# connect to HiveMQ Cloud on port 8883
clientHive.connect("9ffce779bd4242b79eeee549796af5c7.s1.eu.hivemq.cloud", 8883)

# subscribe to the topic "my/test/topic"
clientHive.subscribe("topic/bolb")

clientHive.loop_start()
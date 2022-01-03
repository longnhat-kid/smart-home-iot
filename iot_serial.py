import serial.tools.list_ports

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "com0com" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort


isComPortAvailable = False
if getPort() != "None":
    ser = serial.Serial(port=getPort(), baudrate=115200)
    isComPortAvailable = True










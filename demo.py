import paho.mqtt.client as mqtt
import time
import json
import random
from vehicle import Vehicle

brokers = []

demoCam = '''{
    "accEngaged": true,
    "acceleration": 0,
    "altitude": 800001,
    "altitudeConf": 15,
    "brakePedal": true,
    "collisionWarning": true,
    "cruiseControl": true,
    "curvature": 1023,
    "driveDirection": "FORWARD",
    "emergencyBrake": true,
    "gasPedal": false,
    "heading": 3601,
    "headingConf": 127,
    "latitude": 400000000,
    "length": 100,
    "longitude": -80000000,
    "semiMajorConf": 4095,
    "semiMajorOrient": 3601,
    "semiMinorConf": 4095,
    "specialVehicle": {
        "publicTransportContainer": {
            "embarkationStatus": false
        }
    },
    "speed": 16383,
    "speedConf": 127,
    "speedLimiter": true,
    "stationID": 1,
    "stationType": 15,
    "width": 30,
    "yawRate": 0
}'''

def createCam(id):
    return '''{
    "accEngaged": true,
    "acceleration": 0,
    "altitude": 800001,
    "altitudeConf": 15,
    "brakePedal": true,
    "collisionWarning": true,
    "cruiseControl": true,
    "curvature": 1023,
    "driveDirection": "FORWARD",
    "emergencyBrake": true,
    "gasPedal": false,
    "heading": 3601,
    "headingConf": 127,
    "latitude": 400000000,
    "length": 100,
    "longitude": -80000000,
    "semiMajorConf": 4095,
    "semiMajorOrient": 3601,
    "semiMinorConf": 4095,
    "specialVehicle": {
        "publicTransportContainer": {
            "embarkationStatus": false
        }
    },
    "speed": 16383,
    "speedConf": 127,
    "speedLimiter": true,
    "stationID": '''+str(id)+''',
    "stationType": 15,
    "width": 30,
    "yawRate": 0
}'''

demoDenm = '''{
    "management": {
        "actionID": {
            "originatingStationID": 1798587532,
            "sequenceNumber": 0
        },
        "detectionTime": 1626453837.658,
        "referenceTime": 1626453837.658,
        "eventPosition": {
            "latitude": 40.637799251415686,
            "longitude": -8.652353364491056,
            "positionConfidenceEllipse": {
                "semiMajorConfidence": 0,
                "semiMinorConfidence": 0,
                "semiMajorOrientation": 0
            },
            "altitude": {
                "altitudeValue": 0,
                "altitudeConfidence": 1
            }
        },
        "validityDuration": 0,
        "stationType": 0
    },
    "situation": {
        "informationQuality": 7,
        "eventType": {
            "causeCode": 14,
            "subCauseCode": 14
        }
    }
}'''

def createDenm(id):
    return '''{
    "accEngaged": true,
    "acceleration": 0,
    "altitude": 800001,
    "altitudeConf": 15,
    "brakePedal": true,
    "collisionWarning": true,
    "cruiseControl": true,
    "curvature": 1023,
    "driveDirection": "FORWARD",
    "emergencyBrake": true,
    "gasPedal": false,
    "heading": 3601,
    "headingConf": 127,
    "latitude": 400000000,
    "length": 100,
    "longitude": -80000000,
    "semiMajorConf": 4095,
    "semiMajorOrient": 3601,
    "semiMinorConf": 4095,
    "specialVehicle": {
        "publicTransportContainer": {
            "embarkationStatus": false
        }
    },
    "speed": 16383,
    "speedConf": 127,
    "speedLimiter": true,
    "stationID": '''+str(id)+''',
    "stationType": 15,
    "width": 30,
    "yawRate": 0
}'''

row_ls = [1,1,2,2,3,3] #1 -> right, 2 -> middle, 3 -> left
exit_ls = [1,2,3,random.randint(1, 3),random.randint(1, 3),random.randint(1, 3)]
random.shuffle(row_ls)
random.shuffle(exit_ls)
vehicle1 = Vehicle(row_ls.pop(),exit_ls.pop(),1)
vehicle2 = Vehicle(row_ls.pop(),exit_ls.pop(),2)
vehicle3 = Vehicle(row_ls.pop(),exit_ls.pop(),3)
vehicle4 = Vehicle(row_ls.pop(),exit_ls.pop(),4)
vehicle5 = Vehicle(row_ls.pop(),exit_ls.pop(),5)
vehicle6 = Vehicle(row_ls.pop(),exit_ls.pop(),6)
print(vehicle1.vehicle_info())
print(vehicle2.vehicle_info())
print(vehicle3.vehicle_info())
print(vehicle4.vehicle_info())
print(vehicle5.vehicle_info())
print(vehicle6.vehicle_info())

def on_connect(client, userdata, flags, rc):
    print('Connected with code ' + str(rc))
    client.subscribe('vanetza/out/cam')
    client.subscribe('vanetza/out/denm')

def on_message1(client, userdata, msg):
    message = json.loads(msg.payload)
    # print('OBU1: ' + str(msg.topic) + '\t from OBU' + str(message['stationID']))
    if msg.topic == 'vanetza/out/cam':
        print('OBU1: ' + 'CAM ' ' from OBU' + str(message['stationID']))
    elif msg.topic == 'vanetza/out/denm':
        print('OBU1: ' + 'DENM' + ' from OBU' + str(message['stationID']))

def on_message2(client, userdata, msg):
    message = json.loads(msg.payload)
    # print('OBU2: ' + str(msg.topic) + '\t from OBU' + str(message['stationID']))
    if msg.topic == 'vanetza/out/cam':
        print('OBU2: ' + 'CAM ' ' from OBU' + str(message['stationID']))
    elif msg.topic == 'vanetza/out/denm':
        print('OBU2: ' + 'DENM' + ' from OBU' + str(message['stationID']))

def on_message3(client, userdata, msg):
    message = json.loads(msg.payload)
    # print('OBU3: ' + str(msg.topic) + '\t from OBU' + str(message['stationID']))
    if msg.topic == 'vanetza/out/cam':
        print('OBU3: ' + 'CAM ' ' from OBU' + str(message['stationID']))
    elif msg.topic == 'vanetza/out/denm':
        print('OBU3: ' + 'DENM' + ' from OBU' + str(message['stationID']))

def on_message4(client, userdata, msg):
    message = json.loads(msg.payload)
    # print('OBU4: ' + str(msg.topic) + '\t from OBU' + str(message['stationID']))
    if msg.topic == 'vanetza/out/cam':
        print('OBU4: ' + 'CAM ' ' from OBU' + str(message['stationID']))
    elif msg.topic == 'vanetza/out/denm':
        print('OBU4: ' + 'DENM' + ' from OBU' + str(message['stationID']))

def on_message5(client, userdata, msg):
    message = json.loads(msg.payload)
    # print('OBU5: ' + str(msg.topic) + '\t from OBU' + str(message['stationID']))
    if msg.topic == 'vanetza/out/cam':
        print('OBU5: ' + 'CAM ' ' from OBU' + str(message['stationID']))
    elif msg.topic == 'vanetza/out/denm':
        print('OBU5: ' + 'DENM' + ' from OBU' + str(message['stationID']))

def on_message6(client, userdata, msg):
    message = json.loads(msg.payload)
    # print('OBU6: ' + str(msg.topic) + '\t from OBU' + str(message['stationID']))
    if msg.topic == 'vanetza/out/cam':
        print('OBU6: ' + 'CAM ' ' from OBU' + str(message['stationID']))
    elif msg.topic == 'vanetza/out/denm':
        print('OBU6: ' + 'DENM' + ' from OBU' + str(message['stationID']))

def loop_start():
    for broker in brokers:
        broker.loop_start()

def loop_stop():
    for broker in brokers:
        broker.loop_stop(force=False)

for i in range(1,7):
    obu_name = 'broker'+str(i)
    client = mqtt.Client(obu_name)
    brokers.append(client)

idx = 1
for broker in brokers:
    broker.on_connect = on_connect
    if idx == 1: broker.on_message = on_message1
    elif idx == 2: broker.on_message = on_message2
    elif idx == 3: broker.on_message = on_message3
    elif idx == 4: broker.on_message = on_message4
    elif idx == 5: broker.on_message = on_message5
    elif idx == 6: broker.on_message = on_message6
    ip = '192.168.98.1' + str(idx)
    broker.connect_async(ip)
    idx = idx + 1

loop_start()
time.sleep(0.1)

idx = 0
running = True
while running:
    print('####################')
    brokers[0].publish('vanetza/in/cam', str(createCam(1)))
    brokers[1].publish('vanetza/in/cam', str(createCam(2)))
    brokers[2].publish('vanetza/in/cam', str(createCam(3)))
    brokers[3].publish('vanetza/in/cam', str(createCam(4)))
    brokers[4].publish('vanetza/in/cam', str(createCam(5)))
    brokers[5].publish('vanetza/in/cam', str(createCam(6)))
    if idx%5 == 0:
        brokers[0].publish('vanetza/in/denm', str(demoDenm))
        brokers[1].publish('vanetza/in/denm', str(demoDenm))
        brokers[2].publish('vanetza/in/denm', str(demoDenm))
        brokers[3].publish('vanetza/in/denm', str(demoDenm))
        brokers[4].publish('vanetza/in/denm', str(demoDenm))
        brokers[5].publish('vanetza/in/denm', str(demoDenm))
    idx = idx + 1
    time.sleep(10)

loop_stop()
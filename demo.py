import paho.mqtt.client as mqtt
import time
import json
import random
import geopy
import geopy.distance
from vehicle import Vehicle

brokers = []

initial_coords = [[41.198193, -8.627468, 4], [41.198187, -8.627429, 5], [41.198183, -8.627389, 6], [41.198290, -8.627454, 1], [41.198287, -8.627414, 2], [41.198282, -8.627371, 3]]

def createCam(id, latitude, longitude,speed):
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
    "latitude": '''+str(latitude)+''',
    "length": 10.0,
    "longitude": '''+str(longitude)+''',
    "semiMajorConf": 4095,
    "semiMajorOrient": 3601,
    "semiMinorConf": 4095,
    "specialVehicle": {
        "publicTransportContainer": {
            "embarkationStatus": false
        }
    },
    "speed": '''+str(speed)+''',
    "speedConf": 127,
    "speedLimiter": true,
    "stationID": '''+str(id)+''',
    "stationType": 15,
    "width": 3.0,
    "yawRate": 0
}'''

def createDenm(id,causeCode):
    return '''{
    "management": {
        "actionID": {
            "originatingStationID": '''+str(id)+''',
            "sequenceNumber": 0
        },
        "detectionTime": 1626453837.658,
        "referenceTime": 1626453837.658,
        "eventPosition": {
            "latitude": 41.198193,
            "longitude": -8.627468,
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
            "causeCode": '''+str(causeCode[0])+''',
            "subCauseCode": '''+str(causeCode[1])+'''
        }
    }
}'''

exit_ls = [1,2,3,random.randint(1, 3),random.randint(1, 3),random.randint(1, 3)]
random.shuffle(initial_coords)
random.shuffle(exit_ls)
vehicle1 = Vehicle(1, exit_ls.pop(),initial_coords.pop())
vehicle2 = Vehicle(2, exit_ls.pop(),initial_coords.pop())
vehicle3 = Vehicle(3, exit_ls.pop(),initial_coords.pop())
vehicle4 = Vehicle(4, exit_ls.pop(),initial_coords.pop())
vehicle5 = Vehicle(5, exit_ls.pop(),initial_coords.pop())
vehicle6 = Vehicle(6, exit_ls.pop(),initial_coords.pop())
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

#lists to store other obu's coordinates and then calculate my position on the road
ls1=[]
ls2=[]
ls3=[]
ls4=[]
ls5=[]
ls6=[]

def on_message1(client, userdata, msg):
    message = json.loads(msg.payload)
    #print(message)
    
    if msg.topic == 'vanetza/out/cam':
        if len(ls1) < 5:
            ls1.append((message['latitude'],message['longitude']))
        else:
            vehicle1.get_position(ls1)
            ls1.clear()
        #print('OBU1: ' + 'CAM ' ' from OBU' + str(message['stationID']))
    elif msg.topic == 'vanetza/out/denm':
        print(message)
        pass
        # print('OBU1: ' + 'DENM' + ' from OBU' + str(message['stationID']))
        # print(message['fields']['denm']['situation']['eventType']['causeCode'])
        # print(message['fields']['denm']['management']['eventPosition']['longitude'])

def on_message2(client, userdata, msg):
    message = json.loads(msg.payload)
    if msg.topic == 'vanetza/out/cam':
        if len(ls2) < 5:
            ls2.append((message['latitude'],message['longitude']))
        else:
            vehicle2.get_position(ls2)
            ls2.clear()
        # print('OBU2: ' + 'CAM ' ' from OBU' + str(message['stationID']))
    elif msg.topic == 'vanetza/out/denm':
        pass
        # print('OBU2: ' + 'DENM' + ' from OBU' + str(message['stationID']))

def on_message3(client, userdata, msg):
    message = json.loads(msg.payload)
    if msg.topic == 'vanetza/out/cam':
        if len(ls3) < 5:
            ls3.append((message['latitude'],message['longitude']))
        else:
            vehicle3.get_position(ls3)
            ls3.clear()
        # print('OBU3: ' + 'CAM ' ' from OBU' + str(message['stationID']))
    elif msg.topic == 'vanetza/out/denm':
        pass
        # print('OBU3: ' + 'DENM' + ' from OBU' + str(message['stationID']))

def on_message4(client, userdata, msg):
    message = json.loads(msg.payload)
    if msg.topic == 'vanetza/out/cam':
        if len(ls4) < 5:
            ls4.append((message['latitude'],message['longitude']))
        else:
            vehicle4.get_position(ls4)
            ls4.clear()
        # print('OBU4: ' + 'CAM ' ' from OBU' + str(message['stationID']))
    elif msg.topic == 'vanetza/out/denm':
        pass
        # print('OBU4: ' + 'DENM' + ' from OBU' + str(message['stationID']))

def on_message5(client, userdata, msg):
    message = json.loads(msg.payload)
    if msg.topic == 'vanetza/out/cam':
        if len(ls5) < 5:
            ls5.append((message['latitude'],message['longitude']))
        else:
            vehicle5.get_position(ls5)
            ls5.clear()
        # print('OBU5: ' + 'CAM ' ' from OBU' + str(message['stationID']))
    elif msg.topic == 'vanetza/out/denm':
        pass
        # print('OBU5: ' + 'DENM' + ' from OBU' + str(message['stationID']))

def on_message6(client, userdata, msg):
    message = json.loads(msg.payload)
    if msg.topic == 'vanetza/out/cam':
        if len(ls6) < 5:
            ls6.append((message['latitude'],message['longitude']))
        else:
            vehicle6.get_position(ls6)
            ls6.clear()
        # print('OBU6: ' + 'CAM ' ' from OBU' + str(message['stationID']))
    elif msg.topic == 'vanetza/out/denm':
        pass
        # print('OBU6: ' + 'DENM' + ' from OBU' + str(message['stationID']))

def loop_start():
    for broker in brokers:
        broker.loop_start()

def loop_stop():
    for broker in brokers:
        broker.loop_stop(force=False)

def update_geo_point():
    vehicle1.update_geo_point()
    vehicle2.update_geo_point()
    vehicle3.update_geo_point()
    vehicle4.update_geo_point()
    vehicle5.update_geo_point()
    vehicle6.update_geo_point()

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
time.sleep(1)

idx = 0
phase = 0
running = True
while running:
    print('####################' + str(idx))
    brokers[0].publish('vanetza/in/cam', str(createCam(1,vehicle1.geo_point.latitude,vehicle1.geo_point.longitude,vehicle1.speed)))
    brokers[1].publish('vanetza/in/cam', str(createCam(2,vehicle2.geo_point.latitude,vehicle2.geo_point.longitude,vehicle2.speed)))
    brokers[2].publish('vanetza/in/cam', str(createCam(3,vehicle3.geo_point.latitude,vehicle3.geo_point.longitude,vehicle3.speed)))
    brokers[3].publish('vanetza/in/cam', str(createCam(4,vehicle4.geo_point.latitude,vehicle4.geo_point.longitude,vehicle4.speed)))
    brokers[4].publish('vanetza/in/cam', str(createCam(5,vehicle5.geo_point.latitude,vehicle5.geo_point.longitude,vehicle5.speed)))
    brokers[5].publish('vanetza/in/cam', str(createCam(6,vehicle6.geo_point.latitude,vehicle6.geo_point.longitude,vehicle6.speed)))
    #print(vehicle1.vehicle_info())
    update_geo_point()
    #print(vehicle1.vehicle_info())
    
    if phase==0 and idx != 0:
        if idx%10 == 0:
            brokers[0].publish('vanetza/in/denm', str(createDenm(1,vehicle1.process_initial_cause_code())))
            brokers[1].publish('vanetza/in/denm', str(createDenm(2,vehicle2.process_initial_cause_code())))
            brokers[2].publish('vanetza/in/denm', str(createDenm(3,vehicle3.process_initial_cause_code())))
            brokers[3].publish('vanetza/in/denm', str(createDenm(4,vehicle4.process_initial_cause_code())))
            brokers[4].publish('vanetza/in/denm', str(createDenm(5,vehicle5.process_initial_cause_code())))
            brokers[5].publish('vanetza/in/denm', str(createDenm(6,vehicle6.process_initial_cause_code())))
            phase=1
    if(phase==1):
        #print("MUDOU DE FASE")
        #time.sleep(20)
        pass
    idx = idx + 1
    time.sleep(1)

loop_stop()
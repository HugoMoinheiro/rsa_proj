import paho.mqtt.client as mqtt
import time
import json
import random
import geopy
import geopy.distance
from vehicle import Vehicle

class bcolors: #nicer prints
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

brokers = []

# initial_coords = [[41.198193, -8.627454, 4],
#                   [41.198187, -8.627414, 5],
#                   [41.198183, -8.627371, 6], 
#                   [41.198290, -8.627454, 1], 
#                   [41.198287, -8.627414, 2], 
#                   [41.198282, -8.627371, 3]]

initial_coords = [[38.017080, -99.314110, 1],
                  [38.017080, -99.314100, 2],
                  [38.017080, -99.314090, 3], 
                  [38.017070, -99.314110, 4], 
                  [38.017070, -99.314100, 5], 
                  [38.017070, -99.314090, 6]]

exit1coord = [38.020000, -99.314080]
exit2coord = [38.022000, -99.314080]
exit3coord = [38.024000, -99.314080]

phase = 0 #to control the timeline of the event
vehicle_exiting=0

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
center = Vehicle(7, 3, [38.017080, -99.314100, 7])
vehicle_list=[vehicle1,vehicle2,vehicle3,vehicle4,vehicle5,vehicle6,center]

def print_vehicle_list(): #easier way to see the vehicles in the list
    s="["
    for i in vehicle_list:
        s=s+str(i)+", "
    s=s+"]"
    print(s)
    pass

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
ls1_denm=[]
ls2_denm=[]
ls3_denm=[]
ls4_denm=[]
ls5_denm=[]
ls6_denm=[]

list1=[] #first value 
list2=[]
list3=[]
list4=[]
list5=[]
list6=[]

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
        if phase==1:
            if len(ls1_denm) < 5:
                ls1_denm.append((message['fields']['denm']['situation']['eventType']['causeCode'],message['fields']['denm']['situation']['eventType']['subCauseCode']))
            if len(ls1_denm) == 5:
                list1.append(vehicle1.decide(ls1_denm))
        elif phase==2:
            subCause = message['fields']['denm']['situation']['eventType']['causeCode']
            if vehicle1.my_pos==subCause:
                print("I'm vehicle 1 and some vehcile wants to trade position with me")
            vehicle1.update_geo_point_lane(list1[0])
            # vehicle1.update_speed()
        if vehicle_exiting==1:
            if vehicle1.end==0 and vehicle1.exit!=1:
                vehicle1.update_lane_after_exit(2)
                # vehicle1.update_speed()
        if vehicle_exiting==2:
            if vehicle1.end==0 and vehicle1.exit!=1 and vehicle1.exit!=2:
                vehicle1.update_lane_after_exit(3)
                # vehicle1.update_speed()
        
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
        if phase==1:
            if len(ls2_denm) < 5:
                ls2_denm.append((message['fields']['denm']['situation']['eventType']['causeCode'],message['fields']['denm']['situation']['eventType']['subCauseCode']))
            if len(ls2_denm) == 5:
                list2.append(vehicle2.decide(ls2_denm))
            # print('OBU2: ' + 'DENM' + ' from OBU' + str(message['stationID']))
        elif phase==2:
            subCause = message['fields']['denm']['situation']['eventType']['causeCode']
            if vehicle2.my_pos==subCause:
                print("I'm vehicle 2 and some vehcile wants to trade position with me")
            vehicle2.update_geo_point_lane(list2[0])
            # vehicle2.update_speed()
        if vehicle_exiting==1:
            if vehicle2.end==0 and vehicle2.exit!=1:
                vehicle2.update_lane_after_exit(2)
                # vehicle2.update_speed()
        if vehicle_exiting==2:
            if vehicle2.end==0 and vehicle2.exit!=1 and vehicle2.exit!=2:
                vehicle2.update_lane_after_exit(3)
                # vehicle2.update_speed()

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
        if phase==1:
            if len(ls3_denm) < 5:
                ls3_denm.append((message['fields']['denm']['situation']['eventType']['causeCode'],message['fields']['denm']['situation']['eventType']['subCauseCode']))
            if len(ls3_denm) == 5:
                list3.append(vehicle3.decide(ls3_denm))
            # print('OBU3: ' + 'DENM' + ' from OBU' + str(message['stationID']))
        elif phase==2:
            subCause = message['fields']['denm']['situation']['eventType']['causeCode']
            if vehicle3.my_pos==subCause:
                print("I'm vehicle 3 and some vehcile wants to trade position with me")
            vehicle3.update_geo_point_lane(list3[0])
            # vehicle3.update_speed()
        if vehicle_exiting==1:
            if vehicle3.end==0 and vehicle3.exit!=1:
                vehicle3.update_lane_after_exit(2)
                # vehicle3.update_speed()
        if vehicle_exiting==2:
            if vehicle3.end==0 and vehicle3.exit!=1 and vehicle3.exit!=2:
                vehicle3.update_lane_after_exit(3)
                # vehicle3.update_speed()

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
        if phase==1:
            if len(ls4_denm) < 5:
                ls4_denm.append((message['fields']['denm']['situation']['eventType']['causeCode'],message['fields']['denm']['situation']['eventType']['subCauseCode']))
            if len(ls4_denm) == 5:
                list4.append(vehicle4.decide(ls4_denm))
            # print('OBU4: ' + 'DENM' + ' from OBU' + str(message['stationID']))
        elif phase==2:
            subCause = message['fields']['denm']['situation']['eventType']['causeCode']
            if vehicle4.my_pos==subCause:
                print("I'm vehicle 4 and some vehcile wants to trade position with me")
            vehicle4.update_geo_point_lane(list4[0])
            # vehicle4.update_speed()
        if vehicle_exiting==1:
            if vehicle4.end==0 and vehicle4.exit!=1:
                vehicle4.update_lane_after_exit(2)
                # vehicle4.update_speed()
        if vehicle_exiting==2:
            if vehicle4.end==0 and vehicle4.exit!=1 and vehicle4.exit!=2:
                vehicle4.update_lane_after_exit(3)
                # vehicle4.update_speed()

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
        if phase==1:
            if len(ls5_denm) < 5:
                ls5_denm.append((message['fields']['denm']['situation']['eventType']['causeCode'],message['fields']['denm']['situation']['eventType']['subCauseCode']))
            if len(ls5_denm) == 5:
                list5.append(vehicle5.decide(ls5_denm))
            # print('OBU5: ' + 'DENM' + ' from OBU' + str(message['stationID']))
        elif phase==2:
            subCause = message['fields']['denm']['situation']['eventType']['causeCode']
            if vehicle5.my_pos==subCause:
                print("I'm vehicle 5 and some vehcile wants to trade position with me")
            vehicle5.update_geo_point_lane(list5[0])
            # vehicle5.update_speed()
        if vehicle_exiting==1:
            if vehicle5.end==0 and vehicle5.exit!=1:
                vehicle5.update_lane_after_exit(2)
                # vehicle5.update_speed()
        if vehicle_exiting==2:
            if vehicle5.end==0 and vehicle5.exit!=1 and vehicle5.exit!=2:
                vehicle5.update_lane_after_exit(3)
                # vehicle5.update_speed()

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
        if phase==1:
            if len(ls6_denm) < 5:
                ls6_denm.append((message['fields']['denm']['situation']['eventType']['causeCode'],message['fields']['denm']['situation']['eventType']['subCauseCode']))
            if len(ls6_denm) == 5:
                list6.append(vehicle6.decide(ls6_denm))
            # print('OBU6: ' + 'DENM' + ' from OBU' + str(message['stationID']))
        elif phase==2:
            subCause = message['fields']['denm']['situation']['eventType']['causeCode']
            if vehicle6.my_pos==subCause:
                print("I'm vehicle 6 and some vehcile wants to trade position with me")
            vehicle6.update_geo_point_lane(list6[0])
            # vehicle6.update_speed()
        if vehicle_exiting==1:
            if vehicle6.end==0 and vehicle6.exit!=1:
                vehicle6.update_lane_after_exit(2)
                # vehicle6.update_speed()
        if vehicle_exiting==2:
            if vehicle6.end==0 and vehicle6.exit!=1 and vehicle6.exit!=2:
                vehicle6.update_lane_after_exit(3)
                # vehicle6.update_speed()

def print_road():
    estrada = "| Vehicle "
    for i in vehicle_list:
        if i.my_pos==1:
            estrada = estrada + str(i.id) + " - Vehicle "
    for i in vehicle_list:
        if i.my_pos==2:
            estrada = estrada + str(i.id) + " - Vehicle "
    for i in vehicle_list:
        if i.my_pos==3:
            estrada = estrada + str(i.id) + " |\n| Vehicle " 
    for i in vehicle_list:
        if i.my_pos==4:
            estrada = estrada + str(i.id) + " - Vehicle " 
    for i in vehicle_list:
        if i.my_pos==5:
            estrada = estrada + str(i.id) + " - Vehicle " 
    for i in vehicle_list:
        if i.my_pos==6:
            estrada = estrada + str(i.id) + " |" 
    print(bcolors.WARNING + estrada + bcolors.ENDC)

def print_lane():
    fila="-----------------------\n3rd lane"
    for i in vehicle_list:
        if i.lane==3:
            fila = fila + " Vehicle " + str(i.id) + " coord " + str(i.geo_point.latitude) + " " + str(i.geo_point.longitude) +  " "
    
    fila=fila+"\n-----------------------\n2nd lane:"

    for i in vehicle_list:
        if i.lane==2:
            fila = fila + " Vehicle " + str(i.id) + " coord " + str(i.geo_point.latitude) + " " + str(i.geo_point.longitude) +  " "
    
    fila=fila+"\n-----------------------\n1st lane:"

    for i in vehicle_list:
        if i.lane==1:
            fila = fila + " Vehicle " + str(i.id) + " coord " + str(i.geo_point.latitude) + " " + str(i.geo_point.longitude) +  " "

    print(bcolors.WARNING + fila + bcolors.ENDC)


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
    center.update_geo_point()

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
counter=0
def update_file():
    f = open("webproj/app/vehicle_coords.txt", "w")
    s=""
    for i in vehicle_list:
        s = s +str(i.id) + " " + str(i.geo_point.latitude) + " " + str(i.geo_point.longitude) + "\n"
    f.write(s)
    f.close()
running = True
while running:
    print('####################' + str(idx))
    update_file()
    brokers[0].publish('vanetza/in/cam', str(createCam(1,vehicle1.geo_point.latitude,vehicle1.geo_point.longitude,vehicle1.speed)))
    brokers[1].publish('vanetza/in/cam', str(createCam(2,vehicle2.geo_point.latitude,vehicle2.geo_point.longitude,vehicle2.speed)))
    brokers[2].publish('vanetza/in/cam', str(createCam(3,vehicle3.geo_point.latitude,vehicle3.geo_point.longitude,vehicle3.speed)))
    brokers[3].publish('vanetza/in/cam', str(createCam(4,vehicle4.geo_point.latitude,vehicle4.geo_point.longitude,vehicle4.speed)))
    brokers[4].publish('vanetza/in/cam', str(createCam(5,vehicle5.geo_point.latitude,vehicle5.geo_point.longitude,vehicle5.speed)))
    brokers[5].publish('vanetza/in/cam', str(createCam(6,vehicle6.geo_point.latitude,vehicle6.geo_point.longitude,vehicle6.speed)))
    #print(vehicle1.vehicle_info())
    update_geo_point()
    #print(vehicle1.vehicle_info())
    if idx>3:
        print_lane()
    
    if phase==0 and idx != 0:
        if idx%10 == 0:
            phase=1
            brokers[0].publish('vanetza/in/denm', str(createDenm(1,vehicle1.process_initial_cause_code())))
            brokers[1].publish('vanetza/in/denm', str(createDenm(2,vehicle2.process_initial_cause_code())))
            brokers[2].publish('vanetza/in/denm', str(createDenm(3,vehicle3.process_initial_cause_code())))
            brokers[3].publish('vanetza/in/denm', str(createDenm(4,vehicle4.process_initial_cause_code())))
            brokers[4].publish('vanetza/in/denm', str(createDenm(5,vehicle5.process_initial_cause_code())))
            brokers[5].publish('vanetza/in/denm', str(createDenm(6,vehicle6.process_initial_cause_code())))  
    elif(phase==1 and idx != 10):
        if idx%2 == 0:
            phase=2
            brokers[0].publish('vanetza/in/denm', str(createDenm(1,list1[0])))
            brokers[1].publish('vanetza/in/denm', str(createDenm(2,list2[0])))
            brokers[2].publish('vanetza/in/denm', str(createDenm(3,list3[0])))
            brokers[3].publish('vanetza/in/denm', str(createDenm(4,list4[0])))
            brokers[4].publish('vanetza/in/denm', str(createDenm(5,list5[0])))
            brokers[5].publish('vanetza/in/denm', str(createDenm(6,list6[0])))
    elif phase==2:
        for i in vehicle_list:
            # if i.exit==1 and i.geo_point.latitude>=41.201222:
            if i.exit==1 and i.geo_point.latitude>=exit1coord[0]:
                vehicle_exiting=1
                print("Veículo " + str(i.id) + " sai na primeira saída")
                brokers[i.id-1].publish('vanetza/in/denm', str(createDenm(i.id,[9,7])))
                vehicle_list.remove(i)
                print_vehicle_list()
                i.passed_exit()
            # if i.geo_point.latitude>=41.201422:
            if i.geo_point.latitude>=exit1coord[0]+0.0002:
                phase=3
            i.update_speed()
    elif phase==3:
        for i in vehicle_list:
            # if i.exit==2 and i.geo_point.latitude>=41.206052:
            if i.exit==2 and i.geo_point.latitude>=exit2coord[0]:
                vehicle_exiting=2
                print("Veículo " + str(i.id) + " sai na segunda saída")
                brokers[i.id-1].publish('vanetza/in/denm', str(createDenm(i.id,[9,7])))
                vehicle_list.remove(i)
                print_vehicle_list()
                i.passed_exit()
            # if i.geo_point.latitude>=41.206252:
            if i.geo_point.latitude>=exit2coord[0]+0.0002:
                phase=4
            i.update_speed()
        #print("MUDOU DE FASE")
        #time.sleep(20)
    elif phase==4:
        for i in vehicle_list:
            # if i.exit==3 and i.geo_point.latitude>=41.220500:
            if i.exit==3 and i.geo_point.latitude>=exit3coord[0]:
                print("Veículo " + str(i.id) + " sai na terceira saída")
                brokers[i.id-1].publish('vanetza/in/denm', str(createDenm(i.id,[9,7])))
                vehicle_list.remove(i)
                print_vehicle_list()
                i.passed_exit()
            # if i.geo_point.latitude>=41.206252:
            if i.geo_point.latitude>=exit3coord[0]+0.0002:
                phase=4
            i.update_speed()
        
    idx = idx + 1
    time.sleep(0.5)
    print('~~~~~~~~~~~~~~~~~~~~')
    print(vehicle1.speed)
    print(vehicle2.speed)
    print(vehicle3.speed)
    print(vehicle4.speed)
    print(vehicle5.speed)
    print(vehicle6.speed)
    print('~~~~~~~~~~~~~~~~~~~~')

loop_stop()
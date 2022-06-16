import geopy
import geopy.distance

class Vehicle:
    def __init__(self, id, exit, coords):
        self.exit=exit #1 - first exit, 2 - second exit, 3 - third exit
        self.id=id 
        self.speed=40 #km/h
        self.initial_coords=coords # initial latitude and longitude
        self.geo_point=geopy.Point(coords[0], coords[1]) # geo point to update the coordinates
        self.position_id=coords[2] # real position identifier
        self.direction=0 #0 = north, 90 = east, 180 – South, 270 or -90 west
        self.knows_pos=0 #boolean to calculate position if unknown
        self.my_pos=0 # position identifier that was calculated

    def vehicle_info(self):
        return f' Vehicle: {self.id}' + " / Exit: " + f'{self.exit}' + " / Speed: " + f'{self.speed}' + " / Position: " + f'{self.position_id}' + " / Latitude: " + f'{self.geo_point.latitude}' + " / Longitude: " + f'{self.geo_point.longitude}'
        
    def process_initial_cause_code(self):
        return (self.exit,self.my_pos)

    def update_speed(self, new_speed):
        self.speed=new_speed

    def update_geo_point(self):
        kilometers_traveled = self.speed / 3.6 / 1000 #gets the kilometers traveled in 1 second
        d = geopy.distance.distance(kilometers=kilometers_traveled)
        self.geo_point = d.destination(point=self.geo_point, bearing=0) #bearing = 0 = north

    # [41.198290, -8.6274/54, 1] [41.198287, -8.6274/14, 2] [41.198282, -8.6273/71, 3]
    # [41.198193, -8.6274/68, 4] [41.198187, -8.6274/29, 5] [41.198183, -8.6273/89, 6]

    def get_position(self,obu_coords):
        if self.knows_pos==0:
            line=0
            front=0
            lat_count=0
            long_count=0
            
            if self.direction==0:
                for i in obu_coords:
                    difference1 = self.initial_coords[0] - i[0]
                    difference2 = self.initial_coords[1] - i[1]
                    if difference1 > 0:
                        lat_count+=1
                    if difference2 > 0:
                        long_count+=1
                if lat_count>=3:
                    front=1
                else:
                    front=2
                if long_count>=4:
                    line=3
                elif long_count>=2:
                    line=2
                else:
                    line=1
            self.my_pos = self.get_pos(front,line)
            print("Vehicle " + str(self.id) + " real position: " + str(self.position_id) + "  ||  estimated positio: " + str(self.my_pos))
            self.knows_pos=1

    def get_pos(self,front,line):
        if front == 1:
            if line == 1:
                return 1
            elif line == 2:
                return 2
            elif line == 3:
                return 3
            else:
                return -1
        elif front == 2:
            if line == 1:
                return 4
            elif line == 2:
                return 5
            elif line == 3:
                return 6
            else:
                return -1
        else:
            return -1

    def decide(self, obu_stats):
        tuple=(0,0)
        found_car = False
        if self.exit == 1 and (self.my_pos==3 or self.my_pos==6):
            tuple=(1,7)
            print("Vehicle " + str(self.id) + " is already on the right lane (corret position)")
        elif self.exit == 2 and (self.my_pos==2 or self.my_pos==5):
            tuple=(1,7)
            print("Vehicle " + str(self.id) + " is already on the middle lane (corret position)")
        elif self.exit == 3 and (self.my_pos==1 or self.my_pos==4):
            tuple=(1,7)
            print("Vehicle " + str(self.id) + " is already on the left lane (corret position)")
        else:
            if self.exit == 1 and (self.my_pos==2 or self.my_pos==5): #saída direita e encontras-te no meio
                for i in obu_stats:
                    if (i[1]==3 or i[1]==6) and (i[0] == 3 or i[0] == 2):
                        tuple=(4,i[1])
                        found_car=True
                if not found_car:
                    tuple=(4,7)
                print("Vehicle " + str(self.id) + " wants to move 1 position to the right")
            elif self.exit == 1 and (self.my_pos==1 or self.my_pos==4): #saída direita e encontras-te na esquerda
                for i in obu_stats:
                    if (i[1]==2 or i[1]==5) and i[0] == 3:
                        tuple=(5,i[1])
                        found_car=True
                if not found_car:
                    tuple=(5,7)
                print("Vehicle " + str(self.id) + " wants to move 2 positions to the right")
            elif self.exit == 2 and (self.my_pos==3 or self.my_pos==6): #saída meio e encontras-te na diretia
                for i in obu_stats:
                    if (i[1]==2 or i[1]==5) and i[0] == 1:
                        tuple=(2,i[1])
                        found_car=True
                if not found_car:
                    tuple=(2,7)
                print("Vehicle " + str(self.id) + " wants to move 1 position to the left")
            elif self.exit == 2 and (self.my_pos==1 or self.my_pos==4): #saída meio e encontras-te na esquerda
                for i in obu_stats:
                    if (i[1]==2 or i[1]==5) and i[0] == 3:
                        tuple=(4,i[1])
                        found_car=True
                if not found_car:
                    tuple=(4,7)
                print("Vehicle " + str(self.id) + " wants to move 1 positions to the right")
            elif self.exit == 3 and (self.my_pos==3 or self.my_pos==6): #saída esquerda e encontras-te na direita
                for i in obu_stats:
                    if (i[1]==2 or i[1]==5) and i[0] == 1:
                        tuple=(3,i[1])
                        found_car=True
                if not found_car:
                    tuple=(3,7)
                print("Vehicle " + str(self.id) + " wants to move 2 position to the left")
            elif self.exit == 3 and (self.my_pos==2 or self.my_pos==5): #saída esquerda e encontras-te no meio
                for i in obu_stats:
                    if (i[1]==1 or i[1]==4) and (i[0] == 2 or i[1] == 1):
                        tuple=(2,i[1])
                        found_car=True
                if not found_car:
                    tuple=(2,7)
                print("Vehicle " + str(self.id) + " wants to move 1 positions to the left")
        lst = list(tuple)

        return lst

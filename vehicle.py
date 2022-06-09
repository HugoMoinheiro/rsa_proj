import geopy
import geopy.distance

class Vehicle:
    def __init__(self, id, exit, coords):
        #self.row=row
        self.exit=exit
        self.id=id
        self.speed=40 #km/h
        self.initial_coords=coords
        self.geo_point=geopy.Point(coords[0], coords[1])
        self.position_id=coords[2]
        self.direction=0 #0 = north, 90 = east, 180 – South, 270 or -90 west


    def vehicle_info(self):
        return f' Vehicle: {self.id}' + " / Exit: " + f'{self.exit}' + " / Speed: " + f'{self.speed}' + " / Position: " + f'{self.position_id}' + " / Latitude: " + f'{self.geo_point.latitude}' + " / Longitude: " + f'{self.geo_point.longitude}'
        
    def process_initial_cause_code(self):
        return self.exit

    def update_speed(self, new_speed):
        self.speed=new_speed

    def update_geo_point(self):
        kilometers_traveled = self.speed / 3.6 / 1000 #gets the kilometers traveled in 1 second
        d = geopy.distance.distance(kilometers=kilometers_traveled)
        self.geo_point = d.destination(point=self.geo_point, bearing=0) #bearing = 0 = north

    # [41.198290, -8.6274/54, 1] [41.198287, -8.6274/14, 2] [41.198282, -8.6273/71, 3]
    # [41.198193, -8.6274/68, 4] [41.198187, -8.6274/29, 5] [41.198183, -8.6273/89, 6]

    def get_position(self,obu_coords):
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
        my_pos = self.get_pos(front,line)
        print("Vehicle " + str(self.id) + " real position: " + str(self.position_id) + "  ||  estimated positio: " + str(my_pos))
    
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


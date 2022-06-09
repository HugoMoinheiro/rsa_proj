import geopy
import geopy.distance

class Vehicle:
    def __init__(self, id, exit, coords):
        #self.row=row
        self.exit=exit
        self.id=id
        self.speed=40 #km/h
        self.geo_point=geopy.Point(coords[0], coords[1])
        self.position_id=coords[2]


    def vehicle_info(self):
        return f' Vehicle: {self.id}' + " / Exit: " + f'{self.exit}' + " / Speed: " + f'{self.speed}' + " / Position: " + f'{self.position_id}' + " / Latitude: " + f'{self.geo_point.latitude}' + " / Longitude: " + f'{self.geo_point.longitude}'
        
    def process_initial_cause_code(self):
        return self.exit

    def update_speed(self, new_speed):
        self.speed=new_speed

    def update_geo_point(self):
        meters_traveled = self.speed / 3.6 #gets the meters traveled in 1 second
        d = geopy.distance.distance(meters=meters_traveled)
        self.geo_point = d.destination(point=self.geo_point, bearing=0) #bearing = 0 = north

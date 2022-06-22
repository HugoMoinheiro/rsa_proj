from django.shortcuts import render
from datetime import datetime
from pathlib import Path
import time
import json
from django.http import JsonResponse


filepath = Path(__file__).parent / "vehicle_coords.txt"

def home(request):
    #lias as coordenadas, colocar no dicionario
    tparams = {
        'title': 'Platoon Merging',
        'year': datetime.now().year,
        'refresh_rate': 1
    }
    return render(request, 'index.html', tparams)

def get_coords(request):
    start = time.time()

    car1_lat,car1_lon,car2_lat,car2_lon,car3_lat,car3_lon,car4_lat,car4_lon,car5_lat,car5_lon,car6_lat,car6_lon=[0]*12
    f = open(filepath, "r")
    for line in f:
        coords = line
        x = coords.split()
        print(x)
        if x[0] == '1':
            print("ENTRA")
            car1_lat = float(x[1])
            car1_lon = float(x[2])
        elif x[0] == '2':    
            car2_lat = float(x[1])
            car2_lon = float(x[2])
        elif x[0] == '3': 
            car3_lat = float(x[1])
            car3_lon = float(x[2])
        elif x[0] == '4': 
            car4_lat = float(x[1])
            car4_lon = float(x[2])
        elif x[0] == '5':
            car5_lat = float(x[1])
            car5_lon = float(x[2])
        elif x[0] == '6':
            car6_lat = float(x[1])
            car6_lon = float(x[2])

    tparams = {
        'title': 'Platoon Merging',
        'refresh_rate': 1,
        'car1_lat':car1_lat,
        'car1_lon':car1_lon,
        'car2_lat':car2_lat,
        'car2_lon':car2_lon,
        'car3_lat':car3_lat,
        'car3_lon':car3_lon,
        'car4_lat':car4_lat,
        'car4_lon':car4_lon,
        'car5_lat':car5_lat,
        'car5_lon':car5_lon,
        'car6_lat':car6_lat,
        'car6_lon':car6_lon,
    }
    tparams = json.dumps(tparams)
    loaded_r = json.loads(tparams)
    end = time.time()
    print(end - start)
    
    return JsonResponse(loaded_r)
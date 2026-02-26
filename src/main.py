import time
import os
import obd
import random
from vehicles import nissan, vw, simulator
import json

connection = obd.OBD()
logs = []
last_voice_alert = 0

if connection.is_connected():
    mode = "REAL"
    print("Scanning For Engine Codes")
    codes = connection.get_dtc()
else:
    mode = "SIMULATOR"
    print('No adapter found. Starting in SIMULATOR MODE')
    codes = [("P0420", "Catalyst System Efficiency Below Threshold")] # FAKE CODE
    time.sleep(2)

if codes:
    print(f"--- DIAGNOSTIC REPORT ---")
    for code_name, description in codes:
        with open("engine_codes_log.txt", "a") as f:
            f.write(f"{time.ctime()}: [{code_name}] - {description} \n")
    print("-" * 32)

def detect_vehicle(connection):
    if not connection.is_connected():
        return "SIMULATOR"
    
    try:
        vin_res = connection.query(obd.commands.VIN)
        if vin_res.is_null():
            return "UNKNOWN"
        
        vin = str(vin_res.value).upper()

        with open("config.json", "r") as f:
            brand_data = json.load(f)

        for brand, prefixes in brand_data.items():
            if any(vin.startswith(p) for p in prefixes):
                return brand
            
        return "UNKNOWN"
    except Exception as e:
        print(f"Detection Error: {e}")
        return "UNKNOWN"
    
vehicle_type = detect_vehicle(connection)
print(f"Configuring system for: {vehicle_type}")

NISSAN_OIL_TARGET = 75000
JETTA_OIL_TARGET = 153000


oil_announced = False

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    current_time = time.time() 

    miles_left = None  

    if mode == "REAL":
        
        if vehicle_type == "NISSAN":
            data = nissan.get_vitals(connection)

        elif vehicle_type == "JETTA" or vehicle_type == "AUDI":
            data = vw.get_vitals(connection)

        else:
            data = {"name": "Unknown", "rpm": 0, "temp_c": 0}

    else:
        data = simulator.get_vitals()

    car_name = data["name"]
    rpm      = data["rpm"]
    temp_c   = data["temp_c"]
    bat_level = data["bat_level"]

    print(f"--- {car_name} Vitals ---")
    print(f"Engine Speed: {rpm} RPM")

    if temp_c > 110:
        print(f"Coolant Temp: {temp_c}°C \nWARNING: COOLANT OVERHEATING")
        os.system('say"Warning: Coolant Temperature High"')
        logs.append("Coolant Overheat Detected")
        with open("vehicle_health_log.txt", "a") as f:
            f.write(f"{time.ctime()}: Coolant Hot - {temp_c}C\n")
    else:
        print(f"Coolant Temp: {temp_c}°C")

        print(f"Battery Voltage: {bat_level}v")

    if vehicle_type == "NISSAN":
        oil_target = NISSAN_OIL_TARGET
    if vehicle_type == "JETTA":
        oil_target = JETTA_OIL_TARGET
    else:
        oil_target = None

    if oil_target and data.get("odo"):
        miles_left = oil_target - data["odo"]

        if miles_left <=0:
            oil_status = "CHANGE OIL ASAP"
        else:
            oil_status = f"{int(miles_left)} miles until oil change"
    else:
        oil_status = "Odometer Data Unavailable"

    print(f"Service Info: {oil_status}")

    print("-" * 32)

    print(f"Total Events Logged: {len(logs)}")

    if not oil_announced and miles_left is not None:
        if miles_left < 500:
            os.system(f'say "Reminder: You have {int(miles_left)} miles remaining until your oil change is due" &')
        oil_announced = True

    time.sleep(1)
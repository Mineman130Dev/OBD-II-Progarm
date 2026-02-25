import time
import os
import obd
import random
from vehicles import nissan, vw

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

cvt_temp_sim = 20
temp_c_sim = 25

def detect_vehicle(connection):
    if not connection.is_connected():
        return "SIMULATOR"
    
    try:
        vin_response = connection.query(obd.commands.VIN)
        vin = str(vin_response.value)
        print(f"DETECTED VIN: {vin}")

        if "JN8" in vin:
            return "NISSAN"
        elif "3VW" in vin or "WVW" in vin:
            return "JETTA"
        else:
            return "UNKNOWN"
    except:
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

        elif vehicle_type == "JETTA":
            data = vw.get_vitals(connection)

        else:
            data = {"name": "Unknown", "rpm": 0, "temp_c": 0, "cvt_temp": 0}
        
        car_name = data["name"]
        rpm      = data["rpm"]
        temp_c   = data["temp_c"]
        cvt_temp = data["cvt_temp"]

    else:
        car_name = "Simulator Vehicle"
        rpm = random.randint(800, 3000)
        temp_c = 90
        cvt_temp_sim += 1
        cvt_temp = cvt_temp_sim

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

    if cvt_temp > 100:
        print(f"CVT Temp: {cvt_temp}°C \nWARNING: CVT FUILD OVERHEATING")
        logs.append("CVT Fuild Overheat Detected")
        with open("vehicle_health_log.txt", "a") as f:
            f.write(f"{time.ctime()}: CVT Hot - {cvt_temp}C\n")
    else:
        print(f"CVT Temp: {cvt_temp}°C")

    print("-" * 32)

    if cvt_temp > 100:
        if current_time - last_voice_alert > 5:
            os.system('say "Warning: Transmission Overheating"&')
            last_voice_alert = current_time

    if cvt_temp > 106:
        if current_time - last_voice_alert > 5:
            os.system('say "Emergency: Engine Overheating"&')
            last_voice_alert = current_time

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

    if not oil_announced and miles_left is not None:
        if miles_left < 500:
            os.system(f'say "Reminder: You have {int(miles_left)} miles remaining until your oil change is due" &')
        oil_announced = True

    print(f"Total Events Logged: {len(logs)}")
    time.sleep(1)
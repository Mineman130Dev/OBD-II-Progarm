import time
import os
import obd
import random

connection = obd.OBD()
cvt_overheat_logged = False
logs = []

last_voice_alert = 0

if connection.is_connected():
    mode = "REAL"
else:
    mode = "SIMULATOR"
    print('No adapter found. Starting in SIMULATOR MODE')
    time.sleep(2)

cvt_temp_sim = 20
temp_c_sim = 25

while True:
    os.system('cls' if os.name == 'nt' else 'clear')

    if mode == "REAL":
        r_rpm = connection.query(obd.commands.RPM)
        r_temp_c = connection.query(obd.commands.COOLANT_TEMP)
        r_cvt = connection.query(obd.commands['0121'])

        rpm = r_rpm.value.magnitude if not r_rpm.is_null() else 0
        temp_c = r_temp_c.value.magnitude if not r_temp_c.is_null() else 0
        cvt_temp = r_cvt.value.magnitude if not r_cvt.is_null() else 0
    else:
        rpm = random.randint(800, 3000)
        temp_c = 90
        cvt_temp_sim += 1
        cvt_temp = cvt_temp_sim

    print(f"--- 2014 NISSAN ROGUE VITALS ---")
    print(f"Engine Speed: {rpm} RPM")

    if temp_c > 110:
        print(f"Coolant Temp: {temp_c}°C \nWARNING: COOLANT OVERHEATING")
        os.system('say"Warning: Coolant Temperature High"')
        logs.append("Coolant Overheat Detected")
        with open("nissan_health_log.txt", "a") as f:
            f.write(f"{time.ctime()}: Coolant Hot - {temp_c}C\n")
    else:
        print(f"Coolant Temp: {temp_c}°C")

    if cvt_temp > 100:
        print(f"CVT Temp: {cvt_temp}°C \nWARNING: CVT FUILD OVERHEATING")
        current_time = time.time()        
        logs.append("CVT Fuild Overheat Detected")
        with open("nissan_health_log.txt", "a") as f:
            f.write(f"{time.ctime()}: CVT Hot - {cvt_temp}C\n")
    else:
        print(f"CVT Temp: {cvt_temp}°C")

    print("-" * 30)

    if cvt_temp > 100:
        if current_time - last_voice_alert > 5:
            os.system('say "Warning: Transmission Overheating"&')
            last_voice_alert = current_time

    if cvt_temp > 106:
        if current_time - last_voice_alert > 5:
            os.system('say "Emergency: Engine Overheating"&')
            last_voice_alert = current_time

    print(f"Total Events Logged: {len(logs)}")
    time.sleep(1)
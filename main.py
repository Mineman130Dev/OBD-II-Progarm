import time
import os
import obd

connection = obd.OBD()
cvt_overheat_logged = False
logs = []

while True:
    os.system('cls' if os.name == 'nt' else 'clear')

    if not connection.is_connected():
        print("Error: Could not find the OBD-II adapter.")
        print("Check your connection settings and make sure the car is ON.")
        exit()

    r_rpm = connection.query(obd.commands.RPM)
    r_temp_c = connection.query(obd.commands.COOLANT_TEMP)
    r_cvt = connection.query(obd.commands['0121'])

    rpm = r_rpm.value.magnitude if not r_rpm.is_null() else 0
    temp_c = r_temp_c.value.magnitude if not r_temp_c.is_null() else 0
    cvt_temp = r_cvt.value.magnitude if not r_cvt.is_null() else 0

    temp_c = r_temp_c.value.to("celsius").magnitude if not r_temp_c.is_null() else 0

    print(f"--- 2014 NISSAN ROGUE VITALS ---")
    print(f"Engine Speed: {rpm} RPM")

    if temp_c > 110:
        print(f"Coolant Temp: {temp_c}°C \nWARNING: COOLANT OVERHEATING")
        logs.append("Coolant Overheat Detected")
    else:
        print(f"Coolant Temp: {temp_c}°C")

    if cvt_temp > 100:
        print(f"CVT Temp: {cvt_temp}°C \nWARNING: CVT FUILD OVERHEATING")
        logs.append("CVT Fuild Overheat Detected")
        with open("nissan_health_log.txt", "a") as f:
            f.write(f"{time.ctime()}: CVT Hot - {cvt_temp}C\n")
    else:
        print(f"CVT Temp: {cvt_temp}°C")

    print("-" * 30)

    print(f"Total Events Logged: {len(logs)}")
    time.sleep(0.5)
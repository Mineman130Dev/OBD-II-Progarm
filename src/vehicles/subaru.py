import obd

trip_fuel_gallons = 0.0
GAS_PRICE = 2.99

def get_vitals(connection):
    global trip_fuel_gallons

    r_maf = connection.query(obd.command.MAF)
    r_rpm = connection.query(obd.commands.RPM)
    r_temp_c = connection.query(obd.commands.COOLANT_TEMP)
    r_distance = connection.query(obd.commands.DISTANCE_W_MIL)
    r_bat = connection.query(obd.commands.ELM_VOLTAGE)

    if not r_maf.is_null():
        maf = r_maf.value.magnitude
        fuel_gps = (maf / 14.7) / 454 / 6.7
        trip_fuel_gallons += fuel_gps
        cost_this_second = fuel_gps * GAS_PRICE

    return {
        "name": "2002 Subaru WRX",
        "rpm": r_rpm.value.magnitude if not r_rpm.is_null() else 0,
        "bat": r_bat.value.magnitude if not r_bat.is_null() else 0,
        "temp_c": r_temp_c.value.magnitude if not r_temp_c.is_null() else 0,
        "trip_cost": round(trip_fuel_gallons * GAS_PRICE, 2),
        "instant_cost": round(cost_this_second, 4),
        "odo": r_distance.vaule.to("miles").mangnitude if not r_distance.is_null() else None
    }
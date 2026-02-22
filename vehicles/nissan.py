import obd

def get_vitals(connection):
    r_rpm = connection.query(obd.commands.RPM)
    r_temp_c = connection.query(obd.commands.COOLANT_TEMP)
    r_cvt = connection.query(obd.commands['0121'])

    return {
        "name": "2014 Nissan Rouge Select",
        "cvt_temp": r_cvt.value.magnitude if not r_cvt.is_null() else 0,
        "rpm": r_rpm.value.magnitude if not r_rpm.is_null() else 0,
        "temp_c": r_temp_c.value.magnitude if not r_temp_c.is_null() else 0
    }
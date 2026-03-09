import random

sim_state = {
    "temp_c": 90,
    "bat_level": 14.2,
    "oil_temp": 130,
    "obo": 99281,
    "trip_fuel": 0.0
}

def get_vitals():
    sim_state["temp_c"] += random.uniform(-0.5, 0.5)
    sim_state["oil_temp"] += random.uniform(-1, 1)
    sim_state["obo"] += 0.01

    maf_fake = random.uniform(5.0, 20.0)
    fuel_gps = (maf_fake / 14.7) / 454 / 6.7
    sim_state["trip_fuel"] += fuel_gps
    
    gas_price = 3.39

    return {
        "name": "Simulator Vehicle",
        "rpm": random.randint(800, 3000),
        "temp_c": round(sim_state["temp_c"], 1),
        "bat_level": sim_state["bat_level"],
        "trip_cost": round(sim_state["trip_fuel"] * gas_price, 2),
        "instant_cost": round(fuel_gps * gas_price, 4),
        "odo": round(sim_state["obo"], 1),
        "mileage": round(sim_state["obo"], 1),
    }
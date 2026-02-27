import random

sim_state = {
    "temp_c": 90,
    "bat_level": 14.2,
    "oil_temp": 130
}

def get_vitals():
    sim_state["temp_c"] += random.uniform(-0.5, 0.5)
    sim_state["oil_temp"] += random.uniform(-1, 1)

    return {
        "name": "Simulator Vehicle",
        "rpm": random.randint(800, 3000),
        "temp_c": round(sim_state["temp_c"], 1),
        "bat_level": sim_state["bat_level"],
        "odo": 74850,
    }
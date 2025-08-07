import json
import time
import datetime
import math
from kinesis_helper import KinesisStream

# Panel peak power in Watts
PEAK_POWER_W = 400
# Interval in seconds between each data transmission
INTERVAL_SECONDS = 10


def simulate_panel_real_time(dt_object):
    """
    Simulates the panel state based on real time.
    """
    # 1. Get current time in decimal format (e.g. 13.5 for 1:30 PM)
    real_time = dt_object.hour + dt_object.minute / 60.0

    # 2. Simulate solar irradiance with a sinusoidal curve (max at noon)
    # The curve is positive between 6 AM and 6 PM (can be adjusted)
    # Note: this is a simplification; an advanced simulation would use actual sunrise/sunset times.
    sun_factor = math.sin((real_time - 6) / 12 * math.pi) if 6 < real_time < 21 else 0
    irradiance_w_m2 = max(0, sun_factor * 1000)  # Max 1000 W/m² at solar noon

    # 3. Simulate panel temperature
    ambient_temp = 15  # Base temperature
    panel_temp_c = ambient_temp + (irradiance_w_m2 * 0.045)

    # 4. Calculate instantaneous power in Watts
    if irradiance_w_m2 > 0:
        # Efficiency loss due to heat (approximately -0.35% per °C above 25°C)
        temp_loss = max(0, (panel_temp_c - 25) * 0.0035)

        # Theoretical power based on irradiance
        theoretical_power_w = PEAK_POWER_W * (irradiance_w_m2 / 1000)

        # Actual power after losses
        current_power_w = theoretical_power_w * (1 - temp_loss)
    else:
        current_power_w = 0

    # 5. Calculate energy produced DURING the interval in Watt-hours (Wh)
    incremental_production_wh = current_power_w * (INTERVAL_SECONDS / 3600.0)

    # Create data dictionary
    data = {
        "irradiance_w_m2": round(irradiance_w_m2, 2),
        "panel_temperature_c": round(panel_temp_c, 2),
        "current_power_w": round(current_power_w, 2),
        "incremental_production_wh": round(incremental_production_wh, 4),
        "timestamp_utc": dt_object.astimezone(datetime.timezone.utc).isoformat(),
    }

    return data


if __name__ == "__main__":
    print(f"--- Starting real-time simulator (Panel {PEAK_POWER_W}Wp) ---")
    print(f"A ndJSON message will be generated every {INTERVAL_SECONDS} seconds.")
    print("Press CTRL+C to stop.")
    print("--------------------------------------------------------------------")
    stream = KinesisStream("terraform-kinesis-solar")
    try:
        while True:
            now = datetime.datetime.now()
            current_data = simulate_panel_real_time(now)
            print(json.dumps(current_data))
            stream.send_stream(data=current_data)
            time.sleep(INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\n--- Simulation stopped by user. ---")

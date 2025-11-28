import time
import board
import busio
import adafruit_ltr390
import bme680

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# --- LTR390 (UV + light) ---
ltr = adafruit_ltr390.LTR390(i2c)
ltr.mode = adafruit_ltr390.MODE_UVS  # start in UV mode

# --- BME688 (environment) ---
sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

def read_sensors():
    """Return one reading from both sensors as a dict."""
    # BME688
    sensor.get_sensor_data()
    temp_c = sensor.data.temperature
    hum_rh = sensor.data.humidity
    press_hpa = sensor.data.pressure
    gas_res_ohm = sensor.data.gas_resistance

    # LTR390
    uvi = ltr.uvi
    lux = ltr.lux

    return {
        "temp_c": temp_c,
        "hum_rh": hum_rh,
        "press_hpa": press_hpa,
        "gas_res_ohm": gas_res_ohm,
        "uv_index": uvi,
        "lux": lux,
    }

if __name__ == "__main__":
    while True:
        print(read_sensors())
        time.sleep(2)

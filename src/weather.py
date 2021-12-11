import time
from bme280 import BME280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus


bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

#THROW AWAY RESULT
temperature = bme280.get_temperature()
humidity = bme280.get_humidity()
time.sleep(0.1)

temperature = bme280.get_temperature()
humidity = bme280.get_humidity()

print(float(temperature), float(humidity))
from datetime import datetime
from RPi import GPIO

# Work in progress
# Seedling stage, ambient temp ~ 24.5C
# 77, 79, 83
#After a few days I changed to
# 74, 76, 80

# check if humidifier is running or not
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
humidifier_state = GPIO.input(16)

self.logger.debug("Ensuring climate is in check")

self.loop_count += 1  # Counts how many times the run code has been executed

# early_veg = True
# late_veg_early_flower = False
# mid_late_flower = False

seedling_humidity_target_range = range(70,75)
# seedling_temperature_target_range = range(24,28)

# range and float don't work, so target values * 1000
# early_veg_vpd_target_range = range(400,800)
# late_veg_early_flower_vpd_target_range = range(800,1200)
# mid_late_flower_vpd_target_range = range(1200,1600)

humidity = None
temperature = None
vpd = None

# Handle humidity measurement
try:
    humidity = round(self.condition("83498920"),2)
    self.run_action("94a73d30", value={"topic": "mycodo/measurements/humidity/ambient", "payload": humidity})
except TypeError:
    self.message += "Could not get a reading for humidity!\n"
    self.logger.error("Could not get a reading for humidity!")

# Handle temperature measurement
try:
    temperature = round(self.condition("0040d310"),2)
    self.run_action("94a73d30", value={"topic": "mycodo/measurements/climate/temperature_garden", "payload": temperature})
except TypeError:
    self.message += "Could not get a reading for temperature!\n"
    self.logger.error("Could not get a reading for temperature!")

# Handle VPD measurement
try:
    vpd = round(self.condition("5f792188"),2)
except TypeError:
    self.message += "Could not get a reading for VPD!\n"
    self.logger.error("Could not get a reading for VPD!")

if vpd is not None:
    self.logger.debug(f"VPD is {vpd}")
    self.run_action("94a73d30", value={"topic": "mycodo/measurements/climate/vpd", "payload": vpd})
else:
    self.message += "Could not get a reading for VPD!\n"
    self.logger.error("Could not get a reading for VPD!")

# for now go by humidity instead of VPD
if humidity is not None:
    self.logger.debug(f"Humidity is {humidity}")
    self.run_action("94a73d30", value={"topic": "mycodo/measurements/humidity/ambient", "payload": humidity})
    if humidity not in seedling_humidity_target_range:
        if humidity > 80:
            self.message += "Humidity is way too high!\n"
            self.logger.debug("Humidity is way too high!")
        if humidity > 76 and humidifier_state == 1:
            self.message += f"Humidity is too High! Humidity is {humidity}\n"
            self.logger.debug(f"Humidity is too High! Humidity is {humidity}. Deactivating humidifier.")
            self.run_action("d0792870")
        elif humidity < 74 and humidifier_state == 0:
            self.message += f"Humidity is too Low! Humidity is {humidity}\n"
            self.logger.debug(f"Humidity is too Low! Humidity is {humidity}. Activating humidifier.")
            self.run_action("20d5d009")
else:
    self.message += "Could not get a reading for humidity!\n"
    self.logger.error("Could not get a reading for humidity!")

if temperature is not None:
    self.logger.debug(f"Temperature is {temperature}")
    self.run_action("94a73d30", value={"topic": "mycodo/measurements/climate/temperature_garden", "payload": temperature})
else:
    self.message += "Could not get a reading for temperature!\n"
    self.logger.error("Could not get a reading for temperature!")
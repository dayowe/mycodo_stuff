from datetime import datetime
import RPi.GPIO as GPIO

# Work in progress

# check if humidifier is running or not
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
humidifier_state = GPIO.input(16)

self.logger.debug("Ensuring climate is in check")

self.loop_count += 1  # Counts how many times the run code has been executed

early_veg = True
late_veg_early_flower = False
mid_late_flower = False

seedling_humidity_target_range = range(70,75)
seedling_temperature_target_range = range(24,28)

# range and float don't work, so target values * 1000
early_veg_vpd_target_range = range(400,800)
late_veg_early_flower_vpd_target_range = range(800,1200)
mid_late_flower_vpd_target_range = range(1200,1600)

if vpd is not None:
    vpd = round(self.condition("5f792188"),2)
    self.logger.debug(f"VPD is {vpd}")
    self.run_action("94a73d30", value={"topic": "mycodo/measurements/climate/vpd", "payload": vpd})
else:
    self.message += "Could not get a reading for VPD!\n"
    self.logger.error("Could not get a reading for VPD!")

# for now go by humidity instead of VPD
if humidity is not None:
    humidity = round(self.condition("83498920"),2)
    self.logger.debug(f"Humidity is {humidity}")
    self.run_action("94a73d30", value={"topic": "mycodo/measurements/humidity/ambient", "payload": humidity})
    if humidity not in seedling_humidity_target_range:
        if humidity > 83:
            self.message += "Humidity is way too high!\n"
            self.logger.debug("Humidity is way too high!")
        if humidity > 78 and humidifier_state == 1:
            self.message += f"Humidity is too High! Humidity is {humidity}\n"
            self.logger.debug(f"Humidity is too High! Humidity is {humidity}. Deactivating humidifier.")
            self.run_action("d0792870")
        elif humidity < 70 and humidifier_state == 0:
            self.message += f"Humidity is too Low! Humidity is {humidity}\n"
            self.logger.debug(f"Humidity is too Low! Humidity is {humidity}. Activating humidifier.")
            self.run_action("20d5d009")
else:
    self.message += "Could not get a reading for humidity!\n"
    self.logger.error("Could not get a reading for humidity!")

if temperature is not None:
        temperature = round(self.condition("0040d310"),2)
        self.logger.debug(f"Temperature is {temperature}")
        self.run_action("94a73d30", value={"topic": "mycodo/measurements/climate/temperature_garden", "payload": temperature})
else:
    self.message += "Could not get a reading for temperature!\n"
    self.logger.error("Could not get a reading for temperature!")
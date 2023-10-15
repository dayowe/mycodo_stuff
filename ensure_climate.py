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
seedling_temperature_target_range = range(70,75)
#early_veg_vpd_target_range = range(0.4,0.8)
#late_veg_early_flower_vpd_target_range = range(0.8,1.2)
#mid_late_flower_vpd_target_range = range(1.2,1.6)

humidity = self.condition("83498920")
temperature = self.condition("0040d310")
vpd = self.condition("5f792188")
self.logger.debug(f"Humidity is {humidity}")
self.logger.debug(f"Temperature is {temperature}")
self.logger.debug(f"VPD is {vpd}")

# for now go by humidity instead of VPD
if humidity is not None:
    self.run_action("94a73d30", value={"topic": "mycodo/measurements/humidity/ambient", "payload": humidity})
    if humidity not in seedling_humidity_target_range:
        if humidity > 80:
            self.message += f"Humidity is way too high!\n"
            self.logger.debug(f"Humidity is way too high!")
        if humidity > 75 and humidifier_state == 1:
            self.message += f"Humidity is too High! Humidity is {humidity}\n"
            self.logger.debug(f"Humidity is too High! Humidity is {humidity}. Deactivating humidifier.")
            self.run_action("d0792870")
        elif humidity < 70 and humidifier_state == 0:
            self.message += f"Humidity is too Low! Humidity is {humidity}\n"
            self.logger.debug(f"Humidity is too Low! Humidity is {humidity}. Activating humidifier.")
            self.run_action("20d5d009")

if temperature is not None:
        self.run_action("94a73d30", value={"topic": "mycodo/measurements/temperature/ambient", "payload": temperature})
from datetime import datetime, time

day_start = time(6,00)
day_end = time(23,59)

far_red_morning_start = time(6,00)
far_red_morning_end = time(6,15)
far_red_evening_start = time(23,45)
far_red_evening_end = time(23,59)

flower_phase = False

def should_lights_be_on(begin_time, end_time):
    check_time = datetime.now().time()
    if begin_time < end_time:
        return begin_time <= check_time <= end_time
    # crosses midnight
    return begin_time <= check_time or check_time <= end_time

self.logger.debug("Ensuring the Lights are on schedule!")

veg_led_state = self.condition("efdd495c")
bloom_led_state = self.condition("ee7e791b")
far_red_led_state = self.condition("11cfe4d1")

# If returns True it's daytime
if should_lights_be_on(day_start, day_end) is True:
    if veg_led_state == "off":
        self.message += ("Oh, oh. It's day time, but the VEG channel is off!\nActivating VEG channel.")
        self.logger.debug("Oh, oh. It's day time, but the VEG channel is off!")
        self.logger.debug("Activating VEG channel.")
        self.run_action("d64908a0")
    elif veg_led_state == "on":
        self.message += ("It's day time and the VEG channel is ON, as it should be.\n")
        self.logger.debug("It's day time and the VEG channel is ON, as it should be.")
    else:
        self.message += ("It's night-time and the VEG channel is OFF, as it should be.\n")
        self.logger.debug("It's night-time and the VEG channel is OFF, as it should be.")
    if bloom_led_state == "off":
        if flower_phase is True:
            self.message += ("Oh, oh. It's daytime and we're in flower, but the BLOOM channel is off!\nActivating BLOOM channel.")
            self.logger.debug("Oh, oh. It's daytime and we're in flower, but the BLOOM channel is off!")
            self.logger.debug("Activating BLOOM channel.")
            self.run_action("f488af4f")
        else:
            self.message += ("We're not in flower and the BLOOM channel is OFF, as it should be.\n")
            self.logger.debug("We're not in flower and the BLOOM channel is OFF, as it should be.")
    elif bloom_led_state == "on":
        if flower_phase is False:
            self.message += ("Oh, oh. We're not in flower. but the BLOOM channel is on!\nDeactivating BLOOM channel.")
            self.logger.debug("Oh, oh. It's daytime and we're in flower, but the BLOOM channel is off!")
        else:
            self.message += ("It's day time, we're in flower and the BLOOM channel is ON, as it should be.\n")
            self.logger.debug("It's day time, we're in flower and the BLOOM channel is ON, as it should be.")
    else:
        self.message += ("It's night-time and the BLOOM channel is OFF, as it should be.\n")
        self.logger.debug("It's night-time and the BLOOM channel is OFF, as it should be.")
    if far_red_led_state == "off" and should_lights_be_on(far_red_morning_start, far_red_morning_end) is True:
        self.message += ("Oh, oh. It's sunrise, but the FAR RED channel is off!\nActivating FAR RED channel.")
        self.logger.debug("Oh, oh. It's sunrise, but the FAR RED channel is off!")
        self.logger.debug("Activating FAR RED channel.")
        self.run_action("3bd75ea9")
    elif far_red_led_state == "off" and should_lights_be_on(far_red_evening_start, far_red_evening_end) is True:
        self.message += ("Oh, oh. It's sunset, but the FAR RED channel is off!\nActivating FAR RED channel")
        self.logger.debug("Oh, oh. It's sunset, but the FAR RED channel is off!")
        self.logger.debug("Activating FAR RED channel.")
        self.run_action("3bd75ea9")
    else:
        self.message += ("It's neither sunrise nor sunset and the FAR RED channel is OFF, as it should be.\n")
        self.logger.debug("It's neither sunrise nor sunset and the FAR RED channel is OFF, as it should be.")

elif should_lights_be_on(day_start, day_end) is False:
    if veg_led_state == "on" or bloom_led_state == "on" or far_red_led_state == "on":
        if flower_phase is True:
            self.message += ("\nFuck, fuck, fuck! Dark phase interruption during flower!\n")
            self.logger.debug("Fuck, fuck, fuck! Dark phase interruption during flower!")
        if veg_led_state == "on":
            self.message += ("VEG channel is ON, but should be OFF!\nDeactivating VEG channel.")
            self.logger.debug("VEG channel is ON, but should be OFF!")
            self.logger.debug("Deactivating VEG channel.")
            self.run_action("6da6923a")
        if bloom_led_state == "on":
            self.message += ("BLOOM channel is ON, but should be OFF!\nDeactivating BLOOM channel.")
            self.logger.debug("BLOOM channel is ON, but should be OFF!")
            self.logger.debug("Deactivating BLOOM channel.")
            self.run_action("74266e46")
        if far_red_led_state == "on":
            self.message += ("FAR RED channel is ON, but should be OFF!\nDeactivating FAR RED channel.")
            self.logger.debug("FAR RED channel is ON, but should be OFF!")
            self.logger.debug("Deactivating FAR RED channel.")
            self.run_action("ca0a7279")

else:
    self.message += "It's night-time and the lights are off, as they should be. Sleepy tighty."
    self.logger.info("It's night-time and the lights are off, as they should be. Sleepy tighty.")
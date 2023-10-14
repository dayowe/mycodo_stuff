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
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

self.message += ("Ensuring the Lights are on schedule!\n\n")
self.logger.debug("Ensuring the Lights are on schedule!")

veg_led_state = self.condition("bf39dfcd")
bloom_led_state = self.condition("ee7e791b")
far_red_led_state = self.condition("11cfe4d1")

# If returns True it's daytime
if should_lights_be_on(day_start, day_end) is True:
    if veg_led_state == "off":
        self.message += ("Oh, oh. It's daytime, but the VEG channel is off!\n")
        self.logger.debug("Oh, oh. It's daytime, but the VEG channel is off!")
        self.run_action("d64908a0")
    else:
        self.message += ("The VEG channel is behaving as expected.\n")
        self.logger.debug("The VEG channel is behaving as expected.")
    if bloom_led_state == "off" and flower_phase is True:
        self.message += ("Oh, oh. It's daytime, but the BLOOM channel is off!\n")
        self.logger.debug("Oh, oh. It's daytime, but the BLOOM channel is off!")
        self.run_action("f488af4f")
    else:
        self.message += ("The BLOOM channel is behaving as expected.\n")
        self.logger.debug("The BLOOM channel is behaving as expected.")
    if far_red_led_state == "off" and should_lights_be_on(far_red_morning_start, far_red_morning_end) is True:
        self.message += ("Oh, oh. It's sunrise, but the FAR RED channel is off!\n")
        self.logger.debug("Oh, oh. It's sunrise, but the FAR RED channel is off!")
        self.run_action("3bd75ea9")
    elif far_red_led_state == "off" and should_lights_be_on(far_red_evening_start, far_red_evening_end) is True:
        self.message += ("Oh, oh. It's sunset, but the FAR RED channel is off!\n")
        self.logger.debug("Oh, oh. It's sunset, but the FAR RED channel is off!")
        self.run_action("3bd75ea9")
    else:
        self.message += ("The FAR RED channel is behaving as expected.\n")
        self.logger.debug("The FAR RED channel is behaving as expected.")

elif should_lights_be_on(day_start, day_end) is True:
    self.message += "It's night-time and the lights are off, as they should be.\n"
    self.logger.info("It's night-time and the lights are off, as they should be.")
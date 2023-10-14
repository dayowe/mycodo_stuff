from datetime import datetime

self.logger.debug("Ensuring Chiller pump is on.")

self.loop_count += 1  # Counts how many times the run code has been executed

chiller_pump_state = self.condition("081e57dd")
self.logger.debug(f"Chiller Pump is {chiller_pump_state}")

if chiller_pump_state == "on":
    self.logger.debug(f"The Chiller Pump is {chiller_pump_state}, as it should be.")
    self.message += f"The Chiller Pump is {chiller_pump_state}, as it should be.\n"

elif chiller_pump_state == "off":
    self.logger.info(f"The Chiller Pump is {chiller_pump_state}, but should be on. Activating pump.")
    self.message += f"Chiller Pump is {chiller_pump_state}, but should be on.\nActivating pump."
    self.run_action("867d958c")
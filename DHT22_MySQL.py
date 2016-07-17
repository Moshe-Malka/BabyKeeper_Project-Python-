#!/usr/bin/env python

# 2014-07-11 DHT22.py

import time
import atexit

import pigpio

class sensor:
      
   def __init__(self, pi, gpio, LED=None, power=None):
    
      self.pi = pi
      self.gpio = 4
      self.LED = LED
      self.power = power

      if power is not None:
         pi.write(power, 1) # Switch sensor on.
         time.sleep(1)

      self.powered = True

      self.cb = None

      atexit.register(self.cancel)

      self.bad_CS = 0 # Bad checksum count.
      self.bad_SM = 0 # Short message count.
      self.bad_MM = 0 # Missing message count.
      self.bad_SR = 0 # Sensor reset count.

      # Power cycle if timeout > MAX_TIMEOUTS.
      self.no_response = 0
      self.MAX_NO_RESPONSE = 2

      self.rhum = -999
      self.temp = -999

      self.tov = None

      self.high_tick = 0
      self.bit = 40

      pi.set_pull_up_down(gpio, pigpio.PUD_OFF)

      pi.set_watchdog(gpio, 0) # Kill any watchdogs.

      self.cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cb)

   def _cb(self, gpio, level, tick):
      """
      Accumulate the 40 data bits.  Format into 5 bytes, humidity high,
      humidity low, temperature high, temperature low, checksum.
      """
      diff = pigpio.tickDiff(self.high_tick, tick)

      if level == 0:

         # Edge length determines if bit is 1 or 0.

         if diff >= 50:
            val = 1
            if diff >= 200: # Bad bit?
               self.CS = 256 # Force bad checksum.
         else:
            val = 0

         if self.bit >= 40: # Message complete.
            self.bit = 40

         elif self.bit >= 32: # In checksum byte.
            self.CS  = (self.CS<<1)  + val

            if self.bit == 39:

               # 40th bit received.

               self.pi.set_watchdog(self.gpio, 0)

               self.no_response = 0

               total = self.hH + self.hL + self.tH + self.tL

               if (total & 255) == self.CS: # Is checksum ok?

                  self.rhum = ((self.hH<<8) + self.hL) * 0.1

                  if self.tH & 128: # Negative temperature.
                     mult = -0.1
                     self.tH = self.tH & 127
                  else:
                     mult = 0.1

                  self.temp = ((self.tH<<8) + self.tL) * mult

                  self.tov = time.time()

                  if self.LED is not None:
                     self.pi.write(self.LED, 0)

               else:

                  self.bad_CS += 1

         elif self.bit >=24: # in temp low byte
            self.tL = (self.tL<<1) + val

         elif self.bit >=16: # in temp high byte
            self.tH = (self.tH<<1) + val

         elif self.bit >= 8: # in humidity low byte
            self.hL = (self.hL<<1) + val

         elif self.bit >= 0: # in humidity high byte
            self.hH = (self.hH<<1) + val

         else:               # header bits
            pass

         self.bit += 1

      elif level == 1:
         self.high_tick = tick
         if diff > 250000:
            self.bit = -2
            self.hH = 0
            self.hL = 0
            self.tH = 0
            self.tL = 0
            self.CS = 0

      else: # level == pigpio.TIMEOUT:
         self.pi.set_watchdog(self.gpio, 0)
         if self.bit < 8:       # Too few data bits received.
            self.bad_MM += 1    # Bump missing message count.
            self.no_response += 1
            if self.no_response > self.MAX_NO_RESPONSE:
               self.no_response = 0
               self.bad_SR += 1 # Bump sensor reset count.
               if self.power is not None:
                  self.powered = False
                  self.pi.write(self.power, 0)
                  time.sleep(2)
                  self.pi.write(self.power, 1)
                  time.sleep(2)
                  self.powered = True
         elif self.bit < 39:    # Short message receieved.
            self.bad_SM += 1    # Bump short message count.
            self.no_response = 0

         else:                  # Full message received.
            self.no_response = 0

   def temperature(self):
      """Return current temperature."""
      return self.temp

   def humidity(self):
      """Return current relative humidity."""
      return self.rhum

   def staleness(self):
      """Return time since measurement made."""
      if self.tov is not None:
         return time.time() - self.tov
      else:
         return -999

   def bad_checksum(self):
      """Return count of messages received with bad checksums."""
      return self.bad_CS

   def short_message(self):
      """Return count of short messages."""
      return self.bad_SM

   def missing_message(self):
      """Return count of missing messages."""
      return self.bad_MM

   def sensor_resets(self):
      """Return count of power cycles because of sensor hangs."""
      return self.bad_SR

   def trigger(self):
      """Trigger a new relative humidity and temperature reading."""
      if self.powered:
         if self.LED is not None:
            self.pi.write(self.LED, 1)

         self.pi.write(self.gpio, pigpio.LOW)
         time.sleep(0.017) # 17 ms
         self.pi.set_mode(self.gpio, pigpio.INPUT)
         self.pi.set_watchdog(self.gpio, 200)

   def cancel(self):
      """Cancel the DHT22 sensor."""

      self.pi.set_watchdog(self.gpio, 0)

      if self.cb != None:
         self.cb.cancel()
         self.cb = None

if __name__ == "__main__":

   import time
   import mysql.connector
   import pigpio
   import DHT22
   from raspberry_pi_unique_product_key import getRaspberryPiID

   def insert_data(table,value):
    my_time = time.strftime('%Y-%m-%d %H:%M:%S')
    rpi_id = getRaspberryPiID()
    conn = mysql.connector.connect(
        host=MYSQL_HOST, # Enter your Mysql Server ip
        user=MYSQL_USERNAME, # Enter your mysql username
        password=MYSQL_PASSWORD, # Enter your mysql password
        database=MYSQL_DB)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO %s VALUES( '%s','%d','%s')"""
                   % (table,my_time,value,rpi_id))
    conn.commit()
    cursor.close()
    conn.close()

   MYSQL_HOST = 'sql7.freesqldatabase.com'
   MYSQL_USERNAME = 'sql7118146'
   MYSQL_PASSWORD = 'rmWVntI87f'
   MYSQL_DB = 'sql7118146'
      
   # Intervals of about 2 seconds or less will eventually hang the DHT22.
   INTERVAL=3

   pi = pigpio.pi()

   s = DHT22.sensor(pi, 4)

   currTemperature = 0
   currHumidity = 0
   while True:
      s.trigger()
      time.sleep(0.2)
      
      if abs(s.temperature()) != currTemperature:
         insert_data('temperature_reading',abs(s.temperature()))
         currTemperature = abs(s.temperature())

      time.sleep(0.2)

      if abs(s.humidity()) != currHumidity:
         insert_data('humidity_reading',abs(s.humidity()))
         currHumidity = abs(s.humidity())



      time.sleep(1) # Overall INTERVAL second polling.

   s.cancel()

   pi.stop()


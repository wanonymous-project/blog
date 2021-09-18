#!/usr/bin/env python

import RPi.GPIO as GPIO
import requests
import time

# GAS hook URL
url_1 = 'https://script.google.com/macros/s/AKfycbynSlN9Ms5vSLea_NlNQBZSgNQAraJ2v_U_Q3qJ84Uj3oAePQbdgJ4On_xxJKG0kPsc/exec'+'?sensing=' + "1"
url_0 = 'https://script.google.com/macros/s/AKfycbynSlN9Ms5vSLea_NlNQBZSgNQAraJ2v_U_Q3qJ84Uj3oAePQbdgJ4On_xxJKG0kPsc/exec'+'?sensing=' + "0"

### setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN) # GPIO 18 : human detect sensor

# initialize
if GPIO.input(18):
  requests.get(url_1)
else:
  requests.get(url_0)

while True:
  GPIO.wait_for_edge(18, GPIO.BOTH)
  if GPIO.input(18):
    requests.get(url_1)
  else:
    requests.get(url_0)

    time.sleep(1)

GPIO.cleanup()


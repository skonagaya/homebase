try:
  with open("/sys/class/gpio/gpio4/value") as pin:
    status = pin.read(1)
except:
  print "Remember to export the pin first!"
  status = "Unknown"

print status

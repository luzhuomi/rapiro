import sys
import time
import serial
import colorsys

# config
SENSOR_PIN = 6
RAPIRO_TTY = '/dev/ttyAMA0'
rapiro = serial.Serial(RAPIRO_TTY, 57600, timeout = 10)
value = 0

# version check
rapiro.write("#V")
time.sleep(0.05)
version = ""
while rapiro.inWaiting():
    version += rapiro.read(1)
version = version.split("#Ver")[1]

if(version != "00"):
    print "ERROR: Firmware of Rapiro is different."
    sys.exit(1)

# main loop
while True:
    rapiro.flush() # cleaning
    rapiro.write("#A"+str(SENSOR_PIN)) # sensor request
    time.sleep(0.05)
    buf = ''
    while rapiro.inWaiting():
        buf += rapiro.read(1)
    value = int(buf.split("#A"+str(SENSOR_PIN)+"V")[1])
    rgb = colorsys.hsv_to_rgb(value%2048/2048.0, 1.0, 0.7)
    cmd = "#PR" + str(int(rgb[0]*255)).zfill(3) + "G" + str(int(rgb[1]*255)).zfill(3) + "B" + str(int(rgb[2]*255)).zfill(3) + "T001"
    print "Send: " + cmd
    rapiro.write(cmd)
    time.sleep(0.05)

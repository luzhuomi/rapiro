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

HEAD="00"
WAIST="01"
RIGHT_SHOULDER_Y="02"
RIGHT_SHOULDER_P="03"
RIGHT_HAND="04"
LEFT_SHOULDER_Y="05"
LEFT_SHOULDER_P="06"
LEFT_HAND="07"
RIGHT_FOOT_Y="08"
RIGHT_FOOT_P="09"
LEFT_FOOT_Y="10"
LEFT_FOOT_P="11"


def pickup():
	cmds = [
	"#PS02A180T001",
        "#PS03A090T001",
	"#PS04A090T001",
        "#PS05A000T001",
	"#PS06A090T001",
	"#PS07A115T001",
	]
	for cmd in cmds:
		rapiro.write(cmd)
		time.sleep(1)

	while True:
		rapiro.write("#PS03A110T002")
		rapiro.write("#PS06A070T002")
		time.sleep(1)
		rapiro.write("#PS03A090T002")
		rapiro.write("#PS06A090T002")
		time.sleep(1)
pickup()



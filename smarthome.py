import yeelight

def turn_on():
	bulb = yeelight.Bulb("192.168.1.210")
	bulb.turn_on()

def turn_off():
	bulb = yeelight.Bulb("192.168.1.210")
	bulb.turn_off()

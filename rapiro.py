
import sys
import time
import serial


def mkstr(n,digits):
	return (("0" * digits) + str(n))[-digits:]



def mkcmd(servo, angle, time):
	return ("#PS%sA%sT%s" % (mkstr(servo,2), mkstr(angle,3), mkstr(time,3)))

class Rapiro:

	# config
	SENSOR_PIN = 6
	RAPIRO_TTY = '/dev/ttyAMA0'
	rapiro = serial.Serial(RAPIRO_TTY, 57600, timeout = 10)

	HEAD=0
	WAIST=1
	RIGHT_SHOULDER_Y=2
	RIGHT_SHOULDER_P=3
	RIGHT_HAND=4
	LEFT_SHOULDER_Y=5
	LEFT_SHOULDER_P=6
	LEFT_HAND=7
	RIGHT_FOOT_Y=8
	RIGHT_FOOT_P=9
	LEFT_FOOT_Y=10
	LEFT_FOOT_P=11

	ANGLES = [90, 90,0,130, 90,180, 50, 90, 90, 90, 90, 90] 
	LEDS = [0,0,255]

	current_angles = []
	current_leds = []

	def __init__(self):
		# version check
		self.rapiro.write("#V")
		time.sleep(0.05)
		version = ""
		while self.rapiro.inWaiting():
		    version += self.rapiro.read(1)
		version = version.split("#Ver")[1]

		if(version != "00"):
		    print "ERROR: Firmware of Rapiro is different."
		    sys.exit(1)		

		self.current_angles = self.ANGLES
		self.current_leds = self.LEDS
		return


	def reset(self):
		#for i in range(0,12):
		#	self.rapiro.write(mkcmd(i,self.ANGLES[i],1))
		#	time.sleep(0.05)
		self.rapiro.write("#M00")
		self.current_angles = self.ANGLES
		self.current_leds = self.LEDS

	def head(self,angle,time):
		self.rapiro.write(mkcmd(self.HEAD,angle,time))
		self.current_angles[self.HEAD] = angle 

	def head_is_left_most(self):
		return self.current_angles[self.HEAD] >= 160

	def head_is_right_most(self):
		return self.current_angles[self.HEAD] <= 10

	def head_left(self):
		if self.head_is_left_most():
			pass
		else:
			self.rapiro.write(mkcmd(self.HEAD,self.current_angles[self.HEAD]+5,1))
			self.current_angles[self.HEAD] += 5 
		time.sleep(0.05)

	def head_right(self):
		if self.head_is_right_most():
			pass
		else:
			self.rapiro.write(mkcmd(self.HEAD,self.current_angles[self.HEAD]-5,1))
			self.current_angles[self.HEAD] -= 5 
		time.sleep(0.05)


	def waist(self,angle,time):
		self.rapiro.write(mkcmd(self.WAIST,angle,time))
		self.current_angles[self.WAIST] = angle 

	def waist_left(self):
		self.rapiro.write(mkcmd(self.WAIST,self.current_angles[self.WAIST]+5,1))
		self.current_angles[self.WAIST] += 5 
		time.sleep(0.05)

	def waist_right(self):
		self.rapiro.write(mkcmd(self.WAIST,self.current_angles[self.WAIST]-5,1))
		self.current_angles[self.WAIST] -= 5 
		time.sleep(0.05)


	def right_shoulder_y(self,angle,time):
		self.rapiro.write(mkcmd(self.RIGHT_SHOULDER_Y,angle,time))
		self.current_angles[self.RIGHT_SHOULDER_Y] = angle 

	def right_shoulder_y_left(self):
		self.rapiro.write(mkcmd(self.RIGHT_SHOULDER_Y,self.current_angles[self.RIGHT_SHOULDER_Y]+5,1))
		self.current_angles[self.RIGHT_SHOULDER_Y] += 5 
		time.sleep(0.05)

	def right_shoulder_y_right(self):
		self.rapiro.write(mkcmd(self.RIGHT_SHOULDER_Y,self.current_angles[self.RIGHT_SHOULDER_Y]-5,1))
		self.current_angles[self.RIGHT_SHOULDER_Y] -= 5 
		time.sleep(0.05)



	def right_shoulder_p(self,angle,time):
		self.rapiro.write(mkcmd(self.RIGHT_SHOULDER_P,angle,time))
		self.current_angles[self.RIGHT_SHOULDER_P] = angle 

	def right_shoulder_p_left(self):
		self.rapiro.write(mkcmd(self.RIGHT_SHOULDER_P,self.current_angles[self.RIGHT_SHOULDER_P]+5,1))
		self.current_angles[self.RIGHT_SHOULDER_P] += 5 
		time.sleep(0.05)

	def right_shoulder_p_right(self):
		self.rapiro.write(mkcmd(self.RIGHT_SHOULDER_P,self.current_angles[self.RIGHT_SHOULDER_P]-5,1))
		self.current_angles[self.RIGHT_SHOULDER_P] -= 5 
		time.sleep(0.05)


	def right_hand(self,angle,time):
		self.rapiro.write(mkcmd(self.RIGHT_HAND,angle,time))
		self.current_angles[self.RIGHT_HAND] = angle 

	def right_hand_left(self):
		self.rapiro.write(mkcmd(self.RIGHT_HAND,self.current_angles[self.RIGHT_HAND]+5,1))
		self.current_angles[self.RIGHT_HAND] += 5 
		time.sleep(0.05)

	def right_hand_right(self):
		self.rapiro.write(mkcmd(self.RIGHT_HAND,self.current_angles[self.RIGHT_HAND]-5,1))
		self.current_angles[self.RIGHT_HAND] -= 5 
		time.sleep(0.05)



	def right_foot_y(self,angle,time):
		self.rapiro.write(mkcmd(self.RIGHT_FOOT_Y,angle,time))
		self.current_angles[self.RIGHT_FOOT_Y] = angle 

	def right_foot_y_left(self):
		self.rapiro.write(mkcmd(self.RIGHT_FOOT_Y,self.current_angles[self.RIGHT_FOOT_Y]+5,1))
		self.current_angles[self.RIGHT_FOOT_Y] += 5 
		time.sleep(0.05)

	def right_foot_y_right(self):
		self.rapiro.write(mkcmd(self.RIGHT_FOOT_Y,self.current_angles[self.RIGHT_FOOT_Y]-5,1))
		self.current_angles[self.RIGHT_FOOT_Y] -= 5 
		time.sleep(0.05)



	def right_foot_p(self,angle,time):
		self.rapiro.write(mkcmd(self.RIGHT_FOOT_P,angle,time))
		self.current_angles[self.RIGHT_FOOT_P] = angle 

	def right_foot_p_left(self):
		self.rapiro.write(mkcmd(self.RIGHT_FOOT_P,self.current_angles[self.RIGHT_FOOT_P]+5,1))
		self.current_angles[self.RIGHT_FOOT_P] += 5 
		time.sleep(0.05)

	def right_foot_p_right(self):
		self.rapiro.write(mkcmd(self.RIGHT_FOOT_P,self.current_angles[self.RIGHT_FOOT_P]-5,1))
		self.current_angles[self.RIGHT_FOOT_P] -= 5 
		time.sleep(0.05)






	def left_shoulder_y(self,angle,time):
		self.rapiro.write(mkcmd(self.LEFT_SHOULDER_Y,angle,time))
		self.current_angles[self.LEFT_SHOULDER_Y] = angle 

	def left_shoulder_y_left(self):
		self.rapiro.write(mkcmd(self.LEFT_SHOULDER_Y,self.current_angles[self.LEFT_SHOULDER_Y]+5,1))
		self.current_angles[self.LEFT_SHOULDER_Y] += 5 
		time.sleep(0.05)

	def left_shoulder_y_right(self):
		self.rapiro.write(mkcmd(self.LEFT_SHOULDER_Y,self.current_angles[self.LEFT_SHOULDER_Y]-5,1))
		self.current_angles[self.LEFT_SHOULDER_Y] -= 5 
		time.sleep(0.05)



	def left_shoulder_p(self,angle,time):
		self.rapiro.write(mkcmd(self.LEFT_SHOULDER_P,angle,time))
		self.current_angles[self.LEFT_SHOULDER_P] = angle 

	def left_shoulder_p_left(self):
		self.rapiro.write(mkcmd(self.LEFT_SHOULDER_P,self.current_angles[self.LEFT_SHOULDER_P]+5,1))
		self.current_angles[self.LEFT_SHOULDER_P] += 5 
		time.sleep(0.05)

	def left_shoulder_p_right(self):
		self.rapiro.write(mkcmd(self.LEFT_SHOULDER_P,self.current_angles[self.LEFT_SHOULDER_P]-5,1))
		self.current_angles[self.LEFT_SHOULDER_P] -= 5 
		time.sleep(0.05)


	def left_hand(self,angle,time):
		self.rapiro.write(mkcmd(self.LEFT_HAND,angle,time))
		self.current_angles[self.LEFT_HAND] = angle 

	def left_hand_left(self):
		self.rapiro.write(mkcmd(self.LEFT_HAND,self.current_angles[self.LEFT_HAND]+5,1))
		self.current_angles[self.LEFT_HAND] += 5 
		time.sleep(0.05)

	def left_hand_right(self):
		self.rapiro.write(mkcmd(self.LEFT_HAND,self.current_angles[self.LEFT_HAND]-5,1))
		self.current_angles[self.LEFT_HAND] -= 5 
		time.sleep(0.05)



	def left_foot_y(self,angle,time):
		self.rapiro.write(mkcmd(self.LEFT_FOOT_Y,angle,time))
		self.current_angles[self.LEFT_FOOT_Y] = angle 

	def left_foot_y_left(self):
		self.rapiro.write(mkcmd(self.LEFT_FOOT_Y,self.current_angles[self.LEFT_FOOT_Y]+5,1))
		self.current_angles[self.LEFT_FOOT_Y] += 5 
		time.sleep(0.05)

	def left_foot_y_right(self):
		self.rapiro.write(mkcmd(self.LEFT_FOOT_Y,self.current_angles[self.LEFT_FOOT_Y]-5,1))
		self.current_angles[self.LEFT_FOOT_Y] -= 5 
		time.sleep(0.05)



	def left_foot_p(self,angle,time):
		self.rapiro.write(mkcmd(self.LEFT_FOOT_P,angle,time))
		self.current_angles[self.LEFT_FOOT_P] = angle 

	def left_foot_p_left(self):
		self.rapiro.write(mkcmd(self.LEFT_FOOT_P,self.current_angles[self.LEFT_FOOT_P]+5,1))
		self.current_angles[self.LEFT_FOOT_P] += 5 
		time.sleep(0.05)

	def left_foot_p_right(self):
		self.rapiro.write(mkcmd(self.LEFT_FOOT_P,self.current_angles[self.LEFT_FOOT_P]-5,1))
		self.current_angles[self.LEFT_FOOT_P] -= 5 
		time.sleep(0.05)


	def forward(self):
		self.rapiro.write("#M01")

	def backward(self):
		self.rapiro.write("#M02")

	def turn_right(self):
		self.rapiro.write("#M03")

	def turn_left(self):
		self.rapiro.write("#M04")

	def action(self,n):
		self.rapiro.write("#M"+mkstr(n,2))





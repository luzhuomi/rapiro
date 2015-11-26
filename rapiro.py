
import sys
import time
import serial

import os
import cv2
import numpy as np

import random

rand = random.Random()


from text2speech import speak

def mkstr(n,digits):
	return (("0" * digits) + str(n))[-digits:]



def mkcmd(servo, angle, time):
	return ("#PS%sA%sT%s" % (mkstr(servo,2), mkstr(angle,3), mkstr(time,3)))

def ledcmd(rgb,time):
	return ("#PR" + str(int(rgb[0])).zfill(3) + "G" + str(int(rgb[1])).zfill(3) + "B" + str(int(rgb[2])).zfill(3) + "T" + mkstr(time,3))

class Rapiro:

	# config
	SENSOR_PIN = 6
	RAPIRO_TTY = '/dev/ttyAMA0'
	rapiro = serial.Serial(RAPIRO_TTY, 57600, timeout = 10)

	# servo IDs
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

	# initial angles
	ANGLES = [90, 90,0,130, 90,180, 50, 90, 90, 90, 90, 90] 

	# LED colors
	LEDS = [0,0,255]

	current_angles = []
	current_leds = []

	# TODO move them to settings
	training_img_dir = "./pics"
	cascade_model_file = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"
	face_size=(90,90)
	cam = None
	model = None
	images = None
	labels = None
	names = None




	def __init__(self):
		# version check
		''' does not work for pi 2
		self.rapiro.write("#V")
		time.sleep(0.05)
		version = ""
		while self.rapiro.inWaiting():
		    version += self.rapiro.read(1)
		version = version.split("#Ver")[1]

		if(version != "00"):
			print "ERROR: Firmware of Rapiro is different."
			sys.exit(1)		
		'''
		self.current_angles = [ x for x in self.ANGLES ]
		self.current_leds = [ x for x in self.LEDS ] 
		return



	def init_cam(self):
		if self.cam is None:
			import os.path
			if not os.path.isfile(self.cascade_model_file):
				print "Cascade model (%s) not found." % (self.cascade_model_file)
				return False

			if not os.path.isdir(self.training_img_dir):
				print "Training directory (%s) not found." % (self.training_img_dir)
				print "Creating..."
				os.mkdir(self.training_img_dir)

			self.cam = cv2.VideoCapture(0)

			if ( not self.cam.isOpened() ):
				print "no cam!"
				return False
			
			print "cam: ok."
			self.cascade = cv2.CascadeClassifier(self.cascade_model_file)
			if ( self.cascade.empty() ):
				print "no cascade!"
				return False

			print "cascade: ok"

			# create the model
			self.model = cv2.createFisherFaceRecognizer()

			# train it from faces in the imgdir:
			self.images,self.labels,self.names = retrain(self.training_img_dir,self.model,self.face_size)

			print "trained:",len(self.images),"images",len(self.names),"persons"
			return True
		else:
			return True

	def close_cam(self):
		if self.cam is None:
			pass
		else:
			self.cam = None
		


	def look_for_face(self):
		found = False
		if self.cam is None:
			self.init_cam()

		rotation = self.head_right


		while (not found) and (self.cam is not None):
			print "searching..."
			ret, img = self.cam.read()
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			gray = cv2.equalizeHist(gray)
			rects = self.cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)

			roi = None

			results = []
			for x, y, w, h in rects:
				# crop & resize it 
				roi = cv2.resize( gray[y:y+h, x:x+h], self.face_size )
				# give some visual feedback for the cascade detection
				cv2.rectangle(img, (x,y),(x+w,y+h), (255, 0, 0))
				result = { 'name' : 'unknown', 'confidence' : 0}
				if len(self.images)>0:
					# model.predict is going to return the predicted label and
					# the associated confidence:
					[p_label, p_confidence] = self.model.predict(np.asarray(roi))
					
					name = "unknown"

					if p_label != -1 : name = self.names[p_label]
					print "x=%d,y=%d,x'=%d,y'=%d,conf=%.2f,name=%s" % (x,y,(x+w),(y+h),p_confidence,name)
					result['name'] = name
					result['confidence'] = p_confidence
				results.append(result)
			results = sorted(results, lambda x,y: cmp(y['confidence'],x['confidence']))

			if len(results) == 0:
				if self.head_is_left_most():
					rotation = self.head_right
				elif self.head_is_right_most():
					rotation = self.head_left
				rotation()
			else:
				print "found %s" % (results[0])
				found = True
				self.speak("hello %s" % (results[0]['name']))
				# self.blink_yellow(3)
				self.close_cam()
		return

	def picture(self):
		import picamera
		import datetime
		self.speak("Say cheese!")
		filename = "IMG" + datetime.datetime.now().isoformat() + ".jpg"
		camera = picamera.PiCamera() 
		camera.resolution = (1280, 720)
		camera.iso = 800
		camera.vflip = True
		camera.hflip = True
		camera.capture(filename)
		camera.close()

	def reset(self):
		#for i in range(0,12):
		#	self.rapiro.write(mkcmd(i,self.ANGLES[i],1))
		#	time.sleep(0.05)
		self.rapiro.write("#M00")
		self.current_angles = [ x for x in self.ANGLES ]
		self.current_leds = [ x for x in self.LEDS ] 
		self.close_cam()

	def speak(self,mesg):
		speak(mesg)
		self.blink_yellow(3)

	def blink_yellow(self,t):
		self.rapiro.write(ledcmd([255,255,0],t))
                self.rapiro.write(ledcmd(self.current_leds,t))
		return

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

	def turn_left(self):
		self.rapiro.write("#M03")

	def turn_right(self):
		self.rapiro.write("#M04")

	def action(self,n):
		self.rapiro.write("#M"+mkstr(n,2))


# image retrain
def retrain(imgpath, model,sz ) :
	# read in the image data. This must be a valid path!
	X,y,names = read_images(imgpath,sz)
	if len(X) == 0:
		print "image path empty", imgpath
	 	return [[],[],[]]
	# Learn the model. Remember our function returns Python lists,
	# so we use np.asarray to turn them into NumPy lists to make
	# the OpenCV wrapper happy:
	# Also convert labels to 32bit integers. This is a workaround for 64bit machines,
	model.train(np.asarray(X), np.asarray(y, dtype=np.int32))
	return [X,y,names]		



# added a names list(z)
def read_images(path, sz=None):
    """Reads the images in a given folder, resizes images on the fly if size is given.

    Args:
        path: Path to a folder with subfolders representing the subjects (persons).
        sz: A tuple with the size Resizes

    Returns:
        A list [X,y,z]

            X: The images, which is a Python list of numpy arrays.
            y: The corresponding labels (the unique number of the subject, person) in a Python list.
            z: A list of person-names, indexed by label
    """
    c = 0
    X,y,z = [], [], []
    for dirname, dirnames, filenames in os.walk(path):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                try:
                    im = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)
                    if (len(im)==0):
                        continue # not an image                        
                    # resize to given size (if given)
                    if (sz is not None):
                        im = cv2.resize(im, sz)
                    X.append(np.asarray(im, dtype=np.uint8))
                    y.append(c)
                except IOError, (errno, strerror):
                    print "I/O error({0}): {1}".format(errno, strerror)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
            c = c+1
            z.append(subdirname)
    return [X,y,z]




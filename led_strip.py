
import time
import RPi.GPIO as GPIO
from random import *

# Import the WS28xx Module
from neopixel import *

OFF_BTN_PIN             = 17        # GPIO pin connected to the off button
CHNG_BTN_PIN            = 27        # GPIO pin connected to the state change button






class LED_STRIP_OBJECT(object):

	# LED strip config:
	LED_COUNT           = 240       # Number of LED pixels
	LED_PIN             = 18        # GPIO pin connected to the pixels (PWM)
	#LED_PIN             = 10        # GPIO pin connected to the pixels (SPI)
	LED_FREQ_HZ         = 800000    # LED signal frequency in Hertz
	LED_DMA             = 10        # DMA channel for generating signal
	LED_BRIGHTNESS      = 128       # Brightness value (0 - 255)
	LED_INVERT          = False     # True inverts signal (for NPN transistor)
	LED_CHANNEL         = 0         # set to '1' for GPIO 13, 19, 41, 45, 53

	# creation of LED strip object
	strip = 0
	subState = 0
	stripState          = 0         # sets the current state of the strip
							# 0: off, 1: colorWipe, 2: theaterChase, 3: Rainbow
							# 4: rainbowCycle, 5: theaterChaseRainbow

	def colorWipe(self, strip, color, wait_ms=20):
		"""Wipe color across display one pixel at a time"""
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, color)
			strip.show()
			time.sleep(wait_ms/1000.0)

	def theaterChase(self, strip, color, wait_ms=20):
		"""Movie theater light styled chaser animation"""
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

	def wheel(self, pos=75):
		"""Generate rainbow colors across 0-255 positions"""
		if pos < 85:
			return Color(pos * 3, 255 - pos * 3, 0)
		elif pos < 170:
			pos -= 85
			return Color(255 - pos * 3, 0, pos * 3)
		else:
			pos -= 170
			return Color(0, pos * 3, 255 - pos * 3)

	def rainbow(self, strip, wait_ms=20):
		"""Draw rainbow that fades across all pixels at once"""
		for j in range(256):
			for i in range(strip.numPixels()):
				strip.setPixelColor(i, wheel(i+j))
			strip.show()
			time.sleep(wait_ms/1000.0)

	def rainbowCycle(self, strip, wait_ms=20):
		"""Rainbow that uniformly distributes itself across all pixels"""
		for j in range(256):
			for i in range(strip.numPixels):
				strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
			strip.show()
			time.sleep(wait_ms/1000.0)

	def theaterChaseRainbow(self, strip, wait_ms=20):
		"""Rainbow movie theater light style chaser animation"""
		for j in range(256):
			for q in range(3):
				for i in range(0, strip.numPixels(), 3):
					strip.setPixelColor(i+q, wheel((i+j) % 255))
				strip.show()
				time.sleep(wait_ms/1000.0)
				for i in range(0, strip.numPixels(), 3):
					strip.setPixelColor(i+q, 0)

	def stripOff(self, strip):
		for j in range(strip.numPixels()):
			strip.setPixelColor(j, 0)
		strip.show()

	def notify(self, state):
		if state == 0:
			self.stripState = 0
		else:
			self.stripState = (self.stripState + 1) % 6


	def __init__(self) -> None:
		# create strip
		self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
		# Initialize strip
		self.strip.begin()

		try:
			"""Looping method"""
			self.subState = 0
			while True:
				if self.stripState == 0:
					self.stripOff(self.strip)
				elif self.stripState == 1:
					self.colorWipe(self.strip, wheel(randint(0, 255)))
				elif self.stripState == 2:
					if self.subState == 0:
						self.theaterChase(self.strip, Color(127, 127, 127)) # white chase
						self.subState += 1
					elif subState == 1:
						self.theaterChase(self.strip, Color(127, 0, 0)) # red chase
						self.subState += 1
					elif subState == 2:
						self.theaterChase(self.strip, Color(0, 127, 0)) # green chase
						self.subState += 1
					else:
						self.subState = 0
						self.theaterChase(self.strip, Color(0, 0, 127)) # blue chase
				elif self.stripState == 3:
					self.rainbow(self.strip)
				elif self.stripState == 4:
					self.rainbowCycle(self.strip)
				else:
					self.theaterChaseRainbow(self.strip)
		except KeyboardInterrupt:
			self.stripOff(self.strip)

LED_STRIP = LED_STRIP_OBJECT()
GPIO.setmode(GPIO.BCM)
GPIO.setup(OFF_BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(CHNG_BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(OFF_BTN_PIN, GPIO.RISING, callback=offBtn, bouncetime=200)
GPIO.add_event_detect(CHNG_BTN_PIN, GPIO.RISING, callback=btnStateChange, bouncetime=200)
oldbtn1state = 0
oldbtn2state = 0

def offBtn(self, channel):
	print(0)
	LED_STRIP_OBJECT.notify(self, 0)

def btnStateChange(self, channel):
	print(1)
	LED_STRIP_OBJECT.notify(self, 1)

while True:
	btn1state = GPIO.in(OFF_BTN_PIN)
	if (btn1state != False) and (btn1state != oldbtn1state):
		LED_STRIP.notify(0)
	oldbtn1state = btn1state
	if (btn2state != False) and (btn2state != oldbtn2state):
		LED_STRIP.notify(0) 

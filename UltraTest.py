import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG = 14
ECHO = 24
print "Distance Measurement In Progress" 
while True:
	time.sleep(0.5)
	
	
	GPIO.setup(TRIG,GPIO.OUT)
	GPIO.output(TRIG,0) 
	
	GPIO.setup(ECHO,GPIO.IN)
	
	time.sleep(0.1)
	 
	print "Waiting for 1st Sensor" 
	
	GPIO.output(TRIG,1) 
	time.sleep(0.00001) 
	GPIO.output(TRIG,0) 
	
	while GPIO.input(ECHO)==0: 
		pass
	pulse_start = time.time()
	
	while GPIO.input(ECHO)==1: 
		pass
	pulse_end = time.time() 
	
	pulse_duration = pulse_end - pulse_start 
	distance = pulse_duration * 17150 
	distance = round(distance,2) 
	print "Distance:",distance,"cm"  
	#----------------------------------------------------------------------------	
	

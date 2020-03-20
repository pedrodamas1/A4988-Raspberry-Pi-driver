import RPi.GPIO as GPIO
import time



class A4988:


	def __init__(self, MS, STP, DIR):

		self.rpm = 0.0
		self.dt = 0.8 # seconds
		self.freq = 1/(2*self.dt)
		self.duty_cycle = 50
		self.mode = 0 # Choose from 0 to 4
		self.mode_names = ["full", "half", "quarter", "eight", "sixteenth"]
		self.modes = [[0,0,0], [1,0,0], [0,1,0], [1,1,0], [1,1,1]] # Use as self.modes[i]

		self.MS  = MS 		# Digital
		self.STP = STP 		# PWM
		self.DIR = DIR 		# Digital

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)

		GPIO.setup(self.MS, GPIO.OUT)
		GPIO.setup(self.STP, GPIO.OUT)
		GPIO.setup(self.DIR, GPIO.OUT)

		self.direction = False
		GPIO.output(self.DIR, direction)
		GPIO.output(self.MS, False)
		self.STP_pwm = GPIO.PWM(self.STP, self.freq)

		print("[OK! Initialization successful.")


	def set_mode(self, mode):	# OK

		self.mode = mode
		GPIO.output(self.MS, self.modes[self.mode])
		print("[OK!] Mode changed to: ", self.mode_names[self.mode])


	def reverse(self):	#OK

		self.direction = !self.direction
		GPIO.output(self.DIR, self.direction)
		print("[OK!] Direction successfully changed.")


	def set_speed(self, rpm):

		self.rpm = rpm
		self.dt = 60.0*1000.0 / (2.0*self.rpm*200.0*2**self.mode)
		self.freq = 1/(2*dt)
		self.STP_pwm.ChangeFrequency(self.freq)
		print("[OK!] Speed successfully changed.")
		

	def start(self, duty_cycle): # OK
		
		self.duty_cycle = duty_cycle
		self.STP_pwm.start(self.duty_cycle)
		print("[OK!] Duty cycle successfully changed.")


	def stop(self): # OK

		self.STP_pwm.stop()
		prnt("[OK!] Motor successfully stopped.")


# To change the duty cycle: p.ChangeDutyCycle(dc)


if __name__ == '__main__':

	MS_pins = [11, 13, 15]
	DIR_pin = 16
	STP_pin = 18
	NEMA17  = A4988(MS_pins, DIR_pin, STP_pin)

	NEMA17.set_mode(1) 		# Change to half steps
	NEMA17.set_speed(20)	# Set the speed to 20 RPM
	NEMA17.start(50) 		# Run the motor at 50% duty cycle
	time.sleep(2) 			# Let the motor run for 2 seconds
	NEMA17.stop()			# Stop the motor

	NEMA17.reverse()		# Reverse the direction of the motor
	NEMA17.set_speed(10)	# Change speed to 10 RPM
	NEMA17.start(50) 		# Run the motor at 50% duty cycle
	time.sleep(2) 			# Let the motor run for 2 seconds
	NEMA17.stop()			# Stop the motor

	GPIO.cleanup()



	# while True: # Main loop
	# 	try:

	# 		NEMA17.start(50)

	# 		for speed in range(0,100,10):
	# 			NEMA17.set_speed(speed)

	# 			for secs in range(0,1,0.2):
	# 				print("Take 10 measurements per second.")

	# 		NEMA17.stop()

	# 	except KeyboardInterrupt:

	# 		GPIO.output(self.MS, False)
	# 		GPIO.output(self.STP, False)
	# 		GPIO.output(self.DIR, False)
	# 		GPIO.cleanup()
	# 		print("Wrap up")
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

def isValidReading(values):
	if values[4] != 0 or values[5] != 1023:
		return False
	if all(v == 0 for v in values):
		return False
	if all(v == 1023 for v in values):
		return False
	return True

# Main program loop.
while True:
	# Read all the ADC channel values in a list.
	values = [0]*8
	for i in range(8):
		# The read_adc function will get the value of the specified channel (0-7).
		values[i] = mcp.read_adc(i)
	
	if isValidReading(values):
		x = values[1]
		y = values[3]
		
		if x < 300:
			print("Left")
		elif x > 700:
			print("Right")
		elif y < 90:
			print("Down")
		elif y > 300:
			print("Up")
		else:
			print("Not moving")
	else:
		print("Not valid reading - check wiring")
	
	# Pause for half a second.
	time.sleep(0.5)

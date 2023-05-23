import serial

ser =serial.Serial("COM3", 9600)

def turn_on():
	#  COMポートを開く
	ser.write(b"1")
	
def turn_off():
	#  COMポートを開く
	ser.write(b"0")



#Talking to Arduino via serial interface

import serial
from sys import argv
from os.path import isfile
import datetime

def str_to_int(s):
	i = int(s, 16)
	if i >= 2**15:
		i -= 2**16
	return i 
def dec_to_g(scale, d_num): #scale in miligramms and d_num decimal value
	if d_num >= 0:
		gram = (scale * d_num) / 32767
	else:
		gram = (scale * d_num) / 32768
	return gram

def dec_to_dps(scale, d_num): #scale in dps and d_num decimal value 
	if d_num >= 0:
		dps = (scale * d_num) / 32767
	else:
		dps = (scale * d_num) / 32768
	return dps
script, filename = argv
date = datetime.date.today() #get datetime in yyyy-mm-dd format
if isfile(filename): #check if the file exists
	print "We are going to overwrite %s file. Continue?" %filename
	f_choise = raw_input("1.Yes 2.No>>> ")
	if f_choise == '1': 
		print "Overwiting the file %s..." %filename
	elif f_choise == '2':
		print "Creating new name for your file..."
		filename = str(date)+ "-" + filename #create diferent name for the file
		if isfile(filename):
			print "File already exists...Please enter unique file name>>> "
			filename = raw_input() # get new file name from the user
		else:
			print "Writing to a new file %s" %filename		
	else:
		print "Make valid selection!"
else:
	 print "Writing data to a file %s" %filename
	
in_file = open(filename, 'w') #open file 

ser = serial.Serial(port = "COM2",
					baudrate = 9600) #start serial monitor 
line = 0
try:
	#colect the date until user press escape sequence (CTRL+C)
	while True:	
		in_dat = ser.readline() #read data line by line 
		#split incoming date to saparate lines, then convert it to integer
		#and write it to a file 
		xyz_hex = in_dat.split(' ') 
		
		xA_hex = xyz_hex[0]
		yA_hex = xyz_hex[1]
		zA_hex = xyz_hex[2]
		xG_hex = xyz_hex[3]
		yG_hex = xyz_hex[4]
		zG_hex = xyz_hex[5]
		time = xyz_hex[6]
		xA_dec = str_to_int(xA_hex) 
		yA_dec = str_to_int(yA_hex)
		zA_dec = str_to_int(zA_hex)
		xG_dec = str_to_int(xG_hex)
		yG_dec = str_to_int(yG_hex)
		zG_dec = str_to_int(zG_hex)
		time_dec = int(time, 16)
		x_gram = dec_to_g(2000, xA_dec)
		y_gram = dec_to_g(2000, yA_dec)
		z_gram = dec_to_g(2000, zA_dec)
		x_dps = dec_to_dps(245, xG_dec)
		y_dps = dec_to_dps(245, yG_dec)
		z_dps = dec_to_dps(245, zG_dec)
		
		to_file = "%d %d %d %d %d %d %d " %(x_gram, y_gram, 
			z_gram, x_dps, y_dps, z_dps, time_dec)
		in_file.write(to_file)
		
		print to_file
except KeyboardInterrupt: #exception to handle user interupt 
	print "Interupted by user..."

in_file.close() #close the file

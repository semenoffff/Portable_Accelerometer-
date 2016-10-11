"""
This program communicates with Arduino Uno via serial port
and produces live graph updates. This program was developed to read
data from LSM6DS3 accelerometer/gyroscope which is connected to Arduino
and then display data interactively.

Author: Oleksandr Semenov
Email: semenov221@gmail.com
Date: 10/11/2016
"""
import serial
from sys import argv
from os.path import isfile
import datetime
import matplotlib 
import matplotlib.pyplot as plt
import matplotlib.animation as animation 

matplotlib.style.use('ggplot')

def str_to_int(s):
	i = int(s, 16)
	if i >= 2**15:
		i -= 2**16
	return i 
def dec_to_g(scale, d_num): #scale in milligrams and d_num decimal value
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
	
def read_ser(i): # function that will read data from serial port and plot it	
	try:
		in_dat = ser.readline() #read data line by line 
		
		xyz_hex = in_dat.split(' ') #split incoming date to separate lines
		
		xA_hex = xyz_hex[0]
		yA_hex = xyz_hex[1]
		zA_hex = xyz_hex[2]
		xG_hex = xyz_hex[3]
		yG_hex = xyz_hex[4]
		zG_hex = xyz_hex[5]
		time = xyz_hex[6]
		# convert data to integer
		xA_dec = str_to_int(xA_hex) 
		yA_dec = str_to_int(yA_hex)
		zA_dec = str_to_int(zA_hex)
		xG_dec = str_to_int(xG_hex)
		yG_dec = str_to_int(yG_hex)
		zG_dec = str_to_int(zG_hex)
		time_dec = int(time, 16)
		# convert integer values to dps for gyroscope data 
		# and grams for accelerometer
		x_gram = dec_to_g(2000, xA_dec)
		y_gram = dec_to_g(2000, yA_dec)
		z_gram = dec_to_g(2000, zA_dec)
		x_dps = dec_to_dps(245, xG_dec)
		y_dps = dec_to_dps(245, yG_dec)
		z_dps = dec_to_dps(245, zG_dec)
		# prepare list of values to be plotted	
		xA_list.append(x_gram)
		yA_list.append(y_gram)
		zA_list.append(z_gram)
		xG_list.append(x_dps)
		yG_list.append(y_dps)
		zG_list.append(z_dps)
		time_list.append(time_dec)
		
		fig.clf() # clear figure on every iteration to avoid graphs overlapping 
		plt.subplot(2,1,1) # create subplot for accelerometer data
		plt.title('Accelerometer [Top] and Gyroscope [Buttom] Live Updates')
		linexA, = plt.plot(time_list, xA_list, label = "X_Acc")
		lineyA, = plt.plot(time_list, yA_list, label = "Y_Acc")
		linezA, = plt.plot(time_list, zA_list, label = "Z_Acc")
		plt.legend((linexA, lineyA, linezA),('X_Acc', 'Y_Acc', 'Z_Acc'),loc = 'best', fontsize = 'small')		
		plt.ylabel('XYZ Accelerometer Data[mg]')
		plt.xlabel('Time[s]')
		plt.grid(True)
		
		plt.subplot(2,1,2) # create subplot for gyroscope data
		linexG, = plt.plot(time_list, xG_list, label = "X_Gyro")
		lineyG, = plt.plot(time_list, yG_list, label = "Y_Gyro")
		linezG, = plt.plot(time_list, zG_list, label = "Z_Gyro")
		plt.legend((linexG, lineyG, linezG),('X_Gyro', 'Y_Gyro', 'Z_Gyro'),loc = 'best', fontsize = 'small')
		plt.ylabel('XYZ Gyroscope Data[dps] ')
		plt.xlabel('Time[s]')
		plt.grid(True)
			
		to_file = "%d %d %d %d %d %d %d " %(x_gram, y_gram, 
			z_gram, x_dps, y_dps, z_dps, time_dec)
		in_file.write(to_file)
		print to_file
		
	except KeyboardInterrupt: #exception to handle user interrupt 
		print "Interrupted by user..."

		in_file.close() #close the file
	
script, filename = argv #input arguments script name and name of the file 
# where incoming data will be saved

fig = plt.figure(figsize = (14, 8))

# define lists where data will be stored for plotting 
xA_list = []
yA_list = []
zA_list = []
xG_list = []
yG_list = []
zG_list = []
time_list = []

date = datetime.date.today() #get datetime in yyyy-mm-dd format

if isfile(filename): #check if the file exists
	print "We are going to overwrite %s file. Continue?" %filename
	f_choise = raw_input("1.Yes 2.No>>> ")
	if f_choise == '1': 
		print "Overwriting the file %s..." %filename
	elif f_choise == '2':
		print "Creating new name for your file..."
		filename = str(date)+ "-" + filename #create different name for the file
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

# !!!WARNING!!! Port number may vary. Check the port number where Arduino 
# connected to and adjust port value accordingly 
ser = serial.Serial(port = "COM4",
					baudrate = 9600) #start serial monitor 

# Animation function will call read_ser every second. 
# Adjust interval value to have graphs update slower or faster.
ani = animation.FuncAnimation(fig, read_ser, interval = 1000)
plt.show()


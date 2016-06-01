from sys import argv
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D

script, fileRead = argv

print "Reading from the file %s..." %fileRead
#open file --> read from the file --> close the file 
target = open(fileRead, 'r')
file_data = target.read()
target.close()

numbers = file_data.split(' ') #split string in to list of strings
numbers.pop() #remove last element in the list to avoid error 
#when converting to the list
stuffToPlot = map(int, numbers) #convert to an integer
#initialize for each axes and counter variable for loops
xA_list = []
yA_list = []
zA_list = []
Ax = 0
Ay = 1
Az = 2
xG_list = []
yG_list = []
zG_list = []
Gx = 3
Gy = 4
Gz = 5
time_list = []
time = 6
#break list that we read from the file in to saparate list for each axes
while Ax < len(stuffToPlot): 
	xA_list.append(stuffToPlot[Ax])
	yA_list.append(stuffToPlot[Ay])
	zA_list.append(stuffToPlot[Az])
	xG_list.append(stuffToPlot[Gx])
	yG_list.append(stuffToPlot[Gy])
	zG_list.append(stuffToPlot[Gz])
	time_list.append(stuffToPlot[time])
	Ax += 7
	Ay += 7
	Az += 7
	Gx += 7
	Gy += 7
	Gz += 7
	time += 7
#plot set up 
plt.subplot(211)
linexA, = plt.plot(time_list, xA_list, label = "X_Acc")
lineyA, = plt.plot(time_list, yA_list, label = "Y_Acc")
linezA, = plt.plot(time_list, zA_list, label = "Z_Acc")
plt.legend(handler_map={linexA: HandlerLine2D(numpoints=4)})
plt.ylabel('XYZ Accelerometer Data[mg]')
plt.xlabel('Time[s]')
plt.grid(True)

plt.subplot(212)
linexG, = plt.plot(time_list, xG_list, label = "X_Gyro")
lineyG, = plt.plot(time_list, yG_list, label = "Y_Gyro")
linezG, = plt.plot(time_list, zG_list, label = "Z_Gyro")
plt.legend(handler_map={linexG: HandlerLine2D(numpoints=4)})
plt.ylabel('XYZ Gyroscope Data[dps] ')
plt.xlabel('Time[s]')
plt.grid(True)

plt.show()

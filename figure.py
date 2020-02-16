import tkinter as tk
#from openpyxl import *
#from openpyxl import Workbook, load_workbook
#from tkinter import Frame
#import xlrd
import math
import serial
import time


ser1 = serial.Serial('COM6', 9600)
p=[]
q=[]
def motion(event):
    root.bind('<Motion>', myfunction)

def myfunction(event):

    x, y = event.x, event.y
    if canvas.old_coords:
        x1, y1 = canvas.old_coords

        canvas.create_line(x, y, x1, y1)
        #print(x,y,x1,y1)
        dist=math.sqrt((int(x1)-int(x))**2 + (int(y1)-int(y))**2)
        dis_coord = format(int(dist), '03d')
        if ((x-x1) < 0):
            dis_coord=-1*int(dis_coord)
        dis_str =str(dis_coord)
        if x==x1:
            angle=90
        else:
            angle = (int(y) - int(y1)) / (int(x) - int(x1))
        ang_degrees = math.degrees(math.atan(angle))
        angle_coord = format(int(ang_degrees), '03d')
        print(angle_coord)
        print(dis_coord)
        send_str = str(angle_coord)
        p.append(angle_coord)
        p.append(dis_str)
        global t,b
        t=p[0]
        b=p[1]
    canvas.old_coords = x, y

def end(event):

   # print(t)
    #print(b)
    send_str = str(t)
    send_str1=str(b)
    q.append(t)
    q.append(b)
    #ser1.write(send_str.encode())
    # ser1.write(send_str1.encode())
    i = 0
    while i < len(p)-2:
        if (int(p[i]) <= 0 and int(p[i+2]) <= 0) and (int(p[i+3]) >= 0):
            q.append(-int(p[i]) + int(p[i + 2]))
            q.append(int(p[i+3]))
        elif (int(p[i]) < 0 and int(p[i+2]) < 0) and (int(p[i+3])<0) and (abs(int(p[i]))>abs((int(p[i+2])))):
            q.append(-180-int(p[i]) + int(p[i + 2]))
            q.append(int(p[i + 3]))
        elif (int(p[i]) < 0 and int(p[i+2]) < 0) and (int(p[i+3])<0) and (abs(int(p[i])))<(abs(int(p[i+2]))):
            q.append(180-int(p[i]) + int(p[i + 2]))
            q.append(int(p[i + 3]))
        elif (int(p[i]) < 0 and int(p[i+2]) > 0) and (int(p[i+3])>=0):
            q.append(-int(p[i]) + int(p[i + 2]))
            q.append(int(p[i + 3]))
        elif (int(p[i]) < 0 and int(p[i+2]) > 0) and (int(p[i+3])<0):
            q.append(-180 - int(p[i]) + int(p[i + 2]))
            q.append(int(p[i + 3]))
        elif ((int(p[i]) > 0 and int(p[i + 2])) < 0) and (int(p[i+3])<0):
            q.append(- int(p[i]) + int(p[i + 2]))
            q.append(int(p[i + 3]))
        elif ((int(p[i]) > 0 and int(p[i + 2])) < 0) and (int(p[i + 3]) > 0):
            q.append(180 - int(p[i]) + int(p[i + 2]))
            q.append(int(p[i + 3]))
        elif ((int(p[i]) > 0 and int(p[i + 2])) > 0) and (int(p[i+3])>0) and (abs(int(p[i])))<(abs(int(p[i+2]))):
            q.append(-180 - int(p[i]) + int(p[i + 2]))
            q.append(int(p[i + 3]))
        elif ((int(p[i]) > 0 and int(p[i + 2])) > 0) and (int(p[i + 3]) > 0) and (abs(int(p[i])))>(abs(int(p[i + 2]))):
            q.append(180-int(p[i]) + int(p[i + 2]))
            q.append(int(p[i + 3]))
        elif ((int(p[i]) > 0 and int(p[i + 2])) > 0) and (int(p[i+3])<0):
            q.append(-int(p[i]) + int(p[i + 2]))
            q.append(int(p[i + 3]))
        else:
            break;

        i = i + 2
    j=0
    for j in range(len(p)):
        if(j%2!=0):
            q[j]=abs(int(q[j]))
        q[j]=format(int(q[j]),'04d')
        print(q[j])
    k=0
    r1=1
    time.sleep(2)
    while (k < len(q)):
        str3=str(q[k])+str(q[k+1])+"\n"
        print(str3)
        ser1.write(str3.encode())
        while(ser1.in_waiting == 0):
            v = 0
            u = 0
        v = ser1.readline()
        #u = ser1.readline()
        #print(v, " ", u)
        print(v)
      #  while serial!="ok":
       #     serial = ser1.read(ser1.inWaiting())
        print(serial)
        k=k+2
    ser1.flush()
    exit()



root = tk.Tk()




canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()
canvas.old_coords = None

root.bind('<Button 1>', myfunction)
root.bind('<Shift-Up>',end)


root.mainloop()
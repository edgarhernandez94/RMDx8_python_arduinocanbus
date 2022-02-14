import serial
import array
import time
import re
import sys
import glob
import serial


import serial.tools.list_ports
comlist = serial.tools.list_ports.comports()
connected = []
for element in comlist:
    connected.append(element.device)
print("Connected COM ports: " + str(connected))
port=input("PortCOM:")
arduino = serial.Serial(port=port, baudrate=115200, timeout=0.5)
global data
def motorcurrent(current,motorid):
        cmd_buf = bytes([motorid-0x60,0xA1, 0x00, 0x00, 0x00, current & 0xFF, (current>>8) & 0xFF, 0x00, 0x00])
        arduino.write(cmd_buf)
        time.sleep(0.01)
        #print(cmd_buf[0])
                                            
def motorposition(angle,max_speed,direction,motorid):
        global data      
        cmd_buf1 = [motorid-0x60,0xA4, 0X00, max_speed*6& 0xFF, (max_speed*6>>8) & 0xFF, angle*600 & 0xFF, (angle*600>>8) & 0xFF, (angle*600>>16) & 0xFF, (angle*600>>24) & 0xFF]
        arduino.write(cmd_buf1)
        angle2=angle-5
        angle3=angle+5
        while True:
                readPosition()     
                if data==str(angle2) or data==str(angle2):
                        break 
        #print(cmd_buf1[0])

def motorspeed(speed,motorid):
        cmd_buf = [motorid-0x60,0xA2, 0x00, 0x00, 0x00, speed & 0xFF, (speed>>8) & 0xFF, (speed>>16) & 0xFF, (speed>>24) & 0xFF]
        arduino.write(cmd_buf)
        time.sleep(0.01)
        #print(cmd_buf[0])

def positionloop(pos1,pos2,max_speed,max_speed2,motorid):
        global data 
        cmd_buf = [motorid-0x60,0xA4, 0X00, max_speed*6 & 0xFF, (max_speed*6>>8) & 0xFF, pos1*600 & 0xFF, (pos1*600>>8) & 0xFF, (pos1*600>>16) & 0xFF, (pos1*600>>24) & 0xFF]
        cmd_buf1 = [motorid-0x60,0xA4, 0X00, max_speed2*6 & 0xFF, (max_speed2*6>>8) & 0xFF, pos2*600 & 0xFF, (pos2*600>>8) & 0xFF, (pos2*600>>16) & 0xFF, (pos2*600>>24) & 0xFF]
        while True:
                arduino.write(cmd_buf)
                time.sleep(0.01)
                angle2=pos1-5
                angle3=pos1+5
                angle4=pos2-5
                angle5=pos2+5
                while True:
                        readPosition()     
                        if data==str(pos1):
                                break
                
                arduino.write(cmd_buf1)
                time.sleep(0.01)
                
                while True:
                        readPosition()     
                        if data==str(pos2):
                                break
        #print(cmd_buf[0])

def readPosition():
        global data
        cmd_buf = [motorid-0x60,0x92, 0X00, 0X00,0X00,0X00,0X00, 0X00,0X00]
        arduino.write(cmd_buf)
        time.sleep(0.01)
        data = arduino.readline()
        #data = [int(s) for s in re.findall(r'\b\d+\b', str(data))]
        data =''.join(filter(str.isdigit,str(data)))


if __name__ == '__main__':
        print("Select control:")
        print("1 ----- Current control")
        print("2 ----- Position control")
        print("3 ----- Velocity control")
        print("4 ----- Position Loop")
        controltype=input("Control number:")

        if int(controltype)==1: 
                motorid=int(input("Motorid:"),16)
                
                while True:                        
                        current=int(input("Current value:"))
                        motorcurrent(current,motorid)
                        pass

        if int(controltype)==2:
                motorid=int(input("Motorid:"),16)
                
                while True:                        
                        angle=int(input("Angle value (degree):"))
                        ##angle=(angle*600)/255
                        max_speed=int(input("Max speed value(degree per second):"))
                        print("0 ----- Clockwise")
                        print("1 ----- Anticlockwise")
                        direction=int(input("Direction value:"))
                        motorposition(angle,max_speed,direction,motorid)
                        pass

        if int(controltype)==3:
                motorid=int(input("Motorid:"),16)
                
                while True:                        
                        speed=int(input("Speed value(degree per second):"))
                        speed=speed*600
                        motorspeed(speed,motorid)
                        pass

        if int(controltype)==4:
                motorid=int(input("Motorid:"),16)
                
                while True:
                        pos1=int(input("Position 1 value (degree):"))
                        max_speed=int(input("Speed(degree per second):"))
                        pos2=int(input("Position 2 value (degree):"))
                        max_speed2=int(input("Speed2 (degree per second):"))
                        #direction=int(input("Speed:"))
                        positionloop(pos1,pos2,max_speed,max_speed2,motorid)
                        pass

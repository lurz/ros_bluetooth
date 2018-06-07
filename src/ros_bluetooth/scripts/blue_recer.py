#!/usr/bin/env python
# Receive message from PC and send it to android phone by bluetooth.
import rospy
import serial
import time
from std_msgs.msg import String

class receiver:
    def commback(self, data):
        command = data.data
        rospy.loginfo(command)
        # Send message to serial port.
        ser = serial.Serial('/dev/rfcomm0')
        if command == "StartScan":
            ser.write(b'StartScan')
        if command == "StopScan":
            ser.write(b'StopScan')
        ser.close()
        
    def listener(self):
        # Receive message from ros topic
        rospy.init_node('listener', anonymous=True)
        rospy.Subscriber("bluetooth_receiver", String, self.commback)
        rospy.spin()

if __name__ == '__main__':
    my_recv = receiver()
    my_recv.listener()
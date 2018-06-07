#!/usr/bin/env python
#Receive message from bluetooth and send it through ros topic, then forward by ros bridge.
import rospy
import serial
import os
import time
from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovarianceStamped

class sender:
    pose_data = []

    def poseback(self, data):
        pose = data.pose
        # rospy.loginfo(pose.pose.position.x)
        # rospy.loginfo(pose.pose.position.y)
        self.pose_data = [str(float("{0:.2f}".format(float(pose.pose.position.x))))
                ,str(float("{0:.2f}".format(float(pose.pose.position.y))))]

    def talker(self):
        pub = rospy.Publisher('bluetooth_sender', String, queue_size=10)
        serial_pathname = "/dev/rfcomm0"
        # while not os.path.isfile(serial_pathname):
        #     time.sleep(1)
        #     rospy.loginfo("try")
        ser = serial.Serial(serial_pathname, 19200, timeout=1)
        rospy.init_node('talker', anonymous=True)
        while not rospy.is_shutdown():
            try:
                #read from serial port.
                back_msg = ser.read(100)
            except:
                time.sleep(3)
                continue
            # process message and publish to ros topic
            if back_msg and "Counter" in back_msg:
                rospy.loginfo(back_msg)
                rospy.Subscriber("amcl_pose", PoseWithCovarianceStamped, self.poseback)
                s_line = back_msg.split("*")[2].split(" ")
                time_counter = 0
                while time_counter < 12:
                    if self.pose_data:
                        rospy.loginfo('0,0,' + ','.join(self.pose_data) + ',' + ','.join(s_line))
                        pub.publish('0,0,' + ','.join(self.pose_data) + ',' + ','.join(s_line))
                        break
                    time.sleep(0.01)
                    time_counter += 1
            if back_msg and "test" in back_msg:
                rospy.Subscriber("amcl_pose", PoseWithCovarianceStamped, self.poseback)
                time_counter = 0
                while time_counter < 12:
                    if self.pose_data:
                        rospy.loginfo(str(self.pose_data))
                        pub.publish(str(self.pose_data))
                        break
                    time.sleep(0.01)
                    time_counter += 1
            self.pose_data = []

if __name__ == '__main__':
    my_sender = sender()
    try:
        my_sender.talker()
    except rospy.ROSInterruptException:
        pass
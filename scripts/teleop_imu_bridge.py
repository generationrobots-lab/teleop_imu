#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist
import math
class TeleopImu():
    def __init__(self):
        self.offset_linear= None
        self.offset_angular=None
        self.cmd = Twist()
        self.last_cmd_stamp = rospy.get_time()
        self.sub = rospy.Subscriber("android/imu", Imu, self.callback, queue_size=1)
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        self.timer = rospy.Timer(rospy.Duration(1.0/20.0), self.control_loop)
    def callback(self,data):
                    
        
        if self.offset_angular is None:
            self.offset_angular = data.orientation.x 
        if self.offset_linear is None:
            self.offset_linear = data.orientation.y
        new_z = data.orientation.x - self.offset_angular
        new_x = data.orientation.y - self.offset_linear
        self.last_cmd_stamp = rospy.get_time() # update last time stamp
        if math.fabs(self.cmd.linear.x-new_x) > 0.01 or math.fabs(self.cmd.angular.z-new_z) > 0.01:
            self.cmd.angular.z = new_z  
            self.cmd.linear.x = new_x
        print "linear: " , self.cmd.linear.x, " angular" , self.cmd.angular.z
        
    def control_loop(self,*args): # publish vel command every 20ms
        # in case there has not been any message for 200ms -> send stop
        # stop also on very small velocities to protect motors from overheating while standing still
        if((rospy.get_time() > self.last_cmd_stamp + 0.2) or
            (math.fabs(self.cmd.linear.x)<0.02 and math.fabs(self.cmd.angular.z) < 0.03)): 
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = 0.0
        
        self.pub.publish(self.cmd)

if __name__ == '__main__':
    rospy.init_node("teleop_imu")
    ti = TeleopImu()
    rospy.spin()
#!/bin/bash


source_ros() {
    {
        source /opt/ros/kinetic/setup.bash > /dev/null 2>&1
    }||{
        source /opt/ros/indigo/setup.bash > /dev/null 2>&1 
    }||{
    	echo "Could not source indigo or kinetic rosbash"  && exit 1
    }
}  

source $HOME/ros_ws/devel/setup.bash
roslaunch teleop_imu tb3_core_imu.launch

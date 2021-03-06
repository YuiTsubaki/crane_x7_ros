#!/usr/bin/env python
# coding: utf-8
# Writen by Shota Hirama

import rospy
import actionlib
from control_msgs.msg import (
    FollowJointTrajectoryAction,
    FollowJointTrajectoryGoal
)
from control_msgs.msg import (      #Add 3lines
    GripperCommandAction,
    GripperCommandGoal
 )

from trajectory_msgs.msg import JointTrajectoryPoint
import math
import sys

class GripperClient(object):  #Add class
    def __init__(self):
        self._client = actionlib.SimpleActionClient("/crane_x7/gripper_controller/gripper_cmd",GripperCommandAction)
        self._goal = GripperCommandGoal()

        # Wait 5 Seconds for the gripper action server to start or exit
        self._client.wait_for_server(rospy.Duration(5.0))
        if not self._client.wait_for_server(rospy.Duration(5.0)):
            rospy.logerr("Exiting - Gripper Action Server Not Found.")
            rospy.signal_shutdown("Action Server not found.")
            sys.exit(1)
        self.clear()

    def command(self, position, effort):
        self._goal.command.position = position
        self._goal.command.max_effort = effort
        self._client.send_goal(self._goal,feedback_cb=self.feedback)

    def feedback(self,msg):
        print("feedback callback")
        print(msg)

    def stop(self):
        self._client.cancel_goal()

    def wait(self, timeout=0.1 ):
        self._client.wait_for_result(timeout=rospy.Duration(timeout))
        return self._client.get_result()

class ArmJointTrajectoryExample(object):
    def __init__(self):
        self._client = actionlib.SimpleActionClient(
            "/crane_x7/arm_controller/follow_joint_trajectory", FollowJointTrajectoryAction)
        rospy.sleep(0.1)
        if not self._client.wait_for_server(rospy.Duration(secs=5)):
            rospy.logerr("Action Server Not Found")
            rospy.signal_shutdown("Action Server Not Found")
            sys.exit(1)

    def move_arm(self):
        goal = FollowJointTrajectoryGoal()
        goal.trajectory.joint_names = ["crane_x7_shoulder_fixed_part_pan_joint", "crane_x7_shoulder_revolute_part_tilt_joint",
                                       "crane_x7_upper_arm_revolute_part_twist_joint", "crane_x7_upper_arm_revolute_part_rotate_joint",
                                       "crane_x7_lower_arm_fixed_part_joint", "crane_x7_lower_arm_revolute_part_joint",
                                       "crane_x7_wrist_joint",]

          
       # goal.trajectory.joint_names = ["crane_x7_shoulder_fixed_part_pan_joint"]
        
        print"Goal"
        print(goal)

        point = JointTrajectoryPoint()

        print"Point"
        print(point)

        point.positions.append(math.radians(30.0))
        point.positions.append(math.radians(-30.0))
        point.positions.append(math.radians(30.0))
        point.positions.append(math.radians(-100.0))
        point.positions.append(math.radians(30.0))
        point.positions.append(math.radians(10.0))
        point.positions.append(math.radians(30.0))
        #point.positions.append(math.radians(80.0))
        
        point.time_from_start = rospy.Duration(secs=1.0)


        print"\n\nPoint append positions and time "
        print(point)
        
        goal.trajectory.points.append(point)

        print"\n\nGoal.append"
        print(goal)
        self._client.send_goal(goal)
        self._client.wait_for_result(timeout=rospy.Duration(100.0))
        return self._client.get_result()
        
        """joint_values = [-30.0, -10.0, -30.0, 0.0, -20.0]
        joint_values.extend(reversed(joint_values))
        for i, p in enumerate(joint_values):
            point = JointTrajectoryPoint()
            for _ in range(len(goal.trajectory.joint_names)):
                point.positions.append(math.radians(p))
            point.time_from_start = rospy.Duration(secs=i)
            goal.trajectory.points.append(point)
        self._client.send_goal(goal)
        self._client.wait_for_result(timeout=rospy.Duration(100.0))
        return self._client.get_result()
        """


if __name__ == "__main__":
    rospy.init_node("arm_joint_trajectory_example")
    arm_joint_trajectory_example = ArmJointTrajectoryExample()
    result = arm_joint_trajectory_example.move_arm()
    print(result)

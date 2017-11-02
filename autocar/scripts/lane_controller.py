import  sys  
import roslib; roslib.load_manifest('autocar')  
import rospy 
from std_msgs.msg import String  
from autocar.msg import *
from geometry_msgs.msg import Twist
from nav_msgs.msg import *
import numpy as np
import json

class SpeedController:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.hz = 10
        self.initPubs()
        self.rate = rospy.Rate(self.hz) 
        np.random.seed(self.config["random_seed"])

    def initPubs(self):
        self.robots = [] 
        robot_id = 0
        for i in range(self.config["num_lanes"]):
            num_car_lane = self.config['num_cars_per_lane'][i]
            for j in range(num_car_lane):
                key = 'robot_' + str(robot_id + 1)
                self.robots.append({"lane":j, "pub":rospy.Publisher(key + '/cmd_vel', Twist, queue_size=1)})
                robot_id += 1

    def update_vel(self, i):
        mean_vel = self.config["mean_speed_per_lane"][i]
        stdrr_vel = self.config["stdrr_speed_per_lane"][i]
        return np.random.normal(mean_vel, stdrr_vel)

    def run(self):
        while not rospy.is_shutdown():
            # publish the speed for each robot
            for robot in self.robots:
                vel = self.update_vel(robot["lane"])
                self.send_control(robot["pub"], vel)
            self.rate.sleep()
            
    def send_control(self, robot_pub, vel):
        msg = Twist()
        msg.linear.x = vel
        msg.angular.z = 0
        robot_pub.publish(msg)

if __name__=='__main__':

    if len(sys.argv) < 2:
        print("Please specify the config file.")

    rospy.init_node('agent_controller')

    controller = SpeedController(sys.argv[1])
    print("Press any key to start")
    raw_input()
    controller.run()
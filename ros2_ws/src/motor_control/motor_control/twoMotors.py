#sends required speed to each motor, tracks current position and speed

import rclpy
from rclpy.node import Node
import time
from std_msgs.msg import Int32,Float32, Float32MultiArray
import numpy as np


class twoMotors(Node):
    TargetL = 0.0
    TargetR = 0.0
    currentVelL =0
    currentVelR =0
    stop = 0
    def __init__(self):

        #Publisher for sending speed information to motor
        super().__init__('twoMotors')
        self.leftMotor_ = self.create_publisher(Float32, 'motorLeft', 10)
        timer_period = 0.1  # seconds
        self.timerL = self.create_timer(timer_period, self.motor_callbackL)
        self.iL = 0
        self.rightMotor_ = self.create_publisher(Float32, 'motorRight', 10)
        self.timerR = self.create_timer(timer_period, self.motor_callbackR)
        self.iR = 0
        
        #Subscribing target speed and target location from User input
        self.speedSub = self.create_subscription(Float32MultiArray, 'speed', self.speed,10)
        self.locationSub = self.create_subscription(Float32MultiArray, 'location', self.location,10)

        #Detecting obstacle and send stop signal to the motor
        self.stopSub= self.create_subscription(Int32, 'stop', self.stop_callback, 10)
        
        #Subscriber for getting the current RPM from encoder node
        self.encoderSub = self.create_subscription(Float32MultiArray, 'encoderValue', self.velocity_callback, 10)
        
        #declaring local variables for position and turning
        self.total_meter =0
        self.locationReq = 0.0
        self.turn =0.0
        self.turning =True
        self.goal=0
        self.turngoal =0.0
        self.turnradius =0 
        self.initialValue = 0
        self.third = False
        self.straight = True
        
        #Records the current position
        self.positionPub = self.create_publisher(Float32, "position", 10)
        self.timer2 = self.create_timer(0.1, self.position)

    def location(self,msg):
        self.locationReq =msg.data[0]
        #self.get_logger().info('Location received: "%f"' % self.distance[0])

    
    def position(self):
        
        #Location A programmed to go straight 4.34m and stop, Location B will turn left and go straight for 4.17m, and Location C will go straight 3.7m 
        # turn right and go straight for 3.66m
        locationA = 4.34
        diameter = 0.1524
        if self.stop==0:
            if self.locationReq == 1.0:
                
                #Speed and distance travelled calculation
                avg_speed = (self.TargetL + self.TargetR)
                RPM = avg_speed*600
                m_s = RPM*np.pi*diameter/60
                meter = m_s * 0.1 #measured every 0.1 second
                
                self.total_meter += meter/5
                self.get_logger().info('Publish position: "%f"' % self.total_meter)
                     
                if self.total_meter>=locationA: 
                    self.TargetL =0
                    self.TargetR =0
                    # if len(self.distance) !=0:
                    #     self.goal = self.distance.pop(0)
                    self.total_meter =0

            elif self.locationReq==2.0:
                if self.turning:
                    self.TargetL = 0
                    avg_speed = (self.TargetL + self.TargetR)
                    RPM = avg_speed*600
                    m_s = RPM*np.pi*diameter/60
                    meter2 = m_s * 0.1 #measured every 0.1 second
                    
                    self.turnradius += meter2/5
                    self.get_logger().info('Publish radius: "%f"' % self.total_meter)
                
                    
                if self.turnradius>=0.28: 
                    self.turning = False
                    self.TargetL=self.TargetR
                    avg_speed = (self.TargetL + self.TargetR)
                    RPM = avg_speed*600
                    m_s = RPM*np.pi*diameter/60
                    meter = m_s * 0.1 #measured every 0.1 second
                    
                    self.total_meter += meter/5
                    self.get_logger().info('Publish position: "%f"' % self.total_meter)
                
                    
                    if self.total_meter>=4.17: 
                        self.TargetL =0
                        self.TargetR =0
                        self.total_meter =0

            elif self.locationReq==3.0:
                avg_speed = (self.TargetL + self.TargetR)
                RPM = avg_speed*600
                m_s = RPM*np.pi*diameter/60
                meter = m_s * 0.1 #measured every 0.1 second
                
                self.total_meter += meter/5
                self.get_logger().info('Publish position: "%f"' % self.total_meter)
            
                
                if self.total_meter>=3.7 and self.straight: 
                    self.total_meter =0
                    self.turnradius =0
                    self.turning = True
                    self.third = True

                if self.turning and  self.third:
                    self.TargetR = 0
                    avg_speed = (self.TargetL + self.TargetR)
                    RPM = avg_speed*600
                    m_s = RPM*np.pi*diameter/60
                    meter2 = m_s * 0.1 #measured every 0.1 second
                    self.straight = False
                    self.turnradius += meter2/5
                    self.get_logger().info('Publish position: "%f"' % self.total_meter)
                    self.total_meter =0
                    
                if self.turnradius>=0.23 and self.third: 
                    self.turning = False
                    self.TargetR= self.TargetL
                    if self.total_meter>=3.66: 
                        self.TargetL =0
                        self.TargetR =0
                        self.total_meter =0
    
    #Gets the speed from the user   
    def speed(self,msg):
        self.TargetL = msg.data[0]/10
        self.TargetR = msg.data[0]/10
        self.initialValue = msg.data[0]/10

    #Gets the stop command if there is an obstacle 
    def stop_callback(self,msg):
        #self.get_logger().info("command received(L): %d" % msg.data)
        self.stop = msg.data

    #Gets current RPM from the encoders
    def velocity_callback(self, msg):
        #self.get_logger().info('Publishing: "%d"' % msg.data[0]) 
        self.currentVelL = msg.data[0]
        self.currentVelR = msg.data[1]
       
    #Publishes the left motor speed 
    def motor_callbackL(self):
        msg = Float32()
        KP = 0.9
        KD = 0.25
        KI = 0.25
        msg.data = self.PID(self.TargetL, self.currentVelL,KP,KD,KI)
        self.leftMotor_.publish(msg)
        self.get_logger().info('Publishingleft: "%f"' % msg.data)  
        self.iL += 1

    #Published the right motor speed
    def motor_callbackR(self):
        msg = Float32()
        KP = 0.9
        KD = 0.25
        KI = 0.25
        msg.data = self.PID(self.TargetR, self.currentVelR,KP,KD,KI)
        self.rightMotor_.publish(msg)
        self.get_logger().info('PublishingRight: "%f"' % msg.data)  
        self.iR += 1

    #PID function for calculating the value of motor
    def PID(self,Target, currentVel,KP, KD, KI):
        TARGET = Target #m/s
       
        if self.stop == 1:
            m1_speed =0.0
        else:
            m1_speed = 0.0
            e1_prev_error = 0
            e1_sum_error = 0
            e1_error = TARGET - currentVel  
            m1_speed += (e1_error * KP) + (e1_prev_error * KD) + (e1_sum_error * KI)
            m1_speed = max(min(0.4, m1_speed), 0.00)
            e1_prev_error = e1_error 
            e1_sum_error += e1_error
    
        return m1_speed

def main(args=None):
    rclpy.init(args=args)

    two_motors = twoMotors()

    rclpy.spin(two_motors)
    
    two_motors.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

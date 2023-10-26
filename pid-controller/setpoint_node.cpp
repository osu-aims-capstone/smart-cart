/***************************************************************************/ 
 #include "ros/ros.h"
 #include "std_msgs/Float64.h"
 
 int main(int argc, char** argv)
 {
   ros::init(argc, argv, "setpoint_node");
   ROS_INFO("Starting setpoint publisher");
   ros::NodeHandle setpoint_node;
 
   while (ros::ok() && ros::Time(0) == ros::Time::now())
   {
     ROS_INFO("Setpoint_node spinning, waiting for time to become non-zero");
     sleep(1);
   }
 
   std_msgs::Float64 setpoint;
   setpoint.data = 1.0;
   ros::Publisher setpoint_pub = setpoint_node.advertise<std_msgs::Float64>("setpoint", 1);
 
   ros::Rate loop_rate(0.2);  // change setpoint every 5 seconds
 
   while (ros::ok())
   {
     ros::spinOnce();
 
     setpoint_pub.publish(setpoint);  // publish twice so graph gets it as a step
     setpoint.data = 0 - setpoint.data;
     setpoint_pub.publish(setpoint);
 
     loop_rate.sleep();
   }
 }

 /***************************************************************************/ 
 #include "ros/ros.h"
 #include "rosgraph_msgs/Clock.h"
 
 #include <sys/time.h>
 
 #define SIM_TIME_INCREMENT_US 10000
 
 /*
  * This node publishes increments of 1ms in time to the /clock topic. It does so
  * at a rate determined by sim_speedup (simulation speedup factor), which should
  * be passed
  * in as a private parameter.
  */
 
 int main(int argc, char** argv)
 {
   ros::init(argc, argv, "sim_time_source");
   ros::NodeHandle sim_time_node;
 
   // support integral multiples of wallclock time for simulation speedup
   int sim_speedup;  // integral factor by which to speed up simulation
   ros::NodeHandle node_priv("~");
   node_priv.param<int>("sim_speedup", sim_speedup, 1);
 
   // get the current time & populate sim_time with it
   struct timeval start;
   int rv = gettimeofday(&start, NULL);
   usleep(1000);
   struct timeval now;
   rv = gettimeofday(&now, NULL);
   if (0 != rv)
   {
     ROS_ERROR("Invalid return from gettimeofday: %d", rv);
     return -1;
   }
 
   rosgraph_msgs::Clock sim_time;
   sim_time.clock.sec = now.tv_sec - start.tv_sec;
   sim_time.clock.nsec = now.tv_usec * 1000;
   ros::Publisher sim_time_pub = sim_time_node.advertise<rosgraph_msgs::Clock>("clock", 1);
 
   ROS_INFO("Starting simulation time publisher at time: %d.%d", sim_time.clock.sec, sim_time.clock.nsec);
 
   while (ros::ok())
   {
     sim_time_pub.publish(sim_time);
 
     sim_time.clock.nsec = sim_time.clock.nsec + SIM_TIME_INCREMENT_US * 1000;
     while (sim_time.clock.nsec > 1000000000)
     {
       sim_time.clock.nsec -= 1000000000;
       ++sim_time.clock.sec;
     }
 
     usleep(SIM_TIME_INCREMENT_US / sim_speedup);
     ros::spinOnce();
   }
 }

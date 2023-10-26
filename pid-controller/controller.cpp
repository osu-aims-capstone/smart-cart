 /***************************************************************************/ 
 // Subscribe to a topic about the state of a dynamic system and calculate
 // feedback to
 // stabilize it.
 
 #include <pid/pid.h>
 
 int main(int argc, char** argv)
 {
   ros::init(argc, argv, "controller");
 
   pid_ns::PidObject my_pid;
 
   return 0;
 }

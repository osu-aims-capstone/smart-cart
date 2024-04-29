# Smartcart-AMR

The smartcart is designed to transport 200lbs of load to three locations from user input

## Description

The autonomous mobile robot (AMR) “Smart cart” is designed to transport materials in various industrial settings. With a payload capacity of more than 200 lbs., the smartcart can autonomously travel between designated locations. It is equipped with an obstacle detection system, precise speed control, and over three hours of continuous runtime on a single battery charge. The Smartcart is controlled by a Raspberry Pi 3A+, with ultrasonic sensors, quadrature encoders, and mechanical buttons for seamless operations. Additionally, the cart offers three predefined locations, and three adjustable speeds based on user preference. The software system is implemented with ROS2 communication protocol to ensure robustness and scalability. Additionally, ROS2 offers real-time capabilities and smooth integration with various hardware platforms.  

## Getting Started

### Dependencies

* ROS2-Humble
* Ubuntu - 22.04 LTS

### Installing

* Clone ros2_ws

### Executing program

* Go to the ros workspace launch directory:
```
cd ros2_ws/launch
```
* Source the terminal: 				
```
source install/setub.bash
```
* Initiate pigpio library: 				
```
sudo pigpiod
```
* Run the launch file: 				
```
ros2 launch smartcart.launch.py
```
#### User Interface:
* Press one of the three location buttons
* Press one of the three speed buttons
* If the cart needs to be stopped, press the emergency stop button.

#### Hardware:

If the motor drivers or 24V:5V converter are not connected: 

  * Disconnect the battery. 
  * Attach the V+ terminals of the motor drivers (white wires) and 24V:5V converter (red wire) to the 24V bus (white terminals). Tighten thoroughly. 
  * Connect the V- terminals of the motor drivers and 24V:5V converter (black wires) to the ground bus (black terminals). Tighten thoroughly.
    
To connect the battery: 
  * Attach the positive input of the 48V:24V converter (white wire, fused line) to the positive terminal of the battery (white terminal). Tighten thoroughly. 
  * Switch the anti-arc device to the ‘Connect’ Position. 
  * Attach the negative input of the 48V:24V converter (black wire, attached to anti-arc device) to the negative terminal of the battery (black terminal). Tighten thoroughly. 
  * After 30 seconds, switch the anti-arc device to the ‘Run’ position. Failure to do so before operation will reduce efficiency and may damage the anti-arc device. 

## Help

If the cart remains powered but unresponsive or the ultrasonic sensors stop working: 
  * Press the emergency stop button. 
  * Restart the Pi. 

If the cart loses power: 
  * Check the connections to the battery. 
  * Check the status of the fuse, replace if necessary. 
  * Verify the battery has a charge. 
  * Reconnect battery and restart the Pi. 

If one wheel loses power or exhibits unintended behaviors: 
  * Press the emergency stop button. 
  * Check the connection between motor driver and power bus. 
  * Verify motor driver power LED is lit. 
  * Check the connection between the Pi and the motor driver. 
  * Restart the Pi. 

To charge the battery: 
  * Disconnect the battery from the voltage converter. 
  * Remove the battery from the cart (optional). 
  * Connect the positive terminal (white) of the battery to the positive terminal of a 48V (nominal) power supply. Connect the negative terminal (black) to the negative terminal of the power supply. 
  * Charge until the battery is at 48V to 52V as measured by a multimeter. 
  * Disconnect the power supply and return the battery to the cart. 
  * Connect battery as described above. 

## Full Document

For full documentation refer: https://buckeyemailosu-my.sharepoint.com/:w:/r/personal/dudgeon_55_buckeyemail_osu_edu/Documents/4-Project_SmartCart/Team4_Final_Report.docx?d=w0211a511f0c642df9dbb135f3e812a7f&csf=1&web=1&e=KocE73 

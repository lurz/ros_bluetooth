# ROS-ANDROID BLUETOOTH COMMUNICATION PACKAGE
This is the ROS workspace to enable bluetooth communication with android phone. It uses RFCOMM serial port to send and receive message.
blue_sender.py receive fingerprint message from android phone, and publish topic to ROS to enable the Ros_bridge to resend the message 
to the controlling PC. blue_recer.py receive command message from controlling PC from Ros_bridge, then resend it back to android phone
using bluetooth.

## PACKAGE SETUP
    1. Make sure you have ROS system installed on your machine. For how to install ROS, please read tutorials on its website. Build this
    ROS workspace on your machine
        $ catkin_make
        $ source {workspace dir}/devel/setup.bash

    2. Enable password less sudo on your machine
        $ sudo visudo -f /etc/sudoers
        Append the following line to the file
            {username} ALL=(ALL) NOPASSWD:ALL
        Use `esc :wq!` to exit.

    3. Install bluez on your linux machine. Use the following commands:
        $ sudo apt-get update
        $ sudo apt-get install systemd
        $ cd ~
        $ wget http://www.kernel.org/pub/linux/bluetooth/bluez-5.37.tar.xz
        # other versions that > 5 is also ok.
        $ tar xvf bluez-5.37.tar.xz
        $ cd bluez-5.37
        $ sudo apt-get install -y libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev
        $ ./configure
        $ make
        $ sudo make install
        $ sudo apt-get install bluez-utils

        Also get blueman from official webpage.
    4. Edit config file of your bluetooth
        $ cd /etc/bluetooth
        Add `Enable=Source,Sink,Media,Socket` and `DisablePlugins = pnat` to the `main.conf` file after general.
        edit `rfcomm.conf`, add content like
        `rfcomm0 {
                bind no;
                device 1C:23:2C:06:6E:92;
                channel 22;
                comment "connect galaxy";
        }`

    5. 
        $ rosrun ros_bluetooth startbluenodes
        When the phone is connected, do
        $ roslaunch ros_bluetooth ros_bluetooth.launch

    6. If connection is lost, you may want to restart the android activity and restart the PC bluetooth service.
    Use `Ctrl-C` and `rosrun ros_bluetooth stopbluenodes` to stop the ros process completely. Then restart rfcomm
    listening and ros bluetooth package.

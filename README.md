# Flight Operating System (FOS)
- A micro ‘virtual operating system’.
- Enables autonomous determination, control and operation of the CubeSAT.
- Enables seamless shifting between the different modes of the satellite.
- Allows for communications with uplink and downlink capability.
- Allows for software patches to be sent.


## Changelog
- vAlpha - Triad, IGRF, MPU, PID and ESC code added. Some utils and tests added.
- v0.1 - Logging, Modes, Uplink/Downlink, Image Queueing and Shell capabilites added. Code structure better defined.

## Modules used
- pigpio
- numpy
- pyIGRF
- math
- datetime
- time
- signal
- logging


## Structure
```bash
.
├── communications/
├── config/
├── control_systems/
├── core/
├── determination/
├── tests/
├── modes/
├── unused/
├── fos.py
└── README.md
```



## Features

### UNIX Shell
**Subteam - CS**
- Allows access to the terminal on the flight computer.
- Can easily send patches, as shell and python scripts.
- Gives us a way to make changes to the satellite software in orbit, should anything go wrong.

*_Progress - Basic version completed, more features like custom commands could be added._*

### PID
**Subteam - CS**
- Widely in control systems of autonomous robots
- Helps in adjusting the satellite to account for unforseen variables and improve accuracy of control systems.

*_Progress - PID code needs to be verified and tuned._*


### Global Logging
**Subteam - CS**
-  One logging system throughout the OS
- Multiple levels of logging
- Logs will be sent with data packets and not stored permanently, helping free up memory.

*_Progress - Logging system is defined, needs to implemented throughout each class. Log flushing needs to be completed._*


### Uplink & Downlink Capability
**Subteam - CS, Electrical & ConOps**
- Interfaces with the flight computer and allows smooth transfer of data packets over the satellite antennas.
- Data Packets include telemetry data, logs, images, telemetry and messages. Each data packet estimated to be around 0.5 MB maximum.
- Uplink Capability to take in data from the ground and execute commands through the shell, or perform different functions

*_Progress - Downlink Capability needs to be coded with the flight computer. Need to figure out what do we exactly need to uplink, currently executes shell code._*


### Modes & Mode Switching
**Subteam - CS & ConOps**
- Different Modes for the different missions as well as control of the satellite
- Helps in autonomous decision making based on determination data and switching modes.
- Enables us to conduct multiple experiments like the Imaging and HDD testing autonomously.

*_Progress - Imaging Mode is defined, other modes need to be discussed, finalized and defined. Mode Switching needs to be thought of._*


### Autonomous Image Queueing
**Subteam - CS**
- Automatic queueing of images based on percentage of black pixels in the image.
- Ensures that the pictures with most of Earth in it to be sent first.

*_Progress - Code complete, and partially tested, needs to be integration tested._*

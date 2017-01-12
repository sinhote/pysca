# Pysca
    Copyright 2014 Rubén Pérez Vázquez
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

### Overview ###
Pysca is a purely-Python implementation of the [Sony Visca protocol](http://en.wikipedia.org/wiki/VISCA_Protocol). The protocol is primarily used in PTZ (**P**an, **T**ilt, **Z**oom) cameras, i.e. cameras that can be remotely steered and controlled using a RS-232 ("serial") port . The Visca standard covers not only positiioning and zooming, but also controlling many different camera parameters.

Other open-source implementations of the Visca protocol exist, most notably [libVISCA](http://damien.douxchamps.net/libvisca/). [PyVisca](https://github.com/mutax/PyVisca) is also a purely Python implementation of the Visca protocol, and appears to be inspire on the libVisca code, but at the time this document was written, it was nothing more than a proof-of-concept. 

Pysca differs from libVISCA in that it tries to create a pythonic API to Visca devices that abstract the users from the low-level details of the Visca protocol,  instead of simply create one method for each Visca command available.

Pysca was developed as a prerequisite to manage Visca devices from [Galicaster](http://galicaster.org). Galicaster is a great open, dual-stream recorder that is primarily designed to work with [Opencast Matterhorn](http://opencast.org/matterhorn/), a video processing platform.

#### State of development ####
**Pysca is currently in an ALPHA state**, so it is not guaranteed to be a complete or stable implementation of the protocol. In particular, it is still lacking most of the control commands, and all the query commands. However, the basic steering and zooming commands are still available.

##### Update 12-January-2017 #####

The synchronization logic has been simplified A LOT, but external API (the command methods) remain unchanged. The only (VERY IMPORTANT) difference is that now all the commands are non-blocking by default. Most commands (except `set_power_on`) accept now a `blocking` parameter at the end of their argument list -- when `blocking` is `True`, the command will block till it is completed (i.e. the old behaviour). `blocking` is now `False` by default -i.e. commands that receive an "ACK" return immediately even though they are not yet finished.

Please note that when a non-blocking command returns, it MIGHT be completed, as long as such command always returns a "COMPLETED" response (and not an ACK) after it is invoked.

However, all the frequently-used PTZ commands (i.e. those that move the camera or change its zoom) return an ACK when they start performing and a "COMPLETED" when they are done. These commands, among others, used to block until they were completed, but now they return immediately.

This means that potentially long-lasting instructions like:

```
pysca.recall_memory(1, 3)
```

will NOT be completed when they return, potentially causing the next commands to fail. As an example, the camera (at least the H-100S model) cannot be switched off while there are pending commands executing. Thus, in the following snippet:

```
pysca.pan_tilt_home(1, blocking=True)
pysca.pan_tilt(1, pan=1, pan_position=2000, tilt_position=0)
pysca.set_power_on(1, False)
```

, the third command will fail because it will be issued when the previous command is still running. However, in:

```
pysca.pan_tilt_home(1, blocking=True)
pysca.pan_tilt(1, pan=1, pan_position=2000, tilt_position=0, blocking=True)
pysca.set_power_on(1, False)
```

, the second command will block until is completed and therefore the 3rd command will succeed.

In other cases, it may happen that a command is interrupted by another (without raising an error). For instance, in the following snippet:

```
pysca.pan_tilt(1, pan=7, pan_position=2000, tilt_position=0)
pysca.pan_tilt(1, tilt=10, pan_position=0, tilt_position=10)
```

, the second command will interrupt the first immediately when it is issued.

### Get started ###

#### Access to the serial ports ####

##### Ubuntu #####
Regular uses cannot use the serial ports by default. You can either run the library as root, or add your user to the `dialout` group. After that, you need to restart your session for the change to apply. 

##### Other systems #####
Instructions to set up a regular user to use the serial port in other operating systems are welcome.


#### _Hello World_ example ####

The "Hello World" Pysca program would be something like:

    from pysca import pysca
    
    pysca.connect('/dev/ttyS0')
    pysca.set_power_on(1, True)
    pysca.set_power_on(1, False)

This snippet simply imports the library, connects to the serial port where the Visca device(s) is/are connected, and switches on and off the first device. 

Type `help(pysca)` to see a list of the available commands. 

### Dependencies ###

Pysca uses mostly libraries from the standard Python API. The only exception is [PySerial](http://pyserial.sourceforge.net/), which is used to access the RS-232 port. 

### Compatibility ###

Even though it is in an Alpha state, Pysca has been tested and known to work in __Ubuntu Linux__ and  __Python 2.7__.

The source code tries to follow the PySerial recommendations to deal with byte types, so it can be _theoretically_ be migrated to Python 3 without much effort, __but this has not been tested__.

### Configuration ###

No configuration is required for Pysca (apart from specifying the serial port to use using `connect`). However, the read timeout may be too long for some devices to start or perform certain operations. You can change the timeout by editing the variable `DEFAULT_TIMEOUT` at the beginning of the file.

Soon, there will be a different timeout for reading and for execution of instructions that will hopefully avoid these errors.

### Contributions ###

Pysca is licensed under the GPL3 . 

Bug reports, bug fixes, improvements and the likes are much appreciated.


### Author ###

Rubén Pérez Vázquez ([ruben.perez@uni-koeln.de](mailto:ruben.perez@uni-koeln.de))

This library was done as part of my work in the [_Regionales Rechenzentrum_](http://rrzk.uni-koeln.de/) at the [University of Cologne](http://www.portal.uni-koeln.de/uoc_home.html?&L=1)
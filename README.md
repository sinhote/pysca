To activate this plugin:

1. Copy the `visca.py` into the `plugins` folder in your Galicaster installation.
2. Copy the `pysca.py` file that is into the `pysca` folder of this repo inside the `utils` folder in your Galicaster installation.
3. Add the line marked with an arrow below to the `[plugins]` section of your `conf.ini` file:
        
        [plugins]
        # ...
        visca=True  # <---- Add this line

4. Add the following section in your `conf.ini` file, using your own system values:

        [visca]
        # The port (i.e. path to the system device) where the Visca device(s) are connected
        # (Mandatory)
        port=/dev/ttyS0
        
        # The preset that the camera will be set to, just before starting the recording
        # (Optional. Defaults to 0 -that is the preset 1 in the remote control-)
        record-preset=0
        
        # The preset that the camera will be set to, right after the recording is finished
        # (Optional. Defaults to 5 -that is the preset 6 in the remote control-)
        idle-preset=5

5. The plugin should be now ready to use


Please note:

* A Visca device should be plugged into the configured serial port when Galicaster is started --otherwise the plugin will fail to initialize
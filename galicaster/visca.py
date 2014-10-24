"""This plugin is a test to see if the signals work"""

from galicaster.core import context
import time
import galicaster.utils.pysca as pysca

# This is the default Visca device this plugin talks to
DEFAULT_DEVICE = 1

# This is the default preset to set when the camera is recording
DEFAULT_RECORD_PRESET = 0

# This is the default preset to set when the camera is switching off
DEFAULT_IDLE_PRESET = 5

# This is the name of this plugin's section in the configuration file
CONFIG_SECTION = "visca"

# This is the key containing the port (path to the device) to use when recording
PORT_KEY = "port"

# This is the key containing the preset to use when recording
RECORD_PRESET_KEY = 'record-preset'

# This is the key containing the preset to set the camera to just after switching it off
IDLE_PRESET_KEY= 'idle-preset'




def init():
    global logger

    logger = context.get_logger()

    # If port is not defined, a None value will make this method fail
    pysca.connect(context.get_conf().get(CONFIG_SECTION, PORT_KEY))

    dispatcher = context.get_dispatcher()
    dispatcher.connect('starting-record', on_start_recording)
    # We don't have such thing as a "post-stop" signal, so we have to live with what we do have
    dispatcher.connect('restart-preview', on_stop_recording)

def on_start_recording(elem):

    global logger

    # Get a shallow copy of this plugin's configuration
    config = context.get_conf().get_section(CONFIG_SECTION) or {}

    try: 
        pysca.set_power_on(DEFAULT_DEVICE, True)
        pysca.recall_memory(DEFAULT_DEVICE, config.get(RECORD_PRESET_KEY, DEFAULT_RECORD_PRESET))
        
    except Exception as e:
        logger.warn("Error accessing the Visca device %u on recording start. The recording may be incorrect! Error: %s" % (DEFAULT_DEVICE, e))


def on_stop_recording(elem):
    
    global logger

    # Get a shallow copy of this plugin's configuration
    config = context.get_conf().get_section(CONFIG_SECTION) or {}

    try:
        pysca.recall_memory(DEFAULT_DEVICE, config.get(IDLE_PRESET_KEY, DEFAULT_IDLE_PRESET))
        pysca.set_power_on(DEFAULT_DEVICE, False)
    except Exception as e:
        logger.warn("Error accessing the Visca device %u on recording end. The recording may be incorrect! Error: %s" % (DEFAULT_DEVICE, e))

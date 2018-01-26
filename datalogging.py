from config import get_config
from config import has_config
from thingspeak import post_to_thingspeak_channel
from trace import trace
from trace import INFO 

# =============================================================================
# Logging
# =============================================================================
def log(measurements):

    if(not has_config("logging")):
        trace("no logging", INFO)

    logging = get_config("logging")
    
    if "trace" in logging:
        trace(measurements, logging["trace"]["level"])

    if "thingspeak" in logging:
        post_to_thingspeak_channel(measurements, logging["thingspeak"]["channel_key"])
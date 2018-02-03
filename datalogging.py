from config import get_config
from config import has_config
from thingspeak import post_thingspeak_channel_update
from trace import trace
from trace import INFO 

# =============================================================================
# Logging
# =============================================================================
def log(measurements):

    if(not has_config("logging")):
        trace("no logging", INFO)
        return

    logging = get_config("logging")
    
    if "trace" in logging:
        trace(measurements, logging["trace"]["level"])

    if "thingspeak" in logging:
        post_thingspeak_channel_update(measurements, logging["thingspeak"]["channel_key"])
import urllib
import httplib
import sys 
from trace import trace
from trace import INFO
from trace import WARN
from trace import ERROR

# =============================================================================
# Send to Thingspeak
# =============================================================================
# channel_key : Write key for thingspeak channel
# sensor_measurement : array of dictionaries with keys: "field" and "value" 
def post_to_thingspeak_channel(sensor_measurement, channel_key):
    param_dict = {}
    for measurement in sensor_measurement:
        param_dict[measurement["field"]] = measurement["value"]
    param_dict["key"] = channel_key

    params = urllib.urlencode(param_dict)
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPSConnection("api.thingspeak.com")                
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        data = response.read()
        if response.status == 200:
            trace(["Success", response.reason, data], INFO)
        else:
            trace(["Failed", response.status, response.reason, data], WARN)
        conn.close()
    except:
        trace("Sending to Thingspeak failed", ERROR)
        trace(str(sys.exc_info()), WARN)

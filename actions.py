from config import get_config
from config import has_config
import datalogging
from trace import trace

# =============================================================================
# Actions
# =============================================================================
def run_actions(measurements):
    
    if(not has_config("actions")):
        trace("no actions", datalogging.INFO)
        return
    
    val = {"field1" : None, 
           "field2" : None, 
           "field3" : None, 
           "field4" : None, 
           "field5" : None, 
           "field6" : None, 
           "field7" : None, 
           "field8" : None}
    for measurement in measurements:
        val[measurement["field"]] = measurement["value"]
           
    actions = get_config("actions")
    for action in actions:
        if eval(action["condition"]):
            if action["type"] == "TRACE":
                trace(measurement, action["level"])

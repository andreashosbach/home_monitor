from datetime import datetime
import sys

# =============================================================================
# Write a formatted trace line
# =============================================================================
def trace(line):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - " + str(line))
    sys.stdout.flush()

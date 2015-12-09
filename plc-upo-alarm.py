import shlex
import sys
import re
from subprocess import Popen, PIPE

def extractMacAddress(ampStatLine):
    macAddr = None
    items = ampStatLine.split( " " )
    for index in range(len(items)):
        if (items[index] == "MAC") and ((index+1) < len(items)):
            if re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", items[index+1].lower()):
                return items[index+1]
    return macAddr

device = "eth0"
if len(sys.argv) > 1:
    device = sys.argv[1]

cmd = "ampstat -m -i {}".format(device)
process = Popen(shlex.split(cmd), stdout=PIPE)
(output, err) = process.communicate()
exit_code = process.wait()

allowedMacAddrMap = dict()

outputArray = output.splitlines()
for entries in outputArray:
    macAddr = extractMacAddress(entries)
    if macAddr is not None:
        # Check if mac address is allowed on the network
        print macAddr




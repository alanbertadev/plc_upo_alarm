import shlex
import sys
import re
from subprocess import Popen, PIPE
import argparse
from sets import Set
import boto.sns


def isNotBlank(myString):
    if myString and myString.strip():
        return True
    return False


def extractMacAddress(ampStatLine):
    macAddr = None
    items = ampStatLine.split(" ")
    for index in range(len(items)):
        if (items[index] == "MAC") and ((index+1) < len(items)):
            if re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", items[index+1].lower()):
                return items[index+1]
    return macAddr


def publishToSnsTopic(allowedMacAddresses, invasiveMacAddresses, topicARN, topicRegion):
    if isNotBlank(topicARN):
        print "sending alert sns to topic ARN({})".format(topicARN)
        message = """
Intruder detected!
The EoP network contains unidentified powerline object(s): {}""".format(invasiveMacAddresses)
        conn = boto.sns.connect_to_region(topicRegion)
        pub = conn.publish(topic=topicARN, message=message)
    else:
        print "unable to send alert sns because of blank topic ARN!"


def start():
    parser = argparse.ArgumentParser(
        description='Check a set of valid mac addresses against an EoP (Ethernet over Powerline) network and alert an optional email if an intruder is present')
    parser.add_argument(
        '-i', help='active network interface with proximity to an EoP device (default: eth0)', default="eth0")
    parser.add_argument(
        '--arn', help='AWS SNS topic ARN to notify of unidentified powerline objects', default="")
    parser.add_argument(
        '--region', help='AWS region that contains the given topic (default: us-east-1)', default="us-east-1")
    parser.add_argument(
        '--macs', nargs='+', help='one or more mac addresses that are allowed to be on the EoP network', default=[])

    args = parser.parse_args()
    device = args.i
    alertSNS = args.arn
    alertRegion = args.region
    validMacAddresses = args.macs

    cmd = "ampstat -m -i {}".format(device)
    process = Popen(shlex.split(cmd), stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

    detectedMacAddresses = []

    outputArray = output.splitlines()
    for entries in outputArray:
        macAddr = extractMacAddress(entries)
        if macAddr is not None:
            # Check if mac address is allowed on the network
            intruderDetected = False
            if macAddr in validMacAddresses:
                print "{}".format(macAddr)
            else:
                detectedMacAddresses.append(macAddr)
                print "{} <-- INTRUDER DETECTED".format(macAddr)
                intruderDetected = True

    if intruderDetected:
        publishToSnsTopic(
            validMacAddresses, detectedMacAddresses, alertSNS, alertRegion)


if __name__ == "__main__":
    start()

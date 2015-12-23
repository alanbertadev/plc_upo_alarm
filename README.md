# Ethernet over Powerline - Unidentified Powerline Object Alarm

This script is a monitoring tool in reaction to the following vulnerability in most ethernet over powerline adapters:
https://www.bentasker.co.uk/documentation/security/282-infiltrating-a-network-via-powerline-homeplugav%20-adapters

The vulnerability allows attackers to gain access to a powerline network. The attack can be detected by monitoring the EoP network with a whitelisted set of mac addresses. The following script can be run periodically (via CRON or other means) and will notify an AWS SNS service of an intruder with each detection. Subscribers to the AWS SNS service can take necessary precautions (ex. An Arduino triggering a relay to shut off network access to the EoP network).

** Note ** This is a work-around and is not ideal.

Requirements
-----------
* [boto 2.38.0](https://pypi.python.org/pypi/boto/)
* Compiled and installed copy of [open-plc-utils](https://github.com/qca/open-plc-utils). This is provided as a submodule in the plc_upo_alarm repository.
* An AWS account with a properly configured [SNS Topic](http://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html)

Installation
-----------
```
cd plc_upo_alarm
python setup.py install
```

Usage
-----------
```
plc-upo-alarm -h
usage: plc-upo-alarm [-h] [-i I] [--arn ARN] [--region REGION]
                     [--macs MACS [MACS ...]]

Check a set of valid mac addresses against an EoP (Ethernet over Powerline)
network and alert an optional email if an intruder is present

optional arguments:
  -h, --help            show this help message and exit
  -i I                  active network interface with proximity to an EoP
                        device (default: eth0)
  --arn ARN             AWS SNS topic ARN to notify of unidentified powerline
                        objects
  --region REGION       AWS region that contains the given topic (default: us-
                        east-1)
  --macs MACS [MACS ...]
                        one or more mac addresses that are allowed to be on
                        the EoP network
```

Example:
```
plc-upo-alarm -i eth0 --arn arn:aws:sns:us-east-1:<your topic id>:<topic name> --region us-east-1 --macs C5:E9:84:5E:C1:81 C4:E9:88:5E:8A:B4
```


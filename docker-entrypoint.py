import json
from requests import get
from os import getenv
import socket
import sys
from time import sleep

this_host = socket.gethostname()

if __name__ == '__main__':

  print('Starting up')

  node_name = getenv('NODE_NAME')

  print('Watching for termination notice on node %s' % node_name)

  counter = 0

  while(True):

    response = get(
      "http://169.254.169.254/metadata/scheduledevents?api-version=2017-11-01",
      headers={'Metadata': 'true'}
    )

    if response.status_code == 200:
      data = response.json()

      for evt in data['Events']:
          eventid = evt['EventId']
          status = evt['EventStatus']
          resources = evt['Resources']
          eventtype = evt['EventType']
          resourcetype = evt['ResourceType']
          notbefore = evt['NotBefore'].replace(" ","_")

          if this_host in resources:
              print("+ Scheduled Event. This host " + this_host + " is scheduled for " + eventtype + " not before " + notbefore)

              # time we have for drain is depending on event (https://docs.microsoft.com/en-us/azure/virtual-machines/linux/scheduled-events)
              # in case of Preempt just 30 secs
              kube_command = ['kubectl', 'drain', node_name,
                              '--grace-period=0', '--force',
                              '--ignore-daemonsets']

              print("Draining node: %s" % node_name)
              result = call(kube_command)
              if (result == 0):
                  print('Node Drain successful')
                  break

    if counter == 60:
        counter = 0
        print("Scheduled events status: %s, on Node: %s" %
              (response.status_code, node_name))

    counter += 5
    sleep(5)

  sys.exit(0)
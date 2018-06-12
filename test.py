import csv
import math
from flask import Flask, render_template, Markup
from lxml import etree

#Parses the scan log and orders the data into a list
port = None
address = None
parsedServers = {}

#Iterates through the masscan XML file. Filters duplicates and stores IP's in dict with accompianing ports.
for event, element in etree.iterparse('output.xml', tag="host"):
    for child in element:
        if child.tag == 'address':
            ipAddress = child.attrib['addr']
        if child.tag == 'ports':
            for subChild in child:
                port = [subChild.attrib['portid']]

    if ipAddress in parsedServers:
        print(ipAddress)
        #print(port)
        #print(parsedServers[ipAddress])
        if parsedServers[ipAddress] == None:
            parsedServers[ipAddress] = [port]
        else:
            parsedServers[ipAddress] = parsedServers[ipAddress].append(port)
    else:
        parsedServers[ipAddress] = [port]
print(parsedServers)


#There should be 40 unique IP's





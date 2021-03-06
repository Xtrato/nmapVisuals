#Tool used to create a visual representation on nmap and masscan outputs.

import math
from flask import Flask, render_template, Markup
from lxml import etree
import collections

#Constructor
port = None
address = None
parsedServers = collections.OrderedDict()



#Finds the IP Range
#Parses log file and populated ipList,
ipList = []
for event, element in etree.iterparse('output.xml', tag="host"):
    for child in element:
        if child.tag == 'address':
            ipList.append(child.attrib['addr'])


#iterates through ipList splits each IP into octets
firstOctetRange = []
secondOctetRange = []
thirdOctetRange = []
forthOctetRange = []
bitDelimeter = 0
startingIP = 0
endingIP = 0
for ip in ipList:
    binaryOctet = ''
    octets = ip.split('.')
    firstOctetRange.append(int(octets[0]))
    secondOctetRange.append(int(octets[1]))
    thirdOctetRange.append(int(octets[2]))
    forthOctetRange.append(int(octets[3]))

#calculates the octet where the IP address changes and saves value in bitDelimeter
if min(firstOctetRange) != max(firstOctetRange):
    bitDelimeter = 0
elif min(secondOctetRange) != max(secondOctetRange):
    bitDelimeter = 1
elif min(thirdOctetRange) != max(thirdOctetRange):
    bitDelimeter = 2
elif min(forthOctetRange) != max(forthOctetRange):
    bitDelimeter = 3


#Creates a ordered Dict which contains all IP addresses in the range taken from the log file.
if bitDelimeter == 0:
    for one in range(min(firstOctetRange), max(firstOctetRange) + 1):
        for two in range(0, 256):
            for three in range(0, 256):
                for four in range(0, 256):
                    ip = "%d.%d.%d.%d" % (one, two, three, four)
                    parsedServers[ip] = []
if bitDelimeter == 1:
    one = min(firstOctetRange)
    for two in range(min(secondOctetRange), max(secondOctetRange) + 1):
        for three in range(0, 256):
            for four in range(0, 256):
                ip = "%d.%d.%d.%d" % (one, two, three, four)
                parsedServers[ip] = []
if bitDelimeter == 2:
    one = min(firstOctetRange)
    two = min(secondOctetRange)
    for three in range(min(thirdOctetRange), max(thirdOctetRange) + 1):
        for four in range(0, 256):
            ip = "%d.%d.%d.%d" % (one, two, three, four)
            parsedServers[ip] = []
if bitDelimeter == 3:
    one = min(firstOctetRange)
    two = min(secondOctetRange)
    three = min(thirdOctetRange)
    for four in range(min(forthOctetRange), max(forthOctetRange) + 1):
            ip = "%d.%d.%d.%d" % (one, two, three, four)
            parsedServers[ip] = []



#Iterates through the masscan XML file. Filters duplicates and adds the ports to parsedServers orderedDict.
for event, element in etree.iterparse('output.xml', tag="host"):
    for child in element:
        if child.tag == 'address':
            ipAddress = child.attrib['addr']
        if child.tag == 'ports':
            for subChild in child:
                port = [subChild.attrib['portid']]
        parsedServers[ipAddress].append(port)



app = Flask(__name__)


count = 0
htmlBuffer = Markup('')
#Iterates through the IP range that was scanned into paesedServers dict. creates an infoString on each iteration containing the IP and open ports.
#This is then appeneded into a htmlBuffer within a HTML table and passed to render_template to generate the page through flask.
for key, value in parsedServers.items():
    infoString = str(key) + '<br>'
    if value:
        infoString += 'Ports:'
        for portValue in value:
            infoString += str(portValue) + ','
    colourRange = ['94A5FF', '0024E5', '2422C5', '4821A6', '6D1F87', '911E67', 'B61C48', 'DA1B29', 'FF1A0A']
    htmlBuffer += Markup('<td class="tooltip", bgcolor="' + colourRange[len(value)] + '"><span class="tooltiptext">' + infoString + '</span></td>')
    count += 1
    if count > math.sqrt(len(parsedServers)):
        htmlBuffer += Markup('</tr><tr>')
        count = 0

@app.route('/')
def index():
    return render_template('index.html', name=htmlBuffer)

if __name__ == '__main__':
    app.run()
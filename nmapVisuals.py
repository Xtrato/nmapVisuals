#Tool used to create a visual representation on nmap and masscan outputs.

import csv
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

#Calculates the range of ports on devices. Used to produce the heatmap.
upperServiceRange = 0
for key, value in parsedServers.items():
    if upperServiceRange < len(value):
        upperServiceRange = len(value)


count = 0
print(math.sqrt(len(parsedServers)))
htmlBuffer = Markup('')



for key, value in parsedServers.items():
    if len(value) < 2:
        htmlBuffer += Markup('<td height="5", width="5", class="tooltip", bgcolor="9fd1ff"><span class="tooltiptext">' + str(key) + '</span></td>')
    if len(value) == 2:
        htmlBuffer += Markup('<td height="5", width="5", class="tooltip", bgcolor="fff99f"><span class="tooltiptext">' + str(key) + '</span></td>')
    if len(value) > 2:
        htmlBuffer += Markup('<td height="5", width="5", class="tooltip", bgcolor="ff9f9f"><span class="tooltiptext">' + str(key) + '</span></td>')
    count += 1
    if count > math.sqrt(len(parsedServers)):
        htmlBuffer += Markup('</tr><tr>')
        count = 0

@app.route('/')
def index():
    return render_template('index.html', name=htmlBuffer)

if __name__ == '__main__':
    app.run()


###NOTES masscan 84.45.0.0/21 --top-ports 200 -oX test.xml
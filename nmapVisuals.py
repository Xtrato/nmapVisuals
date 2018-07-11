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
        portList = parsedServers[ipAddress]
        portList.append(port)
        parsedServers[ipAddress] = portList
    else:
        parsedServers[ipAddress] = [port]


app = Flask(__name__)


#Calculates the range of ports on devices. Used to produce the heatmap.
upperServiceRange = 0
for key, value in parsedServers.items():
    if upperServiceRange < len(value):
        upperServiceRange = len(value)


#Finds the IP Range
firstOctetRange = []
secondOctetRange = []
thirdOctetRange = []
forthOctetRange = []
bitDelimeter = 0
startingIP = 0
endingIP = 0
for key in parsedServers.items():
    binaryOctet = ''
    octets = key[0].split('.')
    firstOctetRange.append(int(octets[0]))
    secondOctetRange.append(int(octets[1]))
    thirdOctetRange.append(int(octets[2]))
    forthOctetRange.append(int(octets[3]))
if min(firstOctetRange) != max(firstOctetRange):
    bitDelimeter = 0
elif min(secondOctetRange) != max(secondOctetRange):
    bitDelimeter = 1
elif min(thirdOctetRange) != max(thirdOctetRange):
    bitDelimeter = 2
elif min(forthOctetRange) != max(forthOctetRange):
    bitDelimeter = 3

if bitDelimeter == 0:
    for one in range(min(firstOctetRange), max(firstOctetRange)):
        for two in range(0, 256):
            for three in range(0, 256):
                for four in range(0, 256):
                    ip = "%d.%d.%d.%d" % (one, two, three, four)
                    print(ip)
if bitDelimeter == 1:
    one = min(firstOctetRange)
    for two in range(min(secondOctetRange), max(secondOctetRange)):
        for three in range(0, 256):
            for four in range(0, 256):
                ip = "%d.%d.%d.%d" % (one, two, three, four)
                print(ip)
if bitDelimeter == 2:
    one = min(firstOctetRange)
    two = min(secondOctetRange)
    for three in range(min(thirdOctetRange), max(thirdOctetRange)):
        for four in range(0, 256):
            ip = "%d.%d.%d.%d" % (one, two, three, four)
            print(ip)
if bitDelimeter == 3:
    one = min(firstOctetRange)
    two = min(secondOctetRange)
    three = min(thirdOctetRange)
    for four in range(min(forthOctetRange), max(forthOctetRange)):
            ip = "%d.%d.%d.%d" % (one, two, three, four)
            print(ip)

print(firstOctetRange)
print(secondOctetRange)
print(thirdOctetRange)
print(forthOctetRange)

count = 0

print(math.sqrt(len(parsedServers)))
htmlBuffer = Markup('')

for key, value in parsedServers.items():
    if len(value) < 2:
        htmlBuffer += Markup('<td bgcolor="9fd1ff">' + str(key) + '</td>')
    if len(value) == 2:
        htmlBuffer += Markup('<td bgcolor="fff99f">' + str(key) + '</td>')
    if len(value) > 2:
        htmlBuffer += Markup('<td bgcolor="ff9f9f">' + str(key) + '</td>')
    count += 1
    #if count > int(math.sqrt(len(parsedServers))):
    if count > 6:
        htmlBuffer += Markup('</tr><tr>')
        count = 0

@app.route('/')
def index():
    return render_template('index.html', name=htmlBuffer)

if __name__ == '__main__':
    app.run(debug = True)
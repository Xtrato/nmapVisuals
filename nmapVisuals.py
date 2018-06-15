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
splitValue = 5
binaryList = []
for key in parsedServers.items():
    binaryOctet = ''
    octets = key[0].split('.')
    for octet in octets:
        binaryOctet += format(int(octet), '008b')
    binaryList.append(binaryOctet)


print(binaryList[0][0])
found = False
lastIteration = binaryList[0][0]
for bitIndex in range(32):
    for address in binaryList:
        if address[bitIndex] != lastIteration:
            bitDelimeter = bitIndex
            found = True
            break
    if found:
        break
        lastIteration = address[bitIndex]


print('################')
print(bitDelimeter)
print('################')

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
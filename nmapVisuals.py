import csv
import math
from flask import Flask, render_template, Markup
from lxml import etree

#Parses the scan log and orders the data into a list
port = None
address = None
parsedServers = []
#Iterates through the masscan XML file.
for event, element in etree.iterparse('output.xml', tag="host"):
    for child in element:
        if child.tag == 'address':
            #Assigns the current iterations address to the address variable.
            exists = False
            for entry in parsedServers:
                if child.attrib['addr'] in entry:
                    exists = True
            parsedServers.append([child.attrib['addr'], 'port', 'port'])
        if child.tag == 'ports':
            for a in child:
                pass
print(parsedServers)
app = Flask(__name__)


upperServiceRange = 0
#get the port open per serice. If more than upperServiceRange then ports = upperServiceRange




count = 1

with open('data.csv', 'r') as csvfile:

    reader = csv.reader(csvfile)
    your_list = list(reader)

print(math.sqrt(len(your_list)))
htmlBuffer = Markup('')

for entry in your_list:
    if '1' in entry[1]:
      if count > int(math.sqrt(len(your_list))):
        count = 0
        htmlBuffer += Markup('<td>1 END</td></tr><tr>')
      else:
          htmlBuffer += Markup('<td>1</td>')
    else:
      if count > int(math.sqrt(len(your_list))):
        count = 0
        htmlBuffer += Markup('<td>0 END</td></tr><tr>')
      else:
          htmlBuffer += Markup('<td>0</td>')
    count = count + 1

@app.route('/')
def index():
    return render_template('index.html', name=htmlBuffer)

if __name__ == '__main__':
    app.run()
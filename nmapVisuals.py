import csv
import math
from sty import fg, bg, ef, rs

count = 1

with open('data.csv', 'r') as csvfile:

    reader = csv.reader(csvfile)
    your_list = list(reader)

print(math.sqrt(len(your_list)))


for entry in your_list:
    if '1' in entry[1]:
      if count > int(math.sqrt(len(your_list))):
        print(bg.red + ' ' + fg.rs)
        count = 0
      else:
        print(bg.red + ' ' + fg.rs,end=" ")
    else:
      if count > int(math.sqrt(len(your_list))):
        print(bg.blue + ' ' + fg.rs)
        count = 0
      else:
        print(bg.blue + ' ' + fg.rs,end=" ")
    count = count + 1
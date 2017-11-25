#!/usr/bin/env python
from urllib import request
import sys, re
xml = request.urlopen('http://data.alexa.com/data?cli=10&dat=s&url=%s'%sys.argv[1]).read().decode("utf-8")
sp = re.search(r'REACH RANK="\d+"', xml).span()
print(int(xml[sp[0]+12:sp[1]-1]))

# try: rank = int(re.search(r'\d+', xml).groups()[0])
# except: rank = -1
# print('Your rank for %s is %d!\n' % (sys.argv[1], rank))

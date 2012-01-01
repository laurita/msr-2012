from xml.dom.minidom import parseString

f = open('/Users/laura/Sandbox/msr-2012/data/android_platform_bugs.xml', 'r')
bug = ''
for line in f:
    line = line.rstrip()
    if (line == '<bug>'):
        bug = line
    elif (line == '</bug>'):
        bug += line
        #dom = parseString(bug)  
        xml = bug
        break   
    else:
        bug += line
 

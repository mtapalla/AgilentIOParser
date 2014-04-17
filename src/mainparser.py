'''
Created on Apr 17, 2014

@author: Marc Tapalla
'''

import xml.etree.ElementTree as ET
import binascii

def GetTraceList():
    tree = ET.parse('../resources/IOMonitorLog.xml')
    root = tree.getroot()
    
    for child in root.iter('TraceList'):
        return list(child)
    
def ExtractBinaryData(child):
    for subchild in child.iter('Parameter'):
        if (('buf' not in subchild.get('Name'))): continue
         
        for subsubchild in subchild.iter('Element'):
            if ('BinHexValue' not in subsubchild.attrib): continue
            return subsubchild.attrib['BinHexValue']

if __name__ == '__main__':
    
    ParseRead = False
    
    for child in GetTraceList():
        
        BinaryData = ""

        if (ParseRead):
            ParseRead = False
            BinaryData = ExtractBinaryData(child)
        
        if ("viWrite" in child.get('MethodName')):
            print(child.get('MethodName'))
            BinaryData = ExtractBinaryData(child)
    
        if ("viRead" in child.get('MethodName')):
            print(child.get('MethodName'))
            ParseRead = True
            continue

        if (BinaryData is ""): continue

        print(child.get('Address'))
        try:
            AsciiData = binascii.b2a_qp(binascii.unhexlify(BinaryData))  
            Output = "Data: %s" % AsciiData.decode('utf-8')
            if (not Output.endswith("\n")): Output = Output + "\n"
            print(Output)
        except:
            print("* Error parsing. Incorrect command?\n")
            continue


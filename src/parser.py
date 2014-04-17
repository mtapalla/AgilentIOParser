'''
Created on Apr 17, 2014

@author: Marc Tapalla
'''

import xml.etree.ElementTree as ET
import binascii

def GetTraceList():
    tree = ET.parse('IOMonitorLog.xml')
    root = tree.getroot()
    
    for child in root.iter('TraceList'):
        return list(child)
    
def ExtractBinaryData(child):
    for subchild in child.iter('Parameter'):
        if (('buf' not in subchild.get('Name'))): continue
        if (subchild.get('ParamType') is 'pointer32'): return None
         
        for subsubchild in subchild.iter('Element'):
            if ('BinHexValue' not in subsubchild.attrib): continue
            return subsubchild.attrib['BinHexValue']

if __name__ == '__main__':
    
    IsParsingRead = False
    IsBinBlock = False
    Output = ""
    
    OutputLog = open("Output.txt", "w")
    OutputExcel = open("Output.xls", "w")
    
    for child in GetTraceList():
        
        CurrentBinaryData = ""
        if (IsBinBlock == False): Output = "" # Reset 'Output' if we're not accumulating binblock data

        if ("viWrite" in child.get('MethodName')): CurrentBinaryData = ExtractBinaryData(child)
        if (IsParsingRead): CurrentBinaryData = ExtractBinaryData(child)
    
        if ("viRead" in child.get('MethodName')):
            if (IsBinBlock == False):
                IsParsingRead = True
                continue

        if (CurrentBinaryData is None or CurrentBinaryData is ""): continue

        # Convert data from Binary to ASCII
        CurrentAsciiData = binascii.b2a_qp(binascii.unhexlify(CurrentBinaryData))
        Output = Output + CurrentAsciiData.decode('utf-8')

        if (CurrentAsciiData.decode('utf-8') == "#"):
            IsBinBlock = True

        # Done accumulating BinBlock data?
        if (CurrentAsciiData.decode('utf-8') == "\n"):
            IsBinBlock = False
            IsParsingRead = False
        
        # If we're accumulating BinBlock data, we don't want to print just yet
        if (IsBinBlock): continue
        
        # Output the Data
        Output  = Output.replace('\n', '')
        print("%s\n%s\n%s\n" % (child.get('Address'),child.get('MethodName'), Output))
        OutputLog.write("%s\n%s\n%s\n\n" % (child.get('Address'),child.get('MethodName'), Output))
        OutputExcel.write("{}\t{}\t{}\n".format(child.get('Address'),child.get('MethodName'), Output))

    OutputLog.close()
    OutputExcel.close()
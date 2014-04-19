'''
My VERY first Python script ever,
a.k.a. my take on Hello World,
a.k.a. proper programming practice was ignored :]

Created on Apr 17, 2014

@author: Marc Tapalla
'''

import xml.etree.ElementTree as ET
import binascii
import struct

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

def Binblock2Ascii(binblock):
    UnpackFormat = ">"
    numberOfExpectedBytes = int(len(binblock) / 4)
    for _ in range(0, numberOfExpectedBytes):
        UnpackFormat = UnpackFormat + "f"
        
    return str(struct.unpack_from(UnpackFormat, binblock))

if __name__ == '__main__':
    
    ParsingRead = False
    
    OutputLog = open("Output.txt", "w")
    OutputExcel = open("Output.xls", "w")
    
    ScpiTypeList = []
    ScpiInstrumentList = []
    ScpiDataList = []
    
    for child in GetTraceList():
        
        CurrentBinaryData = None

        if ("viWrite" in child.get('MethodName')):
            CurrentBinaryData = ExtractBinaryData(child)
            ScpiTypeList.append("Write")
            ScpiInstrumentList.append(child.get('Address'))
            
        if (ParsingRead):
            CurrentBinaryData = ExtractBinaryData(child)
            ParsingRead = False
            
        if ("viRead" in child.get('MethodName')):
            ParsingRead = True
            ScpiTypeList.append("Read")
            ScpiInstrumentList.append(child.get('Address'))
            
        if (CurrentBinaryData == None or CurrentBinaryData == ""): continue

        # XML file stores data in binary. Convert data to ASCII
        EncodedAsciiData = binascii.b2a_qp(binascii.unhexlify(CurrentBinaryData))
        DecodedAsciiData = EncodedAsciiData.decode('utf-8').rstrip()
        ScpiDataList.append(DecodedAsciiData)

    if (len(ScpiTypeList) != len(ScpiDataList)):
        print("* Error parsing list: ScpiTypeList.size != ScpiDataList.size")
        quit()
        
    if (len(ScpiTypeList) != len(ScpiInstrumentList)):
        print("* Error parsing list: ScpiTypeList.size != ScpiInstrumentList.size")
        quit()

    # Parse the extracted data, including data returned as binary blocks
    AccumulatedScpiTypeList = []
    AccumulatedScpiDataList = []
    AccumulatedScpiInstrumentList = []
    for i in range(0, len(ScpiTypeList)):
        
        # Incoming binblock data detected
        # Example binblock string: "#220[binblock]"
        # The pound sign '#' indicates start of binblock datastream
        # The next digit, '2', indicates the following '2' digits is
        # the number of incoming bytes, '20'.
        # This tells us there will be '20' bytes in [binblock]
        if (ScpiTypeList[i] == "Read" and ScpiTypeList[i - 1] != "Read" and ScpiDataList[i].startswith('#')):
            UnparsedBinblockData = ScpiDataList[i]
            UnparsedBinblockData = UnparsedBinblockData[1:]  # Delete out the '#' sign from the concatenated string
            numberOfDigitsIncomingBytes = int(UnparsedBinblockData[0])  # Number of incoming binblock bytes
            numberOfExpectedBytes = int(UnparsedBinblockData[1:numberOfDigitsIncomingBytes + 1])  # Expec
            UnparsedBinblockData = UnparsedBinblockData[numberOfDigitsIncomingBytes + 1:]  # Delete out the 'number of bytes' that follow the '#' sign from the string
            
            AccumulatedScpiTypeList.append("Binblock Read")
            AccumulatedScpiDataList.append(UnparsedBinblockData)
            AccumulatedScpiInstrumentList.append(ScpiInstrumentList[i])
            continue
        
        # If the returned data is longer than the maximum number of characters allowed by the SCPI standard,
        # The data is broken up into segments and sent separately.
        # We want to concanenate all the segmented data
        if (ScpiTypeList[i] == "Read" and ScpiTypeList[i - 1] == "Read"):
            AccumulatedScpiDataList[len(AccumulatedScpiDataList) - 1 ] = AccumulatedScpiDataList[-1] + ScpiDataList[i]
            continue

        AccumulatedScpiDataList.append(ScpiDataList[i])
        AccumulatedScpiTypeList.append(ScpiTypeList[i])
        AccumulatedScpiInstrumentList.append(ScpiInstrumentList[i])
    
    # Output parsed data
    print("{} parsed SCPI transactions found".format(len(AccumulatedScpiTypeList)))
    print("{} total transactions".format(len(ScpiTypeList)))
    OutputLog.write("{} parsed SCPI transactions found\n".format(len(AccumulatedScpiTypeList)))
    OutputLog.write("{} total transactions\n".format(len(ScpiTypeList)))
    
    for i in range(0, len(AccumulatedScpiTypeList)):
        if (AccumulatedScpiTypeList[i] == "Binblock Read"):
            OutputData = Binblock2Ascii(binascii.a2b_qp(AccumulatedScpiDataList[i]))
        else: 
            OutputData =  AccumulatedScpiDataList[i]

        OutputData = OutputData.replace('=\n', '')
        print("\n{}\n{}\n{}".format(AccumulatedScpiInstrumentList[i], AccumulatedScpiTypeList[i], OutputData))
        OutputLog.write("\n{}\n{}\n{}\n".format(AccumulatedScpiInstrumentList[i], AccumulatedScpiTypeList[i], OutputData))
        OutputExcel.write("{}\t{}\t{}\n".format(AccumulatedScpiInstrumentList[i], AccumulatedScpiTypeList[i], OutputData))
        
    OutputLog.close()
    OutputExcel.close()

Agilent IO Monitor Parser
===============

![alt text](http://repo.tapalla.com/images/IOMonitor1.png "Agilent IO Monitor")

Make practical use of those useless Agilent IO Monitor generated logs.

The __Agilent IO Monitor__ application, which is a part of the __Agilent IO Libraries Suite__, records all SCPI transactions sent between the host PC and instruments it is communicating with.
This is useful for test plan analysis, pinpointing bottlenecks, inspecting measurement methodology, etc. This transaction log can be exported as an XML file; however it is impractical to use since it stores the transactions in unreadable binary format. Additionally, XML files are not friendly for bulk analysis (e.g. timings).

This script will take the generated XML file, convert the binary SCPI into human-readable ASCII, then format it into parsable formats such as _.txt_ and _.xls_.

**Requirements**
* Python 3.3.0

**Instructions**

1. Use _Agilent IO Monitor_ to record SCPI transactions.
  1. Launch _Agilent IO Monitor_
  2. Click __Start Capturing Messages__
  3. Send your VISA commands, run your test script, what have you
  4. Click __Stop Capturing Messages__ when done
2. Generate the XML file
  1. _File_ > _Save Messages As_
  2. Save the __IOMonitorLog.xml__ file to the same directory as the __parser.py__ script
3. Run the script
  * Windows:
    1. Open the _Command Prompt_ and `cd` to the directory containing __parser.py__ as well as the _IOMonitorLog.xml_ file
    2. Run `py parser.py`
  * Mac OS X and Linux:
    1. Open the _Terminal_ and `cd` to the directory containing __parser.py__ as well as the _IOMonitorLog.xml_ file
    2. Run `py parser.py`
4. The parsed files will be generated in the same directory as __.txt__ and __.xls__ files containing the same name as the xml file

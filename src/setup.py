'''
Created on Apr 17, 2014

@author: mtapalla
'''
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
#build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
#if sys.platform == "win32":
#    base = "Win32GUI"

setup(  name = "AgilentIOMonitorParser",
        version = "0.1",
        description = "SCPI parser for Agilent IO Monitor",
 #       options = {"build_exe": build_exe_options},
        executables = [Executable("parser.py", base=base)])
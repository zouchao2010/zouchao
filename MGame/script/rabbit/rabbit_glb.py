# -*- coding:GBK -*-
import iapi


API = None

def init():
	global API
	API = iapi.API()

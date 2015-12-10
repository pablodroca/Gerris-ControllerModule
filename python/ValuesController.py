#!/usr/bin/python

import threading
from struct import *
import collections

class ForceValue(object):
	def __init__(self,pf,vf,pm,vm):
		self.pf = pf
		self.vf = vf
		self.pm = pm
		self.vm = vm
		
class LocationValue(object):
	def __init__(self):
		#self.varName = varName
		self.varMap = {}
	def addValue(self, varName, pos, value):
		values = self.varMap.get(varName)
		if values == None:
			values = []
			self.varMap[varName] = values
		values.append((pos,value))
		
class ValueControl(object):
	def __init__(self,time,step,data):
		#self.valType = valType
		self.time = time
		self.step = step
		self.data = data

class ValuesController(threading.Thread):
	def __init__(self,fifo,forcesList,locationsList,lock,length):
		super(ValuesController,self).__init__()
		self.fifo = fifo
		self.forcesList = forcesList
		self.locationsList = locationsList
		self.lock = lock
		self.length = int(length)
		
	def run(self):
		toRead = Struct('idi12d')
		toReadLoc = Struct('idi4d64s')
		while True:
			#try:
				print toRead.size
				query = self.fifo.read(toRead.size) # 112 B
				querySt = toRead.unpack(query)
				print querySt
				print "type"
				print querySt[0]
				if (querySt[0] == 0):	# type: 0 force
					print "Type FORCE"
					print "time"
                                	print querySt[1]
                                	print "step"
                                	print querySt[2]
                                	print "pfx"
                                	print querySt[3]
                                	print "pfy"
                                	print querySt[4]
                                	print "pfz"
                                	print querySt[5]
                                	print "vfx"
                                	print querySt[6]
                                	print "vfy"
                                	print querySt[7]
                                	print "vfz"
                                	print querySt[8]
                                	print "pmx"
                                	print querySt[9]
                                	print "pmy"
                                	print querySt[10]
                                	print "pmz"
                                	print querySt[11]
                                	print "vmx"
                                	print querySt[12]
                                	print "vmy"
                                	print querySt[13]
                                	print "vmz"
                                	print querySt[14]

					self.lock.acquire()
					# guardo valores en forcesList
					fVal = ForceValue(\
						(querySt[3],querySt[4],querySt[5]),\
						(querySt[6],querySt[7],querySt[8]),\
						(querySt[9],querySt[10],querySt[11]),\
						(querySt[12],querySt[13],querySt[14]))
					new = ValueControl(querySt[1],querySt[2],fVal)
					self.forcesList.append(new)			
					if len(self.forcesList) > self.length:
						self.forcesList.popleft()
					self.lock.release()
					print "Force guardada"
					
				elif (querySt[0] == 1): #type: 1 location
					print "Type LOCATION"
					querySt = toReadLoc.unpack(query)
					print querySt
					print "type"
					print querySt[0]
					print "time"
					print querySt[1]
					print "step"
					print querySt[2]
					print "value"
					print querySt[3]
					print "pos0"
					print querySt[4]
					print "pos1"
					print querySt[5]
					print "pos2"
					print querySt[6]
					print "varname"
					print querySt[7]
					self.lock.acquire()
					# guardo valores en locationsMap
					locVal = None
					for loc in self.locationsList:
						if loc.step == querySt[2]:
							locVal = loc
							break

					if (locVal == None):
						loc = LocationValue()
						locVal = ValueControl(querySt[1],querySt[2],loc)
						self.locationsList.append(locVal)

					locVal.data.addValue(querySt[7].rstrip(' \t\r\n\0'),(querySt[4],querySt[5],querySt[6]),querySt[3]) 
						
	
					#loc = LocationValue(querySt[4],querySt[5]) #O loc = LocationValue(querySt[4],(querySt[5],querySt[6],querySt[7]))
					#if not (querySt[3] in self.locationsMap):
					#	self.locationsMap[querySt[3]] = collections.deque()
					#self.locationsMap[querySt[3]].append(loc)
					if len(self.locationsList) > self.length:
						self.locationsList.popleft()
					self.lock.release()
					print "Location guardada"
				else:
					print "Error de tipo de valor a guardar"
			#except:
				#print "Error en ValuesController"
				#return

import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import math
from pymel.core import *

nodeName = 'pk_floatFalloffNode'
nodeId = om.MTypeId(0x127154)

class floatFalloffClass(ompx.MPxNode):
	def __init__(self):
		super(floatFalloffClass, self).__init__()

	def compute(self, plug, dataBlock):
		if plug == self.output:
			# input
			inputTimeValue = dataBlock.inputValue(self.inputTime).asFloat()
			baseTimeValue = dataBlock.inputValue(self.baseTime).asFloat()
			widthValue = dataBlock.inputValue(self.width).asFloat()
			falloffValue = dataBlock.inputValue(self.falloff).asFloat()
			spotValue = dataBlock.inputValue(self.spot).asFloat()

			# compute 
			diff = inputTimeValue - baseTimeValue
			if diff < 0 : diff = diff * -1

			if diff <= spotValue: 
				result = widthValue
			else:
				mult = falloffValue - diff + spotValue
				if mult < 0 : mult = 0
				if falloffValue <= 0: falloffValue = 0.01
				result = widthValue * mult / falloffValue
			
			# output
			outHandle = dataBlock.outputValue(self.output)
			outHandle.setFloat(result)
			
			dataBlock.setClean(plug)
			
		else:
			return om.kUnknownParameter
		
		return True

	@classmethod
	def creatorNode(cls): 
		return ompx.asMPxPtr(cls())

	@classmethod
	def nodeInitialize(cls):
		nAttr = om.MFnNumericAttribute()
		
		# output
		cls.output = nAttr.create("output", "out", om.MFnNumericData.kFloat, 0.0)
		nAttr.setStorable(False)
		nAttr.setWritable(False)
		cls.addAttribute(cls.output)
		
		# intput
		cls.inputTime = nAttr.create("inputTime", "inTime", om.MFnNumericData.kFloat, 0.0)
		nAttr.setStorable(True)
		nAttr.setConnectable(True)
		nAttr.setWritable(True)
		nAttr.setKeyable(True)
		cls.addAttribute(cls.inputTime)	
		cls.attributeAffects(cls.inputTime, cls.output)
		
		cls.baseTime = nAttr.create("baseTime", "baseTime", om.MFnNumericData.kFloat, 0.0)
		nAttr.setStorable(True)
		nAttr.setConnectable(True)
		nAttr.setWritable(True)
		nAttr.setKeyable(True)
		cls.addAttribute(cls.baseTime)	
		cls.attributeAffects(cls.baseTime, cls.output)
		
		cls.width = nAttr.create("width", "width", om.MFnNumericData.kFloat, 1.0)
		nAttr.setStorable(True)
		nAttr.setConnectable(True)
		nAttr.setWritable(True)
		nAttr.setKeyable(True)
		cls.addAttribute(cls.width)	
		cls.attributeAffects(cls.width, cls.output)
		
		cls.falloff = nAttr.create("falloff", "falloff", om.MFnNumericData.kFloat, 1.0)
		nAttr.setStorable(True)
		nAttr.setConnectable(True)
		nAttr.setWritable(True)
		nAttr.setKeyable(True)
		cls.addAttribute(cls.falloff)	
		cls.attributeAffects(cls.falloff, cls.output)
		
		cls.spot = nAttr.create("spot", "spot", om.MFnNumericData.kFloat, 1.0)
		nAttr.setStorable(True)
		nAttr.setConnectable(True)
		nAttr.setWritable(True)
		nAttr.setKeyable(True)
		cls.addAttribute(cls.spot)	
		cls.attributeAffects(cls.spot, cls.output)


def initializePlugin(mobject):
	plugin = ompx.MFnPlugin(mobject, "Pavel Korolyov", "1.0", "Any")
	try:
		plugin.registerNode(nodeName, nodeId, 
		                    floatFalloffClass.creatorNode,
		                    floatFalloffClass.nodeInitialize,
		                    ompx.MPxNode.kDependNode)
	except:
		om.MGlobal.displayError("Failed unload plugin: %s\n" % nodeName)

def uninitializePlugin(mobject):
	plugin = ompx.MFnPlugin(mobject)
	try:
		plugin.deregisterNode(nodeId)
	except:
		om.MGlobal.displayError("Failed to unregister command: %s\n" % nodeName)
		raise
	


class AEpk_floatFalloffNodeTemplate(ui.AETemplate):
	def __init__(self, nodeName):
		super(AEpk_floatFalloffNodeTemplate, self).__init__(nodeName)
		
		self.beginScrollLayout()
		ui.AETemplate.beginLayout(self,"Parameters", collapse=0) #self.beginLayout("Parametrs", collapse=0)
		ui.AETemplate.addControl(self,"inputTime") #self.addControl('func')		
		ui.AETemplate.addControl(self, "baseTime") #self.addControl('input')
		ui.AETemplate.addControl(self,"width")	
		ui.AETemplate.addControl(self,"falloff")	
		ui.AETemplate.addControl(self,"spot")	
		ui.AETemplate.addControl(self,"output")
		
		self.endLayout()
		mel.AEdependNodeTemplate(nodeName)
		self.addExtraControls()
		self.endScrollLayout()
		
mel.refreshEditorTemplates()
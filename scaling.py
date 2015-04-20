import bpy
import numpy
import math

# according to hypertextbook.com/facts/2006/bodyproportions.shtml
# forarm+hand vs forarm ratio
GOLDEN_RATIO = 1.618 

# blender object modes
EDIT_MODE = 'EDIT'
OBJECT_MODE = 'OBJECT'

# name of the hand objects after imported into blender
HAND_LEFT = 'handLeft'
HAND_RIGHT = 'handRight'

# name of the forarm bone, should always be this name
FOREARM = 'rForeArm'

# get the total length of all the children bone
def childrenBoneLength(children):
    length = 0
    
    for bone in children:
        length += bone.length
    
    return length

# calculate the length of the leap hand imported into blender
def getLeapHandLength():
    middleFinger = 'Middle_Metacarpal'
    # assuming the model is always loaded after the body model
    armatures = bpy.data.armatures[HAND_LEFT]
    if armatures is not None:
        bones = armatures.bones
        if middleFinger in bones:
            finger = bones[middleFinger]
            return finger.length + childrenBoneLength(finger.children_recursive)
    
    return -1    

# calculates the length of the hand on the model
def getModelHandLength():
    middleFinger = 'lMid1'
    hand = 'lHand'
    armatures = bpy.data.armatures[0]
    if armatures is not None:
        bones = armatures.bones
        if middleFinger in bones:
            finger = bones[middleFinger]
            return bones[hand].length + finger.length + childrenBoneLength(finger.children_recursive)
    
    return -1   
        

# returns the length of the forearm of the model
def getForeArmLength():
    # assuming the model is always loaded first
    armatures = bpy.data.armatures[0]
    if armatures is not None:
        bones = armatures.bones
        if FOREARM in bones:
            return bones[FOREARM].length
    
    return -1     

# returns the scale factor required to scale the leap hand model
def getScaleFactor():
    scaleFactor = 0
    
    foreArmLength = getForeArmLength()
    modelHandLength = getModelHandLength()
    leapHandLength = getLeapHandLength()
    
    if foreArmLength > 0:
        if modelHandLength < 0:
            # in case where there isnt a hand available
            # we scale it based on the golden ratio
            modelHandLength = (GOLDEN_RATIO*foreArmLength - foreArmLength)
            
        scaleFactor = leapHandLength/modelHandLength
    
    return math.fabs(scaleFactor)

# scales the hand
# possible other ways:
# 1. bpy.ops.transform.resize
# 2. iterate through every bone of the hand and resize    
def scaleHand(hand):
    bpySceneObj = bpy.context.scene.objects
    bpyOpsObj = bpy.ops.object
    bpyDataObj = bpy.data.objects
    
    # set the active object to be resized
    bpySceneObj.active = bpyDataObj.get(hand)
    handModel = bpyDataObj[hand]
    if handModel is not None:
        scaleFactor = getScaleFactor()
        if scaleFactor != 0:
            scaleFactor = 1/scaleFactor
            handModel.scale = (scaleFactor, scaleFactor, scaleFactor)        
    
    bpySceneObj.active = None 

# scales both right and left hand
def scaleBothHands():
    scaleHand(HAND_LEFT)
    scaleHandRight(HAND_RIGHT)
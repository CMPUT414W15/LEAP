import bpy
import numpy
import math


class Scaler:

    # according to hypertextbook.com/facts/2006/bodyproportions.shtml
    # forarm+hand vs forarm ratio
    GOLDEN_RATIO = 1.618

    # name of the forarm bone, should always be this name
    FOREARM = 'rForeArm'

    # name of the hand objects after imported into blender
    leftHandName = ''
    rightHandName = ''
    modelName = ''

    def __init__(self, modelName, leftHandName, rightHandName):
        self.leftHandName = leftHandName
        self.rightHandName = rightHandName
        self.modelName = modelName

    # get the total length of all the children bone
    def childrenBoneLength(self, children):
        length = 0

        for bone in children:
            length += bone.length

        return length

    # calculate the length of the leap hand imported into blender
    def getLeapHandLength(self):
        middleFinger = 'Middle_Metacarpal'
        # assuming the model is always loaded after the body model
        armatures = bpy.data.armatures[self.leftHandName]
        if armatures is not None:
            bones = armatures.bones
            if middleFinger in bones:
                finger = bones[middleFinger]
                return finger.length + self.childrenBoneLength(finger.children_recursive)

        return -1

    # calculates the length of the hand on the model
    def getModelHandLength(self):
        middleFinger = 'lMid1'
        hand = 'lHand'
        armatures = bpy.data.armatures[self.modelName]
        if armatures is not None:
            bones = armatures.bones
            if middleFinger in bones:
                finger = bones[middleFinger]
                return bones[hand].length + finger.length + self.childrenBoneLength(finger.children_recursive)

        return -1


    # returns the length of the forearm of the model
    def getForeArmLength(self):
        # assuming the model is always loaded first
        armatures = bpy.data.armatures[self.modelName]
        if armatures is not None:
            bones = armatures.bones
            if self.FOREARM in bones:
                return bones[self.FOREARM].length

        return -1

    # returns the scale factor required to scale the leap hand model
    def getScaleFactor(self):
        scaleFactor = 0

        foreArmLength = self.getForeArmLength()
        modelHandLength = self.getModelHandLength()
        leapHandLength = self.getLeapHandLength()

        if foreArmLength > 0:
            if modelHandLength < 0:
                # in case where there isnt a hand available
                # we scale it based on the golden ratio
                modelHandLength = (self.GOLDEN_RATIO*foreArmLength - foreArmLength)

            scaleFactor = leapHandLength/modelHandLength

        return math.fabs(scaleFactor)

    # scales the hand
    # possible other ways:
    # 1. bpy.ops.transform.resize
    # 2. iterate through every bone of the hand and resize
    def scaleHand(self, hand):
        bpySceneObj = bpy.context.scene.objects
        bpyDataObj = bpy.data.objects

        # set the active object to be resized
        bpySceneObj.active = bpyDataObj.get(hand)
        handModel = bpyDataObj[hand]
        if handModel is not None:
            scaleFactor = self.getScaleFactor()
            if scaleFactor != 0:
                scaleFactor = 1/scaleFactor
                handModel.scale = (scaleFactor, scaleFactor, scaleFactor)

        bpySceneObj.active = None

    # scales both hands imported into leap
    def scaleBothHands(self):
        self.scaleHand(self.leftHandName)
        self.scaleHand(self.rightHandName)
        
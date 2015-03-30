import os
import csv
from pyfbsdk import FBCreateObject, FBVector3d

#get file
#filename = input('Enter the filename')
filename = "D:/Documents/courses/414/leap/data/left_dribble.csv"

#files = ["data/left_dribble.csv",
#      "data/left_move.csv",
#      "data/left_pina.csv",
#      "data/right_dribble.csv",
#      "data/right_move.csv",
#      "data/right_piano.csv"]


vectors = ['Hand Palm', 'Arm Direction', 'Wrist Position', 'Elbow Position', 'Thumb Metacarpal Start', 'Thumb Metacarpal End', 'Thumb Metacarpal Direction', 'Thumb Proximal Start', 'Thumb Proximal End', 'Thumb Proximal Direction', 'Thumb Middle Start', 'Thumb Middle End', 'Thumb Middle Direction', 'Thumb Distal Start', 'Thumb Distal End', 'Thum Distal Direction', 'Index Metacarpal Start', 'Index Metacarpal End', 'Index Metacarpal Direction', 'Index Proximal Start', 'Index Proximal End', 'Index Proximal Direction', 'Index Middle Start', 'Index Middle End', 'Index Middle Direction', 'Index Distal Start', 'Index Distal End', 'Index Distal Direction', 'Middle Metacarpal Start', 'Middle Metacarpal End', 'Middle Metacarpal Direction', 'Middle Proximal Start', 'Middle Proximal End', 'Middle Metacarpal Direction', 'Middle Middle Start', 'Middle Middle End', 'Middle Middle Direction', 'Middle Distal Start', 'Middle Distal End', 'Middle Distal Direction', 'Ring Metacarpal Start', 'Ring Metacarpal End', 'Ring Metacarpal Direction', 'Ring Proximal Start', 'Ring Proximal End', 'Ring Proximal Direction', 'Ring Middle Start', 'Ring Middle End', 'Ring Middle Direction', 'Ring Distal Start', 'Ring Distal End', 'Ring Distal Direction', 'Pinky Metacarpal Start', 'Pinky Metacarpal End', 'Pinky Metacarpal Direction', 'Pinky Proximal Start', 'Pinky Proximal End', 'Pinky Proximal Direction', 'Pinky Middle Start', 'Pinky Middle End', 'Pinky Middle Direction', 'Pinky Distal Start', 'Pinky Distal End', 'Pinky Distal Direction']

fingers = ['Thumb','Index','Middle','Ring','Pinky']
joints = ['Metacarpal', 'Middle', 'Distal', 'Proximal']
ends = ['Start', 'End', 'Direction']


#combinations = [' '.join([f, j, e])
#        for f in fingers
#        for j in joints
#        for e in ends]
#
## Some of these things are not like the others; some of these things just don't
## belong
#for i in vectors:
#    if i not in combinations:
#        print i
## Note that all combinations exists in the vectors, however, so using the
# combinations should be safe, with the exception of thumb-metacarpal, which shouldn't exist
#for i in combinations:
#        print i in vectors


def fileApply(f):
    with open(filename, 'rb') as handfile:
        reader = csv.DictReader(handfile)
        
        # create skeleton nodes based on objects
        map(f, reader)
    

def process(fileDict):
    # start creating skeleton root at the wrist?
    wrist_keys = ["Wrist Position %s" % axis for axis in list('XYZ')]
    wrist_vector = [float(fileDict[k]) for k in wrist_keys]
    print(wrist_vector)
    wrist = FBCreateObject( "Browsing/Templates/Elements", "Skeleton root",
            "Wrist")
    wrist.Translation = FBVector3d(*wrist_vector)
    #for f in fingers:
    #    for j in joints:
    #        for e in ends:
    #            


if __name__ in  ("__main__" , "__builtin__"):
    fileApply(process)


# FBCreateObject(GroupName, EntryName, ObjectName) has 3 parameters as input:
# GroupName: id of the group creation function. In asset Browser each group starts with "Browsing" (ex: Browsing/Templates/Elements)
# EntryName: This is id of the object to create. In Asset Browser this would be the name under the icon (ex: Cube)
# ObjectName: the name the object will have at creation

#test = FBCreateObject( "Browsing/Templates/Elements", "Skeleton root", "HANDROOT" )
#test2 = FBCreateObject( "Browsing/Templates/Elements", "Skeleton node", "HANDNODE" )
#print(test)

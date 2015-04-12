import csv
from pyfbsdk import FBCreateObject, FBVector3d

# get file
# filename = input('Enter the filename')
filename = "D:/Documents/courses/414/leap/data/left_dribble.csv"

# files = ["data/left_dribble.csv",
#      "data/left_move.csv",
#      "data/left_pina.csv",
#      "data/right_dribble.csv",
#      "data/right_move.csv",
#      "data/right_piano.csv"]


class HandsMaker:
    # You can use 'Hand Palm', 'Arm Direction', 'Wrist Position' and 'Elbow
    # Position' in addition to the combination of the following 3
    FINGERS = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    JOINTS = ['Metacarpal', 'Middle', 'Distal', 'Proximal']
    ENDS = ['Start', 'End', 'Direction']
    def __init__(self):
        self.skel = []
        self.skelAnimationNodes = []
        self.wrist = FBCreateObject("Browsing/Templates/Elements",
                                    "Skeleton root",
                                    "Wrist")
        self.skelNames = [" ".join([f, j, "End"])
                    for f in self.FINGERS for j in self.JOINTS]
        time = 0

    def joint_key(self, joint_name):
        axes = list('XYZ')
        return [" ".join([joint_name, axis]) for axis in axes]


    def fileApply(self, lines_func):
        # create skeleton nodes based on objects
        self.skel = [FBCreateObject("Browsing/Templates/Elements",
                                    "Skeleton node",
                                    " ".join([f, j, "End"]))
                     for f in self.FINGERS for j in self.JOINTS]
        # set properties for every joint
        for x in self.skel:
            x.Show = True
            x.Translation.SetAnimated(True)
            # get animation nodes
            self.skelAnimationNodes = [x.Translation.GetAnimationNode()
                                       for x in self.skel]
        # read and apply lines_func to each line read
        with open(filename, 'rb') as handfile:
            reader = csv.DictReader(handfile)
            map(lines_func, reader)
            #lines_func(reader.next())


    # get the position vector for a given joint in the current dict
    def posVector(self, joint_name, line_dict):
        return FBVector3d(*[float(line_dict[k]) for k in self.joint_key(joint_name)])

    # parse and work with each line
    def processLine(self, line_dict):
        # start creating skeleton root at the wrist?
##        wrist_vector = self.posVector("Wrist", line_dict)
##        self.wrist.Translation = wrist_vector
##        self.wrist.Show = True

        # set vectors for each skeleton node
        for node, vector in zip(self.skelAnimationNodes, [self.posVector(x, line_dict) for x in self.skelNames]):
            # add key to fcurves for each animation node (translation XYZ values)
            fcurves = [n.FCurve for n in node.Nodes]
            for fcurve, axis in zip(fcurves, vector):
                #TODO: fix fcurve
                fcurve.KeyAdd(0, axis)
        self.time += 1000

if __name__ in ("__main__", "__builtin__"):
    a = HandsMaker()
    a.fileApply(a.processLine)


# FBCreateObject(GroupName, EntryName, ObjectName) has 3 parameters as input:
# GroupName: id of the group creation function. In asset Browser each group
#     starts with "Browsing" (ex: Browsing/Templates/Elements)
# EntryName: This is id of the object to create. In Asset Browser this would be
#     the name under the icon (ex: Cube)
# ObjectName: the name the object will have at creation

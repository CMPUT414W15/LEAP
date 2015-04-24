###===================================================================
# 	File used to generate BVH for LEAP Motion Capture Data
###===================================================================

###===================================================================
# 	Create the header section of a BVH file
# 	joints = List containing joint names (strings)
# 	offsets = List containing offsets (strings)
###===================================================================
def createHeader(joints, offsets):

    header = "HIERARCHY"

    # Strings used in header
    root = " 6 Xposition Yposition Zposition Zrotation Yrotation Xrotation"
    joint = " 3 Zrotation Yrotation Xrotation"

    # Keep track of channels to add to BVH
    channels = [root] + [joint] * (len(joints) - 1)

    # Keep track of number of tabs (aesthetic formatting only)
    counter = 0

    for c, joint in enumerate(joints):
    	# Root node
        if c == 0:
            header += '\n' + '\t'*(c - counter) +  'ROOT %s\n{\n'%(joint) + '\t'*(c - counter + 1) + 'OFFSET %s \n'%(offsets[c]) + '\t'*(c - counter + 1) +'CHANNELS %s '%(channels[c])
            continue

        # End Site (Distal bone)
        if joint[-6:] == "Distal":
            header += '\n' + '\t'*(c - counter) +  'JOINT %s\n'%(joint) + '\t'*(c - counter) + '{\n' + '\t'*(c - counter + 1) + 'OFFSET %s \n'%(offsets[c-1]) + '\t'*(c - counter + 1) +'CHANNELS %s '%(channels[c])
            header += '\n' + '\t' * (c - counter + 1) + 'End Site\n' + '\t' * (c - counter + 1) + '{\n' +'\t' * (c - counter + 2) + 'OFFSET %s\n'%(offsets[c])
            temp = counter
            counter = c
            # Add closing braces
            while (c - temp >= 0):
                header += '\t'*(c - temp + 1) + '}\n'
                c -= 1

        # First joint (connected to the root, distance should be 0)
        elif joint[-10:] == "Metacarpal":
            header += '\n' + '\t'*(c - counter) +  'JOINT %s\n'%(joint) + '\t'*(c - counter + 1) + '{\n' + '\t'*(c - counter + 1) + 'OFFSET 0.0 0.0 0.0\n' + '\t'*(c - counter + 1) +'CHANNELS %s '%(channels[c])
        
        # Any other joint
        else:
            header += '\n' + '\t'*(c - counter) +  'JOINT %s\n'%(joint) + '\t'*(c - counter + 1) + '{\n' + '\t'*(c - counter + 1) + 'OFFSET %s \n'%(offsets[c-1]) + '\t'*(c - counter + 1) +'CHANNELS %s '%(channels[c])

    header += "}\n"

    return header

###===================================================================
# 	Create the motion section of a BVH file
# 	motions = list of lists representing all motions of a frame
# 	time = time frame value
###===================================================================
def createMotion(motions, time):
	# Motion header information
    motion = "MOTION\nFrames: %s\nFrame Time: %s"%(len(motions), time) + '\n'
    # Information for each frame
    motion += "\n".join(motions)
    
    return motion

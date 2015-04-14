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

	channels = []

	root = " 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation"
	joint = " 3 Zrotation Xrotation Yrotation"

	channels.append(root)
	for i in range(len(joints)-1):
		channels.append(joint)

	counter = 0
	for c, joint in enumerate(joints):
		if joint[-6:] == "Distal":
			header += '\n' + '\t' * (c - counter) + 'End Site\n' + '\t' * (c - counter) + '{\n' +'\t' * (c - counter + 1) + 'OFFSET %s\n'%(offsets[c]) 
			temp = counter
			counter = c
			while (c - temp > 0):
				header += '\t'*(c - temp) + '}\n'
				c -= 1
		elif c == 0:
			header += '\n' + '\t'*(c - counter) +  'ROOT %s\n{\n'%(joint) + '\t'*(c - counter + 1) + 'OFFSET %s \n'%(offsets[c]) + '\t'*(c - counter + 1) +'CHANNELS %s '%(channels[c])
		else:
			header += '\n' + '\t'*(c - counter) +  'JOINT %s\n'%(joint) + '\t'*(c - counter) + '{\n'+ '\t'*(c - counter + 1) + 'OFFSET %s \n'%(offsets[c]) + '\t'*(c - counter + 1) +'CHANNELS %s '%(channels[c])

	header += "}\n"

	return header

###===================================================================
# 	Create the motion section of a BVH file
# 	motions = list of lists representing all motions of a frame
# 	time = time frame value
###===================================================================
def createMotion(motions, time):

	motion = "MOTION\nFrames: %s\nFrame Time: %s"%(len(motions), time)
	for i in motions:
		motion += "\n"
		for j in i:
			motion += j + ' '

	return motion


###===================================================================
# 	Example Usage
# 	2 fingers + Root
# 	3 frames of data
# 	Made up offsets
###===================================================================
if __name__ == "__main__":
	joints = ["Hand", "Thumb Metacarpal", "Thumb Proximal", "Thumb Intermediate", "Thumb Distal", "Index Metacarpal", "Index Proximal", "Index Intermediate", "Index Distal"]
	offsets = ["0 0 0", "0 0 1", "0 1 0", "0 1 1", "1 0 0", "1 0 1", "1 1 0", "1 1 1", "0 0 0", "0 0 1", "0 1 0"]
	motions = [['3', '3', '4', '2', '4', '5', '2'], ['3', '3', '7', '6', '5', '5', '4'], ['4', '5', '3', '2', '4', '1', '4']]
	time = '0.5'

	header = createHeader(joints, offsets)
	motion = createMotion(motions, time)

	BVH = header + motion

	print(BVH)









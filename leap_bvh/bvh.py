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

	root = " 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation"
	joint = " 3 Zrotation Xrotation Yrotation"

	channels = [root] + [joint] * (len(joints) - 1)

	counter = 0
	for c, joint in enumerate(joints):
		if c == 0:
			header += '\n' + '\t'*(c - counter) +  'ROOT %s\n{\n'%(joint) + '\t'*(c - counter + 1) + 'OFFSET %s \n'%(offsets[c]) + '\t'*(c - counter + 1) +'CHANNELS %s '%(channels[c])
			continue

		if joint[-6:] == "Distal":
			header += '\n' + '\t'*(c - counter) +  'JOINT %s\n'%(joint) + '\t'*(c - counter) + '{\n' + '\t'*(c - counter + 1) + 'OFFSET %s \n'%(offsets[c-1]) + '\t'*(c - counter + 1) +'CHANNELS %s '%(channels[c])
			header += '\n' + '\t' * (c - counter + 1) + 'End Site\n' + '\t' * (c - counter + 1) + '{\n' +'\t' * (c - counter + 2) + 'OFFSET %s\n'%(offsets[c])
			temp = counter
			counter = c
			while (c - temp >= 0):
				header += '\t'*(c - temp + 1) + '}\n'
				c -= 1
		
		elif joint[-10:] == "Metacarpal":
			header += '\n' + '\t'*(c - counter) +  'JOINT %s\n'%(joint) + '\t'*(c - counter + 1) + '{\n' + '\t'*(c - counter + 1) + 'OFFSET 0.0 0.0 0.0\n' + '\t'*(c - counter + 1) +'CHANNELS %s '%(channels[c])
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

	motion = "MOTION\nFrames: %s\nFrame Time: %s"%(len(motions), time) + '\n'
	motion += "\n".join(motions)
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
	motions = ['3 2 1 3 4 3', '3 2 4 3 2 4', '4 5 2 3 4 2']
	time = '0.5'

	header = createHeader(joints, offsets)
	motion = createMotion(motions, time)

	BVH = header + motion

	print(BVH)
	# print(header)









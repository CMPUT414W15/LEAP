import bpy
from numpy import array, zeros, argmin, inf
from numpy.linalg import norm
from mathutils import *

####==========================================================================
#   DTW implementation courtesy of Pierre Rouanet:
#   http://github.com/pierre-rouanet/dtw
#   See examples that he posts
####==========================================================================

def dtw(x, y, dist=lambda x, y: norm(x - y, ord=1)):
    """ Computes the DTW of two sequences.

    :param array x: N1*M array
    :param array y: N2*M array
    :param func dist: distance used as cost measure (default L1 norm)

    Returns the minimum distance, the accumulated cost matrix and the wrap path.

    """
    x = array(x)
    if len(x.shape) == 1:
        x = x.reshape(-1, 1)
    y = array(y)
    if len(y.shape) == 1:
        y = y.reshape(-1, 1)

    r, c = len(x), len(y)

    D = zeros((r + 1, c + 1))
    D[0, 1:] = inf
    D[1:, 0] = inf

    for i in range(r):
        for j in range(c):
            D[i+1, j+1] = dist(x[i], y[j])

    for i in range(r):
        for j in range(c):
            D[i+1, j+1] += min(D[i, j], D[i, j+1], D[i+1, j])

    D = D[1:, 1:]

    dist = D[-1, -1] / sum(D.shape)

    return dist, D, _trackeback(D)


def _trackeback(D):
    i, j = array(D.shape) - 1
    p, q = [i], [j]
    while (i > 0 and j > 0):
        tb = argmin((D[i-1, j-1], D[i-1, j], D[i, j-1]))

        if (tb == 0):
            i = i - 1
            j = j - 1
        elif (tb == 1):
            i = i - 1
        elif (tb == 2):
            j = j - 1

        p.insert(0, i)
        q.insert(0, j)

    p.insert(0, 0)
    q.insert(0, 0)
    return (array(p), array(q))

####==========================================================================


####==========================================================================
#   Get the rotation given mocap to search in, bonename, and frame
#   "action" is a blender Action, "bonename" is a string, "frame" is an int
#   blender Actions can be found in bpy.data.actions
####==========================================================================
def get_rotation(action, bonename, frame=1):
    rot = Euler([0,0,0])
    data_path = 'pose.bones["%s"].rotation_euler'%(bonename)
    for fc in action.fcurves:
        if fc.data_path == data_path:
            rot[fc.array_index] = fc.evaluate(frame)
    return(rot)

####==========================================================================
#   Creates a list containing the rotations of a bone
#   rot[i] equals the i+1th frame of animation
#   "action" is a blender Action, "bonename" is a string
####==========================================================================
def listRotation(action, bonename):
	rot = []
	if bonename[-3:] == "001":
		bonename = bonename[:-4]
	for i in range(1, int(action.fcurves[0].range()[1]) + 1):
		rot.append(get_rotation(action, bonename, i))
	return rot

####==========================================================================
#   Creates new rotation FCurves
#   "action" is a blender Action, "bonename" is a string and 
#   "rot" is a list of vectors
#	FCurves are guarenteed to not exist if the model is joined for the first time
####==========================================================================
def addRotation(action, bonename, rot):
    data_path = 'pose.bones["%s"].rotation_euler'%(bonename)
    c0 = action.fcurves.new(data_path, 0)
    c1 = action.fcurves.new(data_path, 1)
    c2 = action.fcurves.new(data_path, 2)

    c0k = c0.keyframe_points
    c1k = c1.keyframe_points
    c2k = c2.keyframe_points

    x = []
    y = []
    z = []  

    # Separate x, y, z values 
    for i in range(len(rot)):
        x.append(rot[i][0])
        y.append(rot[i][1])
        z.append(rot[i][2])

    for i in range(1, len(x)+1):
        c0k.insert(i, x[i-1])
        c1k.insert(i, y[i-1])
        c2k.insert(i, z[i-1])


####==========================================================================
#  	This section was not used for the demo, however it represents the code base
#	necessary to implement interpolation using the DTW algorithm
#	There was not enough time to test and so this code may contain bugs
#	An example usage is shown below:
# 	
#	action1 = bpy.data.actions[0] # Mocap 1
#   action2 = bpy.data.actions[1] # Mocap 2
#
#   # Comparison joints
#   bodyBone = 'lHand'
#   handBone = 'Hand'
#
#   # Get the rotation data (vectors)
#   rotA = listRotation(action1, bodyBone)
#   rotB = listRotation(action2, handBone)
#
#   # Process rotA and rotB
#   rotA, rotB = applyDTW(rotA, rotB)
#
#   # Replace originals
#   replaceRotation(action1, bodyBone, rotA)
#   replaceRotation(action2, handBone, rotB)
#
# 	It will be necessary to compare every joint on the body to ensure the 
#	number of frames is consistent across every FCurve
####==========================================================================

####==========================================================================
#   Replaces the existing rotation FCurves with the new computed rotations
#   "action" is a blender Action, "bonename" is a string and 
#   "rot" is a list of vectors
#	This function was replaced by addRotation for the demo but can still be used
# 	wrt interpolation using the DTW algorithm
####==========================================================================
def replaceRotation(action, bonename, rot):
    data_path = 'pose.bones["%s"].rotation_euler'%(bonename)
    x = []
    y = []
    z = []  
    # Separate x, y, z values 
    for i in range(len(rot)):
        x.append(rot[i][0])
        y.append(rot[i][1])
        z.append(rot[i][2])

    # Obtain curves of interest
    for curve in action.fcurves:
    	if curve.data_path == data_path:
    		if curve.array_index == 0:
    			c0 = curve
    		elif curve.array_index == 1:
    			c1 = curve
    		elif curve.array_index == 2:
    			c2 = curve

   	# Access keyframes
    c0k = c0.keyframe_points
    c1k = c1.keyframe_points
    c2k = c2.keyframe_points

    # Replace existing keyframes with new ones
    for i in range(1, len(x)+1):
        c0k.insert(i, x[i-1], {'REPLACE'})
        c1k.insert(i, y[i-1], {'REPLACE'})
        c2k.insert(i, z[i-1], {'REPLACE'})

####==========================================================================
#   Creates the final curve based on determined path
#   Based on current undrestanding of the function
#   "curve" is a list of vectors and "path" is a list of ints
####==========================================================================
def match(curve, path):
    t = []
    for i in path:
        t.append(curve[i])
    return t

####==========================================================================
#   Run DTW alg to find shortest path
#   Primarily interested in Path for the time being
#   Uses it to generate the new rotations
#   "curveA", "curveB" are a list of vectors
####==========================================================================
def applyDTW(curveA, curveB):
    dist, cost, path = dtw(curveA, curveB)
    curveA = match(curveA, path[0])
    curveB = match(curveB, path[1])
    return curveA, curveB

####==========================================================================


if __name__ == "__main__":
	obj = bpy.data.objects
	body = obj[0] # Assumes this returns the body bvh

	bpy.ops.object.select_all(action="DESELECT") # Deselect All
	bpy.ops.object.select_by_type(type="ARMATURE") # Select all armatures *ie imported BVH)
	bpy.context.scene.objects.active = body 
	bpy.ops.object.join() # Merge the bvh files
	bpy.ops.object.mode_set(mode="EDIT") # Turn on edit mode (so there are edit bones)

	body = obj[0] # Re-select the object, for some reason it doesn't seem to work otherwise

	# Identify marker bones: Names can be changed to accomodate the BVH files imported
	# Using the provided leap_reader script, the hands will have the names "LeftHand" and "RightHand"
	# The BVH files we used (from https://sites.google.com/a/cgspeed.com/cgspeed/motion-capture/daz-friendly-release) used the naming conventions "lHand", and "rHand"
	for bone in body.data.edit_bones:
	    if bone.name == "lHand":
	        blh = bone
	    if bone.name == "LeftHand":
	        lh = bone
	    if bone.name == "rHand":
	    	brh = bone
	    if bone.name == "RightHand":
	    	rh = bone

	# Assigns the parents of the bones
	rh.parent = brh
	lh.parent = blh

	# List used to log the length of each bone in the hand (initially)
	# This step is necessary now because the hand is attached using "bone.use_connect = True" which moves the bone automatically, and warps the length of the finger
	vecs = []

	# The BVH files we used contained fingers (but no adequate hand animation)
	# This section delets all the fingers that came with the model (assuming naming conventions such as "lThumb", "rThumb", etc)
	# Also, calculate the length of the finger if it is part of the imported BVH
	for child in blh.children_recursive:
		if child.name[:1] == "l":
			body.data.edit_bones.remove(child)
		else:
			vecs.append((child.name, child.tail-child.head))

	for child in brh.children_recursive:
		if child.name[:1] == "r":
			body.data.edit_bones.remove(child)
		else:
			vecs.append((child.name, child.tail-child.head))

	# Connect the root of the hand BVHs to the body BVH and set it's length accordingly
	vec = [v[1] for i, v in enumerate(vecs) if v[0] == lh.name]
	vec = vec[0]
	lh.use_connect = True
	lh.tail = lh.head + vec

	vec = [v[1] for i, v in enumerate(vecs) if v[0] == rh.name]
	vec = vec[0]
	rh.use_connect = True
	rh.tail = rh.head + vec

	# Connect each bone to the parent's location, and then adjust the length accordingly
	# This essentially moves the hand to the body while keeping the orientation and scale
	for bone in lh.children_recursive:
		bone.use_connect = True
		vec = [v[1] for i, v in enumerate(vecs) if v[0] == bone.name]
		vec = vec[0]
		bone.tail = bone.head + vec

	for bone in rh.children_recursive:
		bone.use_connect = True
		vec = [v[1] for i, v in enumerate(vecs) if v[0] == bone.name]
		vec = vec[0]
		bone.tail = bone.head + vec

	# Actions contain the animation data
	# 'left' and 'right' are the names of the BVH files for the left and right hands respectively
	# When the BVH files are merged, the animation data is kept separate. Therefore, it is necessary to extract the animations stored in the actions
	# and add it to the main BVH
	bodyActions = bpy.data.actions[0]
	handActions1 = bpy.data.actions['left']
	handActions2 = bpy.data.actions['right']

	bonename = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
	joint = ["Metacarpal", "Proximal", "Intermediate", "Distal", "Metacarpal.001", "Proximal.001", "Intermediate.001", "Distal.001"]

	# Adds the existing animation on the FCurve to the main BVH
	for b in bonename:
		for j in joint:
			bone = b + "_" + j
			# Using the Leap_reader script, the bone names will be identical
			# Blender will automatically rename the bones to end in ".001"
			if bone[-3:] == "001":
				rot = listRotation(handActions2, bone)
			else:
				rot = listRotation(handActions1, bone)
			addRotation(bodyActions, bone, rot)

















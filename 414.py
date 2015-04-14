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
	for i in range(1, int(action.fcurves[0].range()[1]) + 1):
		rot.append(get_rotation(action, bonename, i))
	return rot

####==========================================================================
#   Replaces the existing rotation FCurves with the new computed rotations
#   "action" is a blender Action, "bonename" is a string and 
#   "rot" is a list of vectors
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
#   Example Usage
####==========================================================================
if __name__ == "__main__":
	action1 = bpy.data.actions[0] # Mocap 1
    action2 = bpy.data.actions[1] # Mocap 2
    
    # Comparison joints
    bodyBone = 'lHand'
    handBone = 'Hand'

    # Get the rotation data (vectors)
	rotA = listRotation(action1, bodyBone)
	rotB = listRotation(action2, handBone)

    # Process rotA and rotB
    rotA, rotB = applyDTW(rotA, rotB)

    # Replace originals
    replaceRotation(action1, bodyBone, rotA)
    replaceRotation(action2, handBone, rotB)



import bpy
from numpy import array, zeros, argmin, inf
from numpy.linalg import norm
from mathutils import *


####==========================================================================
#   DTW implementation courtesy of Pierre Rouanet:
#   http://github.com/pierre-rouanet/dtw
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

# Get the rotation given mocap, bonename, and frame
def get_rotation(action, bonename, frame=1):
    rot = Euler([0,0,0])
    data_path = 'pose.bones["%s"].rotation_euler'%(bonename)
    for fc in action.fcurves:
        if fc.data_path == data_path:
            rot[fc.array_index] = fc.evaluate(frame)
    return(rot)

# Creates a list containing the rotations of a bone
# rot[i] equals the i+1th frame of animation
def listRotation(action, bonename):
	rot = []
	for i in range(1, int(action.fcurves[0].range()[1]) + 1):
		rot.append(get_rotation(action, bonename, i))
	return rot

# Replaces the existing rotation FCurves with the new one
def replaceRotation(action, bonename, rot):
    data_path = 'pose.bones["%s"].rotation_euler'%(bonename)
    # c2 = action.fcurves.new(data_path)
    # c2.array_index = 2
    # c1 = action.fcurves.new(data_path)
    # c1.array_index = 1
    # c0 = action.fcurves.new(data_path)
    # c0.array_index = 1
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

if __name__ == "__main__":
	action = bpy.data.actions[0]
	rotA = listRotation(action, 'lHand')
	rotB = listRotation(action, 'rHand')

	dist, cost, path = dtw(rotA, rotB)

	print("dist", dist)
	print("cost", cost)
	print("path", path)







fcurves = bpy.context.scene.node_tree.animation_data.action.fcurves

for fcu in fcurves:
    fcurves.remove(fcu)
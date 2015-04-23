import bpy
from numpy import array, zeros, argmin, inf
from numpy.linalg import norm
from mathutils import *

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

obj = bpy.data.objects

body = obj[0]
# hand = obj[1]

bpy.ops.object.select_all(action="DESELECT")
bpy.ops.object.select_by_type(type="ARMATURE")
bpy.context.scene.objects.active = body
bpy.ops.object.join()
bpy.ops.object.mode_set(mode="EDIT")

body = obj[0]

for bone in body.data.edit_bones:
    if bone.name == "lHand":
        blh = bone
    if bone.name == "LeftHand":
        lh = bone
    if bone.name == "rHand":
    	brh = bone
    if bone.name == "RightHand":
    	rh = bone

rh.parent = brh
lh.parent = blh

vecs = []

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

vec = [v[1] for i, v in enumerate(vecs) if v[0] == lh.name]
vec = vec[0]
lh.use_connect = True
lh.tail = lh.head + vec

vec = [v[1] for i, v in enumerate(vecs) if v[0] == rh.name]
vec = vec[0]
rh.use_connect = True
rh.tail = rh.head + vec

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

bodyActions = bpy.data.actions[0]
handActions1 = bpy.data.actions['left']
handActions2 = bpy.data.actions['right']

print(handActions1)
print(handActions2)

bonename = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
joint = ["Metacarpal", "Proximal", "Intermediate", "Distal", "Metacarpal.001", "Proximal.001", "Intermediate.001", "Distal.001"]

for b in bonename:
	for j in joint:
		bone = b + "_" + j
		if bone[-3:] == "001":
			rot = listRotation(handActions2, bone)
		else:
			rot = listRotation(handActions1, bone)
		addRotation(bodyActions, bone, rot)

















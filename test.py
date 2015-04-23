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
    if (bone.name == "lHand"):
        blh = bone
    if (bone.name == "LeftHand"):
        lh = bone

lh.parent = blh

# # Force attach to parent
# for bone in body.data.edit_bones:

vecs = []

for child in blh.children_recursive:
	if child.name[:1] == "l":
		body.data.edit_bones.remove(child)
	else:
		vecs.append((child.name, child.tail-child.head))

vec = [v[1] for i, v in enumerate(vecs) if v[0] == lh.name]
vec = vec[0]
lh.use_connect = True
lh.tail = lh.head + vec

for bone in lh.children_recursive:
	bone.use_connect = True
	vec = [v[1] for i, v in enumerate(vecs) if v[0] == bone.name]
	vec = vec[0]
	bone.tail = bone.head + vec

bodyActions = bpy.data.actions[0]
handActions = bpy.data.actions[1]

bonename = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
joint = ["Metacarpal", "Proximal", "Intermediate", "Distal"]

for b in bonename:
	for j in joint:
		bone = b + "_" + j
		rot = listRotation(handActions, bone)
		addRotation(bodyActions, bone, rot)

















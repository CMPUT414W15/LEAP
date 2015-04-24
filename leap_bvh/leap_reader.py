##########################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.              #
# Leap Motion proprietary and confidential. Not for distribution.             #
# Use subject to the terms of the Leap Motion SDK Agreement available at      #
# https://developer.leapmotion.com/sdk_agreement, or another agreement        #
# between Leap Motion and you, your company or other organization.            #
##########################################################################

from __future__ import print_function
import sys
import numpy as np
from bvh import createHeader, createMotion

from numpy.linalg import inv
from numpy import float64, hypot, zeros, matrix

# if you don't have the LeapSDK setup in PATH, use:
# sys.path.insert(0, "/Users/aaron_t15/Desktop/LeapSDK/lib")

import Leap


class BVHListener(Leap.Listener):
    """ A LEAP listener that writes BVH """
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def __init__(self):
        Leap.Listener.__init__(self)
        self.first_frame = 0
        self.frame_times = 0
        self.channel_data = []

    def on_exit(self, controller):
        # Calculate avg fps from # of frames and total fps
        frame_sample = 1 / (self.frame_times / len(self.channel_data))

        print(createMotion(self.channel_data, frame_sample))

    """ Convert a leap Vector class to a string """
    def vec_to_str(self, v):
        return " ".join(str(i) for i in [v.x, v.y, v.z])

    """ NumPy-ify a LEAP matrix's 3x3 array """
    def npmat(self, mat):
        return np.matrix([[mat[0], mat[1], mat[2]],
                          [mat[3], mat[4], mat[5]],
                          [mat[6], mat[7], mat[8]]])

    """ Get Euler angles as calculated in the LEAP API sample code """
    def hand_to_euler(self, normal, direction):
        pitch = direction.pitch * Leap.RAD_TO_DEG
        yaw = direction.yaw * Leap.RAD_TO_DEG
        roll = normal.roll * Leap.RAD_TO_DEG
        return "%s %s %s " % (roll, pitch, yaw)

    """ Convert 3x3 rotation matrix to euler angles """
    def rotation_to_euler(self, R):
        # old decomposition
        # yaw = np.arctan2(R[2,1], R[2,2])
        # roll = np.arctan2(-R[2,0], np.sqrt(R[2,1]*R[2,1] + R[2,2]*R[2,2]))
        # pitch = np.arctan2(R[1,0], R[0,0])

        # Algorithem from
        # http://staff.city.ac.uk/~sbbh653/publications/euler.pdf
        # xxxx1 and xxxx2 are oppsoites rotations of each other

        if R[2, 0] != 1 and R[2, 0] != -1:
            roll1 = -np.arcsin(R[2, 0])
            roll2 = np.pi - roll1

            yaw1 = np.arctan2(R[2, 1]/np.cos(roll1), R[2, 2]/np.cos(roll1))
            yaw2 = np.arctan2(R[2, 1]/np.cos(roll2), R[2, 2]/np.cos(roll2))

            pitch1 = np.arctan2(R[1, 0]/np.cos(roll1), R[0, 0]/np.cos(roll1))
            pitch2 = np.arctan2(R[1, 0]/np.cos(roll2), R[0, 0]/np.cos(roll2))

        else:
            pitch1 = pitch2 = 0
            alpha = np.arctan2(R[0, 1], R[0, 2])

            if R[2, 0] == -1:
                roll1 = roll2 = np.pi/2
                yaw1 = yaw2 = pitch1 + alpha
            else:
                roll1 = roll2 = -np.pi/2
                yaw1 = yaw2 = -pitch1 + alpha

        return "%s %s %s " % (pitch1 * Leap.RAD_TO_DEG,
                              roll1 * Leap.RAD_TO_DEG,
                              yaw1 * Leap.RAD_TO_DEG)

    def on_frame(self, controller):
        frame = controller.frame()

        for hand in frame.hands:
            # do first frame things, i.e. HIERARCHY
            if self.first_frame == 0:
                bones = [finger.bone(b)
                         for finger in hand.fingers
                         for b in range(4)]
                joints = [" ".join([finger, bone])
                          for finger in self.finger_names
                          for bone in self.bone_names]

                joints.insert(0, ("Right" if hand.is_right else "Left") + "Hand")
                vector_offsets = [bone.next_joint - bone.prev_joint
                                  for bone in bones]
                vector_offsets.insert(0, Leap.Vector(0, 0, 0))
                offsets = [self.vec_to_str(v) for v in vector_offsets]
                print(createHeader(joints, offsets))
                self.first_frame = frame.id

            # No need to capture hand location
            # Set to origin everytime
            frame_data = "0 0 0 "
            frame_data += self.hand_to_euler(hand.palm_normal, hand.direction)

            # Iterate through fingers
            for finger in hand.fingers:

                for b in range(4):
                    bone = finger.bone(b)

                    # Thumb's have no Metacarpal bone
                    # but LEAP still returns a bone with length 0
                    # which throws off Blender
                    if finger.type() == Leap.Finger.TYPE_THUMB and b == 0:
                        frame_data += "0 0 0 "
                    else:
                        #
                        mat = self.npmat(bone.basis.rigid_inverse().to_array_3x3())

                        if hand.is_left:
                            mat[:, 0] *= -1

                        frame_data += self.rotation_to_euler(mat)

            self.channel_data.append(frame_data)
            self.frame_times += frame.current_frames_per_second


def main():
    # Create a sample listener and controller
    listener = BVHListener()
    controller = Leap.Controller()

    controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    # print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()

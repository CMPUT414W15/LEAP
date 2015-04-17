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
from math import acos, atan2, cos, pi, sin
from numpy import float64, hypot, zeros, matrix

sys.path.insert(0, "/Users/Karim/LeapSDK/lib")

import Leap
class BVHListener(Leap.Listener):
    """ A LEAP listener that writes BVH """
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def __init__(self):
        Leap.Listener.__init__(self)
        self.first_frame = 0
        self.frame_times = []
        self.channel_data = []

    def on_init(self, controller):
        pass

    def on_connect(self, controller):
        pass

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        pass

    def on_exit(self, controller):
        print(createMotion(self.channel_data, sum(self.frame_times)))

    def vec_to_str(self, v):
        return " ".join(str(i) for i in [v.x, v.y, v.z])

    def npmat(self, mat):
        """ NumPy-ify a LEAP matrix's 3x3 array """
        return np.matrix([[mat[0], mat[1], mat[2]],
                          [mat[3], mat[4], mat[5]],
                          [mat[6], mat[7], mat[8]]])


    def mat_to_euler(self, mtx):
        yaw = np.arccos(mtx[2, 2])
        pitch = -np.arctan2(mtx[2, 0], mtx[2, 1])
        roll = -np.arctan2(mtx[0, 2], mtx[1, 2])

        return "%s %s %s " % (yaw * Leap.RAD_TO_DEG ,
                              pitch * Leap.RAD_TO_DEG,
                              roll * Leap.RAD_TO_DEG)

    def hand_to_euler(self, normal, direction):
        """ Get Euler angles as calculated in the LEAP API sample code """

        pitch = direction.pitch * Leap.RAD_TO_DEG
        yaw = direction.yaw * Leap.RAD_TO_DEG
        roll = normal.roll * Leap.RAD_TO_DEG
        return "%s %s %s " % (roll, pitch, yaw)

    def euler_from_rotation(self, mtx):
        # if mtx.y_basis.x > 0.998:
        #     yaw = np.arctan2(mtx.x_basis.z, mtx.z_basis.z)
        #     pitch = Math.PI/2
        #     roll = 0
        # elif mtx.y_basis.x  < -0.998:
        #     yaw = np.arctan2(mtx.x_basis.z, mtx.z_basis.z)
        #     pitch = -Math.PI/2
        #     roll = 0
        # else:
        #     yaw = np.arctan2(-mtx.z_basis.x, mtx.x_basis.x)
        #     roll = np.arctan2(-mtx.y_basis.z, mtx.y_basis.y)
        #     pitch = np.arcsin(mtx.y_basis.x)
        #
        # return "%s %s %s " % (yaw * Leap.RAD_TO_DEG ,
        #                       pitch * Leap.RAD_TO_DEG,
        #                       roll * Leap.RAD_TO_DEG)

        return "0 0 0 "

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
                joints.insert(0, "Hand")
                vector_offsets = [bone.next_joint - bone.prev_joint
                                  for bone in bones]
                vector_offsets.insert(0, Leap.Vector(0, 0, 0))
                offsets = [self.vec_to_str(v) for v in vector_offsets]
                print(createHeader(joints, offsets))
                self.first_frame = frame.id


            # right hand only?

            frame_data = "0 0 0 "

            frame_data += self.hand_to_euler(hand.palm_normal, hand.direction)

            # for finger in hand.fingers:
            #     for b in range(4):
            #         # frame_data += '0 0 0 '
            #         bone = finger.bone(b)
            #         # mat = self.npmat(bone.basis.rigid_inverse().to_array_3x3())
            #         # finger_mat = np.linalg.inv(finger_mat) * mat
            #         # yaw, roll, pitch = self.mat_to_euler(finger_mat)
            #         # print("yaw, pitch, roll", file=sys.stderr)
            #         # print(yaw, pitch, roll, file=sys.stderr)
            #         # frame_data += "%s " % (yaw)
            #         # frame_data += "%s " % (roll)
            #         # frame_data += "%s " % (pitch)
            #
            #         # if b == 3:
            #         frame_data += self.euler_from_rotation(bone.basis)
            #         # else:
            #         #     frame_data += "0 0 0 "


            # # do all frame things
            # mat = hand.basis.rigid_inverse().to_array_3x3()
            # hand_mat = self.npmat(mat)
            # frame_data = "0 0 0 "
            # frame_data += self.leap_hand_eulers(hand) + " "
            # for finger in hand.fingers:
            #     finger_mat = hand_mat
            #     for b in range(4):
            #         bone = finger.bone(b)
            #         mat = self.npmat(bone.basis.rigid_inverse().to_array_3x3())
            #         finger_mat = np.linalg.inv(finger_mat) * mat
            #         yaw, roll, pitch = self.mat_to_euler(finger_mat)
            #         print("yaw, pitch, roll", file=sys.stderr)
            #         print(yaw, pitch, roll, file=sys.stderr)
            #         frame_data += "%s " % (yaw)
            #         frame_data += "%s " % (roll)
            #         frame_data += "%s " % (pitch)

            self.channel_data.append(frame_data)
            self.frame_times.append(0.4)

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

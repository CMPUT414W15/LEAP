##########################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.              #
# Leap Motion proprietary and confidential. Not for distribution.             #
# Use subject to the terms of the Leap Motion SDK Agreement available at      #
# https://developer.leapmotion.com/sdk_agreement, or another agreement        #
# between Leap Motion and you, your company or other organization.            #
##########################################################################

import Leap
import sys
import numpy as np
from bvh import createHeader, createMotion


class BVHListener(Leap.Listener):
    """ A LEAP listener that writes BVH """
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Distal']
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
        # pass

    def on_frame(self, controller):
        """
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        #print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d,
        gestures: %d" % (
        #      frame.id, frame.timestamp, len(frame.hands), len(frame.fingers),
        #      len(frame.tools), len(frame.gestures()))

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            #print "  %s, id %d, position: %s" % (
            #    handType, hand.id, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            #print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
            #    direction.pitch * Leap.RAD_TO_DEG,
            #    normal.roll * Leap.RAD_TO_DEG,
            #    direction.yaw * Leap.RAD_TO_DEG)

            # Get arm bone
            arm = hand.arm
            #print "  Arm direction: %s, wrist position: %s, elbow position:
            %s" % (
            #    arm.direction,
            #    arm.wrist_position,
            #    arm.elbow_position)

            # Get fingers
            for finger in hand.fingers:

                #print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
                #    self.finger_names[finger.type()],
                #    finger.id,
                ##    finger.length,
                #    finger.width)

                # Get bones
            for b in range(0, 4):
                bone = finger.bone(b)
                #    print "      Bone: %s, start: %s, end: %s, direction: %s,
                #    basis: %s" % ( self.bone_names[bone.type],
                #        bone.prev_joint,
                #        bone.next_joint,
                #        bone.direction,
                #        bone.basis)
        """
        frame = controller.frame()

        def vec_to_str(v):
            return " ".join(str(i) for i in [v.x, v.y, v.z])

        def npmat(mat):
            return np.matrix(np.reshape(np.array(mat), (3, 3)))

        def mat_to_euler(_matrix):
            from math import acos, atan2, pi
            yaw = acos(_matrix[2, 2])
            pitch = -atan2(_matrix[2, 0], _matrix[2, 1])
            roll = -atan2(_matrix[0, 2], _matrix[1, 2])
            #return yaw * (180 / pi), pitch * (180 / pi), roll * (180 / pi)
            return yaw * (180 / pi), roll * (180 / pi), pitch * (180 / pi)

        def leap_hand_eulers(hand):
            normal = hand.palm_normal
            direction = hand.direction
            pitch = direction.pitch * Leap.RAD_TO_DEG
            roll = normal.roll * Leap.RAD_TO_DEG
            yaw = direction.yaw * Leap.RAD_TO_DEG
            result = " ".join(str(i) for i in [yaw, roll, pitch])
            return result

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
                vector_offsets.insert(0, Leap.Vector(0,0,0))
                offsets = [vec_to_str(v) for v in vector_offsets]
                print(createHeader(joints, offsets))
                self.first_frame = frame.id

            # do all frame things
            mat = hand.basis.rigid_inverse().to_array_3x3()
            hand_mat = np.matrix([[mat[0], mat[1], mat[2]],
                                [mat[3], mat[4], mat[5]],
                                [mat[6], mat[7], mat[8]]])

            frame_data = vec_to_str(hand.palm_position) + " " + leap_hand_eulers(hand) + " "
            for finger in hand.fingers:
                finger_mat = hand_mat
                for b in range(4):
                    if b == 1:
                        bone = finger.bone(b)
                # for bone in (finger.bone(b) for b in range(4)):
                    # print(b, "b")
                        mat = bone.basis.rigid_inverse().to_array_3x3()
                        mat = np.matrix([[mat[0], mat[1], mat[2]],
                                    [mat[3], mat[4], mat[5]],
                                    [mat[6], mat[7], mat[8]]])
                        finger_mat = np.linalg.inv(finger_mat) * mat
                        yaw, roll, pitch = mat_to_euler(finger_mat)
                        frame_data += "%s "%(yaw)
                        frame_data += "%s "%(roll)
                        frame_data += "%s "%(pitch)
                    # frame_data += " ".join(str(i) for i in [yaw, roll, pitch]) + " "

            self.channel_data.append(frame_data)
            self.frame_times.append(0.4)

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"
        if state == Leap.gesture.STATE_UPDATE:
            return "STATE_UPDATE"
        if state == Leap.gesture.STATE_STOP:
            return "STATE_STOP"
        if state == Leap.gesture.STATE_INVALID:
            return "STATE_INVALID"


def main():
    # Create a sample listener and controller
    listener = BVHListener()
    controller = Leap.Controller()

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

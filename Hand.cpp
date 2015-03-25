/******************************************************************************\
* Copyright (C) 2012-2014 Leap Motion, Inc. All rights reserved.               *
* Leap Motion proprietary and confidential. Not for distribution.              *
* Use subject to the terms of the Leap Motion SDK Agreement available at       *
* https://developer.leapmotion.com/sdk_agreement, or another agreement         *
* between Leap Motion and you, your company or other organization.             *
\******************************************************************************/

#include <iostream>
#include <string.h>
#include "Leap.h"

using namespace Leap;

class SampleListener : public Listener {
  public:
    virtual void onInit(const Controller&);
    virtual void onConnect(const Controller&);
    virtual void onDisconnect(const Controller&);
    virtual void onExit(const Controller&);
    virtual void onFrame(const Controller&);
    virtual void onFocusGained(const Controller&);
    virtual void onFocusLost(const Controller&);
    virtual void onDeviceChange(const Controller&);
    virtual void onServiceConnect(const Controller&);
    virtual void onServiceDisconnect(const Controller&);

  private:
};

const std::string fingerNames[] = {"Thumb", "Index", "Middle", "Ring", "Pinky"};
const std::string boneNames[] = {"Metacarpal", "Proximal", "Middle", "Distal"};
const std::string stateNames[] = {"STATE_INVALID", "STATE_START", "STATE_UPDATE", "STATE_END"};

void SampleListener::onInit(const Controller& controller) {
  std::cerr << "Initialized" << std::endl;
}

void SampleListener::onConnect(const Controller& controller) {
  std::cerr << "Connected" << std::endl;
  std::cout << "Frame Id, Hands, Timestamp, Extended Fingers, Tools, Gestures, "
            << "Hand Id, Hand Palm X, Y, Z, Hand Pitch, Hand Roll, Hand Yaw, Arm Direction X, Y, Z, Wrist Position X, Y, Z, Elbow Position X, Y, Z, "
            << "Thumb Id, Thumb Length, Thumb width, "
            << "Thumb Metacarpal Start X, Y, Z, Thumb Metacarpal End X, Y, Z, Thumb Metacarpal Direction X, Y, Z, "
            << "Thumb Proximal Start X, Y, Z, Thumb Proximal End X, Y, Z, Thumb Proximal Direction X, Y, Z, "
            << "Thumb Middle Start X, Y, Z, Thumb Middle End X, Y, Z, Thumb Middle Direction X, Y, Z, "
            << "Thumb Distal Start X, Y, Z, Thumb Distal End X, Y, Z, Thumb Distal Direction X, Y, Z, "
            << "Index Id, Index Length, Index Width, "
            << "Index Metacarpal Start X, Y, Z, Index Metacarpal End X, Y, Z, Index Metacarpal Direction X, Y, Z, "
            << "Index Proximal Start X, Y, Z, Index Proximal End X, Y, Z, Index Proximal Direction X, Y, Z, "
            << "Index Middle Start X, Y, Z, Index Middle End X, Y, Z, Index Middle Direction X, Y, Z, "
            << "Index Distal Start X, Y, Z, Index Distal End X, Y, Z, Index Distal Direction X, Y, Z, "
            << "Middle Id, Middle Length, Middle Width, "
            << "Middle Metacarpal Start X, Y, Z, Middle Metacarpal End X, Y, Z, Middle Metacarpal Direction X, Y, Z, "
            << "Middle Proximal Start X, Y, Z, Middle Proximal End X, Y, Z, Middle Metacarpal Direction X, Y, Z, "
            << "Middle Middle Start X, Y, Z, Middle Middle End X, Y, Z, Middle Middle Direction X, Y, Z, "
            << "Middle Distal Start X, Y, Z, Middle Distal End X, Y, Z, Middle Distal Direction X, Y, Z, "
            << "Ring Id, Ring Length, Ring Width, "
            << "Ring Metacarpal Start X, Y, Z, Ring Metacarpal End X, Y, Z, Ring Metacarpal Direction X, Y, Z, "
            << "Ring Proximal Start X, Y, Z, Ring Proximal End X, Y, Z, Ring Proximal Direction X, Y, Z, "
            << "Ring Middle Start X, Y, Z, Ring Middle End X, Y, Z, Ring Middle Direction X, Y, Z, "
            << "Ring Distal Start X, Y, Z, Ring Distal End X, Y, Z, Ring Distal Direction X, Y, Z, "
            << "Pinky Id, Pinky Length, Pinky Width, "
            << "Pinky Metacarpal Start X, Y, Z, Pinky Metacarpal End X, Y, Z, Pinky Metacarpal Direction X, Y, Z, "
            << "Pinky Proximal Start X, Y, Z, Pinky Proximal End X, Y, Z, Pinky Proximal Direction X, Y, Z, "
            << "Pinky Middle Start X, Y, Z, Pinky Middle End X, Y, Z, Pinky Middle Direction X, Y, Z, "
            << "Pinky Distal Start X, Y, Z, Pinky Distal End X, Y, Z, Pinky Distal Direction X, Y, Z" << std::endl;
  controller.enableGesture(Gesture::TYPE_CIRCLE);
  controller.enableGesture(Gesture::TYPE_KEY_TAP);
  controller.enableGesture(Gesture::TYPE_SCREEN_TAP);
  controller.enableGesture(Gesture::TYPE_SWIPE);
}

void SampleListener::onDisconnect(const Controller& controller) {
  // Note: not dispatched when running in a debugger.
  std::cerr << "Disconnected" << std::endl;
}

void SampleListener::onExit(const Controller& controller) {
  std::cerr << "Exited" << std::endl;
}

void SampleListener::onFrame(const Controller& controller) {
  // Get the most recent frame and report some basic information
  const Frame frame = controller.frame();
  if (frame.hands().count() > 0) {
    std::cout << frame.id()
              << ", " << frame.timestamp()
              << ", " << frame.hands().count()
              << ", " << frame.fingers().extended().count()
              << ", " << frame.tools().count()
              << ", " << frame.gestures().count();

    HandList hands = frame.hands();
    for (HandList::const_iterator hl = hands.begin(); hl != hands.end(); ++hl) {
      // Get the first hand
      const Hand hand = *hl;
      std::string handType = hand.isLeft() ? "Left hand" : "Right hand";
      std::cout << ", " << hand.id()
                << ", " << hand.palmPosition() << ", ";
      // Get the hand's normal vector and direction
      const Vector normal = hand.palmNormal();
      const Vector direction = hand.direction() ;

      // Calculate the hand's pitch, roll, and yaw angles
      std::cout << direction.pitch() * RAD_TO_DEG << " degrees, "
                << normal.roll() * RAD_TO_DEG << " degrees, "
                << direction.yaw() * RAD_TO_DEG << " degrees ";

      // Get the Arm bone
      Arm arm = hand.arm();
      std::cout << ", " << arm.direction()
                << ", " << arm.wristPosition()
                << ", " << arm.elbowPosition();

      // Get fingers
      const FingerList fingers = hand.fingers();
      for (FingerList::const_iterator fl = fingers.begin(); fl != fingers.end(); ++fl) {
        const Finger finger = *fl;
        std::cout << ", " << finger.id()
                  << ", " << finger.length()
                  << ", " << finger.width();

        // Get finger bones
        for (int b = 0; b < 4; ++b) {
          Bone::Type boneType = static_cast<Bone::Type>(b);
          Bone bone = finger.bone(boneType);
          std::cout << ", " << bone.prevJoint()
                    << ", " << bone.nextJoint()
                    << ", " << bone.direction();
        }
      }
    }

    // std::cout << std::endl;

    // Get tools
    const ToolList tools = frame.tools();
    for (ToolList::const_iterator tl = tools.begin(); tl != tools.end(); ++tl) {
      const Tool tool = *tl;
      std::cout << ", "<< tool.id()
                << ", " << tool.tipPosition()
                << ", " << tool.direction();
    }

    // Get gestures
    const GestureList gestures = frame.gestures();
    for (int g = 0; g < gestures.count(); ++g) {
      Gesture gesture = gestures[g];

      switch (gesture.type()) {
        case Gesture::TYPE_CIRCLE:
        {
          CircleGesture circle = gesture;
          std::string clockwiseness;

          if (circle.pointable().direction().angleTo(circle.normal()) <= PI/2) {
            clockwiseness = "clockwise";
          } else {
            clockwiseness = "counterclockwise";
          }

          // Calculate angle swept since last frame
          float sweptAngle = 0;
          if (circle.state() != Gesture::STATE_START) {
            CircleGesture previousUpdate = CircleGesture(controller.frame(1).gesture(circle.id()));
            sweptAngle = (circle.progress() - previousUpdate.progress()) * 2 * PI;
          }
          std::cout << std::string(2, ' ')
                    << "Circle id: " << gesture.id()
                    << ", state: " << stateNames[gesture.state()]
                    << ", progress: " << circle.progress()
                    << ", radius: " << circle.radius()
                    << ", angle " << sweptAngle * RAD_TO_DEG
                    <<  ", " << clockwiseness << std::endl;
          break;
        }
        case Gesture::TYPE_SWIPE:
        {
          SwipeGesture swipe = gesture;
          std::cout << std::string(2, ' ')
            << "Swipe id: " << gesture.id()
            << ", state: " << stateNames[gesture.state()]
            << ", direction: " << swipe.direction()
            << ", speed: " << swipe.speed() << std::endl;
          break;
        }
        case Gesture::TYPE_KEY_TAP:
        {
          KeyTapGesture tap = gesture;
          std::cout << std::string(2, ' ')
            << "Key Tap id: " << gesture.id()
            << ", state: " << stateNames[gesture.state()]
            << ", position: " << tap.position()
            << ", direction: " << tap.direction()<< std::endl;
          break;
        }
        case Gesture::TYPE_SCREEN_TAP:
        {
          ScreenTapGesture screentap = gesture;
          std::cout << std::string(2, ' ')
            << "Screen Tap id: " << gesture.id()
            << ", state: " << stateNames[gesture.state()]
            << ", position: " << screentap.position()
            << ", direction: " << screentap.direction()<< std::endl;
          break;
        }
        default:
          std::cout << std::string(2, ' ')  << "Unknown gesture type." << std::endl;
          break;
      }
    }

    if (!frame.hands().isEmpty() || !gestures.isEmpty()) {
      std::cout << std::endl;
    }
  }
}

void SampleListener::onFocusGained(const Controller& controller) {
  std::cerr << "Focus Gained" << std::endl;
}

void SampleListener::onFocusLost(const Controller& controller) {
  std::cerr << "Focus Lost" << std::endl;
}

void SampleListener::onDeviceChange(const Controller& controller) {
  std::cerr << "Device Changed" << std::endl;
  const DeviceList devices = controller.devices();

  for (int i = 0; i < devices.count(); ++i) {
    std::cerr << "id: " << devices[i].toString() << std::endl;
    std::cerr << "  isStreaming: " << (devices[i].isStreaming() ? "true" : "false") << std::endl;
  }
}

void SampleListener::onServiceConnect(const Controller& controller) {
  std::cerr << "Service Connected" << std::endl;
}

void SampleListener::onServiceDisconnect(const Controller& controller) {
  std::cerr << "Service Disconnected" << std::endl;
}

int main(int argc, char** argv) {
  // Create a sample listener and controller
  SampleListener listener;
  Controller controller;

  // Have the sample listener receive events from the controller
  controller.addListener(listener);

  if (argc > 1 && strcmp(argv[1], "--bg") == 0)
    controller.setPolicy(Leap::Controller::POLICY_BACKGROUND_FRAMES);

  // Keep this process running until Enter is pressed
  std::cerr << "Press Enter to quit..." << std::endl;
  std::cin.get();

  // Remove the sample listener when done
  controller.removeListener(listener);

  return 0;
}

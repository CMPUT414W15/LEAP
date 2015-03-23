from pyfbsdk import *

def DeselectAll():
    for model in FBSystem().Scene.Components:
        model.Selected = False

def SelectBranch(topModel):
    '''
    Selects the given model and all of its descendants. Note that this
    function does not clear the current selection -- that's the caller's
    responsibility, if desired.
    '''
    for childModel in topModel.Children:
        SelectBranch(childModel)

    topModel.Selected = True

def SetScaling(animationNode):
    '''
    iterates through all the animation nodes Nodes(which indicates by x node[0],
    y node[1], and z node[2] and add key frames to them which scales the model
    up from default size to 5x the size towards the end of the animation
    '''
    if len(animationNode.Nodes) != 0:
        startTime = FBSystem().CurrentTake.LocalTimeSpan.GetStart()
        stopTime = FBSystem().CurrentTake.LocalTimeSpan.GetStop()    
        for dirNode in animationNode.Nodes:
            '''
            We can actually get fancier in here and add key frames to each second
            this requires intervals to be keyed instead of just a beginning and an end
            '''
            dirNode.FCurve.KeyAdd(startTime, 1.0)
            dirNode.FCurve.KeyAdd(stopTime, 5.0)
        
def ScaleChild( model ):
    '''
    models normally have scaling, rotation and translation animation nodes 
    which we can manipulate
    '''
    SetScaling(model.Scaling.GetAnimationNode())
    for child in model.Children:
        ScaleChild(child)



def main():
    '''
    in order to work with the models we must select them first? 
    '''
    DeselectAll()
    
    rightHand = FBFindModelByLabelName('BVH:rHand')
    SelectBranch(rightHand)
    
    leftHand = FBFindModelByLabelName('BVH:lHand')
    SelectBranch(leftHand)
    
    selectedModels = FBModelList()
    FBGetSelectedModels(selectedModels)
    
    for model in selectedModels:
        ScaleChild(model)

if __name__ in ('__main__', '__builtin__'):
    main()

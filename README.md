# LEAP

# Running

From a terminal session

## Record data
Record right hand
```
python2 leap_reader.py > left.bvh
```

Record left hand
```
python2 leap_reader.py > right.bvh
```

## Import into Blender

After importing run the following from the Blender's console
```
x = Scaler("name of body BVH", "left", "right")
x.scaleBothHands()
```

## Press Play!

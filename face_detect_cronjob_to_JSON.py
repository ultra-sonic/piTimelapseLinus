#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Face detection library demo.

 - Takes an input image and tries to detect faces.
 - Draws bounding boxes around detected objects.
 - Saves an image with bounding boxes around detected objects.
"""
# import argparse
import io
import sys
import os
import json
from PIL import Image
# from PIL import ImageDraw

from aiy.vision.inference import ImageInference
from aiy.vision.models import face_detection
import glob
import shutil

def main():
    # allImages=glob.glob( "/home/pi/Linus_Timelapse/20190326*/*.jpg" )
    # allDirs=glob.glob( "/home/pi/Linus_Timelapse/20*" )
    allDirs=glob.glob("/starscream/data_100G/Linus_Timelapse/faces/201*")
    for imageDir in sorted( allDirs, reverse=True ):  # reverse is only for very many dirs were I'd like to see the newest images processed first
        if os.path.isdir(imageDir):
            jsonLogPath=os.path.join(imageDir,"aiyJoyDetectorLog.json")
            print(jsonLogPath)
            data={}
            if os.path.isfile( jsonLogPath ):
                with open(jsonLogPath, 'r') as jsonFile:
                    data=json.load( jsonFile )
                print("File read from disk!")
            else:
                print("File created!")
            allImages=glob.glob(os.path.join(imageDir,"*.jpg")) # full of faces
            for argsinput in sorted( allImages, reverse=True ):
                basename=os.path.basename( argsinput )
                if basename in data.keys():
                    print("Already processed: " + argsinput )
                    continue

                with ImageInference(face_detection.model()) as inference:
                    # 3280x2465 - crop to 0.3,0.05,0.6,0.8 = 
                    cropMask = ( 984, 239, 2821, 2049 ) # no crop because we keep the whole image for now
                    scale=0.5
                    rotate=270
                    image = Image.open( argsinput)\
                                 .crop( cropMask )\
                                 .resize((int((cropMask[2]-cropMask[0])*scale),\
                                          int((cropMask[3]-cropMask[1])*scale)))\
                                 .rotate(rotate,Image.NEAREST)

                    # draw = ImageDraw.Draw(image)
                    
                    # debug only
                    # image.save( "/starscream/data_100G/Linus_Timelapse/debug/"+basename, format='JPEG' )
                    
                    joyscore = -1.0
                    faces=face_detection.get_faces(inference.run(image))
                    # print(faces)
                    if faces:
                        faceDict=dict()
                        for i, face in enumerate( faces ):
                            print('FOUND FACE #%d: %s' % (i, str(face)))
                            x, y, width, height = face.bounding_box
                            # draw.rectangle((x, y, x + width, y + height), outline='red')
                            # print (str(face))
                            faceDict["cropMask"]=cropMask
                            faceDict["scale"]=scale
                            faceDict["rotate"]=rotate
                            faceDict["joy_score"]=face.joy_score
                            faceDict["face_score"]=face.face_score
                            faceDict["bounding_box"]=face.bounding_box
                            break # exit after first face
                        data[ basename ]=faceDict
                        print ("            {0}".format(basename))
                    else:
                        data[ basename ]={}
                        # print ("No face in: " + basename )
                        if "/home/pi/Linus_Timelapse/" in argsinput: # do not move files from starscream - only local files go to trash
                            shutil.move( argsinput, "/home/pi/Linus_Timelapse/trash/" )
                    
                    with open(jsonLogPath, 'w') as jsonFile:
                      json.dump(data, jsonFile, sort_keys=True, indent=4)


if __name__ == '__main__':
    main()

'''
Created on Mar 29, 2017

@author: Max
'''
import Tree
from Tree import  Node
import cozmo
from cozmo.util import  distance_mm, speed_mmps, Speed, degrees, Pose
from cozmo.objects import   CustomObject, CustomObjectMarkers, CustomObjectTypes
import time
import math
from random import randint
from numpy.core.defchararray import center


#set number of columns
MAZECOLS=3
#set number of rows here
MAZEROWS=3

#set wall length here mm
WALLLENGTH=160

#set wall height here mm
WALLHEIGHT=80

#set nudge amount here
NUDGE=25

#set algorithm here: PLEDGE, RANDOM, TREMAUX, WALLFOLLOW, TEST
ALGORITHM="PLEDGE"

#set start row here
STARTROW=0
#set start col here
STARTCOL=3

#set tolerance here (degrees)
ANGLETOLERANCE=1

start=time.time()
moveCount=0
class NavStat:
    
    
    def __init__(self, startCol, startRow, startOrient):
        self.col=startCol
        self.row=startRow
        self.orient=startOrient
        self.startCol=startCol
        self.startRow=startRow
        
        self.navMaze=Tree.Maze()
        self.navMaze.create(MAZECOLS,MAZEROWS);
        self.navMaze.printCoords()
        
    def getOrient(self):
        return self.orient;
        
    def getRow(self):
        return self.row;
        
    def getCol(self):
        return self.col;
        
    def rotate90CCW(self):
        if self.orient=="up":
            self.orient="left"
            
        elif self.orient=="left":
            self.orient="down"
                
        elif self.orient=="down":
            self.orient="right"
                
        elif self.orient=="right":
            self.orient="up"
                
                
    def rotate90CW(self):
        if self.orient=="up":
            self.orient="right"
            
        elif self.orient=="left":
            self.orient="up"
                
        elif self.orient=="down":
            self.orient="left"
                
        elif self.orient=="right":
            self.orient="down"
                
    def advance(self):
        validMove=0
        currNode=self.navMaze.get(self.col, self.row);
        print("moving from: ",currNode.col, currNode.row)
        if self.orient=="up":
            if currNode.up:
                validMove=1
                self.row=self.row-1
            
        elif self.orient=="right":
            if currNode.right:
                validMove=1
                self.col=self.col+1
                    
        elif self.orient=="down":
            if currNode.down:
                validMove=1
                self.row=self.row+1
            
        elif self.orient=="left":
            if currNode.left:
                validMove=1
                self.col=self.col-1
                
        return validMove
        moveCount+=1
    
    def detectedWall(self):
        currNode=self.navMaze.get(self.col, self.row)
        self.navMaze.wallOff(currNode, self.orient)

#make sure you are not at start when testing this        
    def checkComplete(self):
        currNode=self.navMaze.get(self.col, self.row)
        if currNode.isExt==1 and self.isStart()==0:
            return 1
        else:
            return 0
        
    def isStart(self):
        if self.col==self.startCol and self.row==self.startRow:
            return 1
        else:
            return 0
    def checkJunct(self):
        currNode=self.navMaze.get(self.col, self.row)
        junction=currNode.isJunct
        print ("test junction: ", junction)
        return junction
    
    def setJunct(self, set):
        currNode=self.navMaze.get(self.col, self.row)
        currNode.setJunct(set)
        
    def retreat(self):
        validMove=0
        currNode=self.navMaze.get(self.col, self.row);
        if self.orient=="up":
            if currNode.down:
                self.row=self.row+1
                validMove=1
                
        elif self.orient=="right":
            if currNode.left:
                    self.col=self.col-1
                    validMove=1
                        
        elif self.orient=="down":
            if currNode.up:
                    self.row=self.row-1
                    validMove=1
                
        elif self.orient=="left":
            if currNode.right:
                    self.col=self.col+1
                    validMove=1
                        
        if validMove==0:
            print("invalid move")
                
        else:
            print("retreating")
            
        return validMove
    
    #retests senses at revisited walls, adding speed and lessening alignment error
    def senseCheck(self):
        wallPresent=0
        currNode=self.navMaze.get(self.col, self.row)
        if(self.orient=="up"):
            if not currNode.up:
                wallPresent=1
        elif(self.orient=="down"):
            if not currNode.down:
                wallPresent=1
        elif(self.orient=="left"):
            if not currNode.left:
                wallPresent=1
        elif(self.orient=="right"):
            if not currNode.right:
                wallPresent=1
                
        return wallPresent
    
    def markEntry(self):
        currNode=self.navMaze.get(self.col, self.row)
        if(self.orient=="up"):
            currNode.down.iterateMarks()
            marks=currNode.down.retMark()
           
        elif(self.orient=="down"):
            currNode.up.iterateMarks()
            marks=currNode.up.retMark()
        elif(self.orient=="left"):
            currNode.right.iterateMarks()
            marks=currNode.right.retMark()
        elif(self.orient=="right"):
            currNode.left.iterateMarks()
            marks=currNode.left.retMark()
            
            return marks
            
        
    
    def retMarks(self):
        currNode=self.navMaze.get(self.col, self.row)        
        marks=currNode.retMark()
        
    def getNeighborMarks(self):
        print("you're here!")
        testNode=None
        marks=0
        if(self.orient=="up"):
            testNode=self.navMaze.get(self.col, self.row-1)

            print("marks: ", marks)
        elif(self.orient=="down"):
            testNode=self.navMaze.get(self.col, self.row+1)

            print("marks: ", marks)
        elif(self.orient=="left"):
            testNode=self.navMaze.get(self.col-1, self.row)

        elif(self.orient=="right"):
            testNode=self.navMaze.get(self.col+1, self.row)

            marks=testNode.retMark()
            
            return marks;
    
    def iterateMarks(self):
        currNode=self.navMaze.get(self.col, self.row)
        currNode.iterateMarks
     
def handle_object_appeared(evt, **kw):
    if isinstance(evt.obj, CustomObject):
        print ("Cozmo started seeing a ", str(evt.obj.object_type))
        
        
                   
def cozmo_program(robot: cozmo.robot.Robot):
    robot.add_event_handler(cozmo.objects.EvtObjectAppeared, handle_object_appeared)
    robot.world.image_annotator.add_static_text('text', ALGORITHM)
    Nav1=NavStat(STARTCOL,STARTROW,"down")

    # set cozmo headAngle
    robot.set_head_angle(degrees(16)).wait_for_completed()
    #test wall 1 definition
    mazeWall=robot.world.define_custom_wall(CustomObjectTypes.CustomType02, CustomObjectMarkers.Circles2, WALLLENGTH,WALLHEIGHT,60,30,False)
    
    
    
        
    
    #connect data to action
    class DriveImplementation:
        
        
        
        def __init__(self):
            self.complete=0
            self.couresCorrect=0
            self.preRot=None
            self.postRot=None
            self.error=cozmo.util.radians(0)
            
        def rotate90CW(self):
            preTurn=robot.pose.rotation.angle_z
            print (preTurn)
            Nav1.rotate90CW()
            robot.turn_in_place(degrees(-90)).wait_for_completed()
            postTurn=robot.pose.rotation.angle_z
            self.courseCorrection(preTurn,postTurn)
            #self.courseCorrect()
            
            
            print("robot is facing", Nav1.orient)
            
        def rotate90CCW(self):
            preTurn=robot.pose.rotation.angle_z
            Nav1.rotate90CCW()
            robot.turn_in_place(degrees(90)).wait_for_completed()
            postTurn=robot.pose.rotation.angle_z
            self.courseCorrection(preTurn,postTurn)
           
            #self.courseCorrect()
            print("robot is facing", Nav1.orient)
            
        def advance(self):
            validDest=Nav1.advance()
            if validDest==1: 
                robot.drive_straight(distance_mm(WALLLENGTH+12),speed_mmps(55)).wait_for_completed()
                print("advancing")
                print(robot.pose.position)
                
        def retreat(self):
            validDest=Nav1.retreat()
            if validDest==1:
                robot.drive_straight(distance_mm(-150),speed_mmps(55)).wait_for_completed()
        
        def sense(self):
            if(Nav1.senseCheck()==1):
                return 1
            
            self.nudgeBack()
            walls=robot.world.wait_until_observe_num_objects(num=1, object_type=None, timeout=1)
            robot.drive_straight(distance_mm(NUDGE),speed_mmps(50)).wait_for_completed()
            detected=0
            wallPos=None
            for wall in walls:
                wallPos=wall.pose
                roboPos=robot.pose
                translation=wallPos-roboPos
                dist=translation.position.x
                detected=0
                print(dist)
                #register close walls only
                if dist<WALLLENGTH:
                    detected=1
                    Nav1.detectedWall()
                    
            return detected
        
        #
        def checkJunct(self):
            check=Nav1.checkJunct()
            print("check ", check)
            numWalls=0
            if(check==0):
                numWalls+=self.sense()
                self.rotate90CCW()
                numWalls+=self.sense()
                self.rotate90CW()
                self.rotate90CW()
                numWalls+=self.sense()
                self.rotate90CCW()
                if(numWalls<2):
                    Nav1.setJunct(1)
                    return 1
                else:
                    Nav1.setJunct(-1)
                    return 0
                
        def courseCorrection(self, preRotation, postRotation):
            testTurns=0
            tolerance=cozmo.util.radians(ANGLETOLERANCE*math.pi/180)
            negTol=cozmo.util.radians(-1*ANGLETOLERANCE*math.pi/180)
            localPost=postRotation
            localPre=preRotation
            if(postRotation<cozmo.util.degrees(0)):
                localPost=postRotation+degrees(360)
                print("modified angle ",localPost)
            if(preRotation<cozmo.util.degrees(0)):
                localPre=preRotation+degrees(360)
                print("modified angle ",localPre)   
        
            print(localPre)
            print(localPost)     
            dif=localPost-localPre
            print("difference ",dif )
            if(dif>degrees(180)):
                dif=dif-degrees(180)
            elif(dif<degrees(-180)):
                dif=dif+degrees(180)
            
            if dif<cozmo.util.radians(0):
                self.error-=(cozmo.util.radians(math.pi/2)+dif)
            else:
                self.error+=(cozmo.util.radians(math.pi/2)-dif)
                
            print("error is: ",self.error)
            print("difference ",dif )
            if(self.error>tolerance or self.error<negTol):
                print("correcting error")
                robot.turn_in_place(self.error).wait_for_completed()
                
                print("correction angle: ",robot.pose.rotation.angle_z)
                self.error=cozmo.util.radians(0)               
                    
            
       
        
        #getting into camera range   
        def nudgeBack(self):
            robot.drive_straight(distance_mm(-NUDGE),speed_mmps(50)).wait_for_completed()
                
            
            
                
    driveFunct=DriveImplementation()
    
    
    #RANDOM algorithm
    if ALGORITHM=="RANDOM":
        end=0
        driveFunct.advance()
        while end==0:
            if Nav1.isStart()==1:
                driveFunct.preRot=robot.pose.angle_z
                driveFunct.reverse()
            else:
                end=Nav1.checkComplete()
                
            if end==1:
                break
            #direction picker 
            else:
                validDir=0
                leftvalid=1
                rightvalid=1
                centervalid=1
                while(validDir==0):
                    dirPick=randint(0,2)
                    print(dirPick)
                    if(centervalid==1 and dirPick==0):
                        ("testing forward")
                        wallD=driveFunct.sense()
                        centervalid-=wallD
                        if(centervalid==1):
                            validDir=1
                            
                        else:
                            centervalid=0
                            
                    elif(leftvalid==1 and dirPick==1):
                        print("testing left")
                        driveFunct.rotate90CCW()
                        wallD=driveFunct.sense()
                        leftvalid-=wallD
                        if(leftvalid==1):
                            validDir=1
                            
                        else:
                            leftvalid=0
                            driveFunct.rotate90CW()
                            
                    elif(rightvalid==1 and dirPick==2):
                        print("testing right")
                        driveFunct.rotate90CW()
                        wallD=driveFunct.sense()
                        rightvalid-=wallD
                        if(rightvalid==1):
                            validDir=1
                            
                            
                        else:
                            rightvalid=0
                            driveFunct.rotate90CCW()
                            
                    elif(rightvalid==0 and center==0 and leftvalid==0):
                        driveFunct.rotate90CCW()
                        driveFunct.rotate90CCW()
                        validDir=1
                
                driveFunct.advance()
        
    #left-wall pledge
    if(ALGORITHM=="PLEDGE"):
        end=0
        driveFunct.advance()
        while end==0:
            end=Nav1.checkComplete()
            if(end==1):
                break
            wallD=0
        #advance until detected
            while wallD==0:
                wallD=driveFunct.sense()
                if(wallD==0):
                    driveFunct.advance()
                    
            heading=0
            #heading into pledge body
            if(wallD!=0):
                turnSum=0
                driveFunct.rotate90CW()
                heading-=90
                turnSum-=1
                while(heading!=0 or turnSum!=0)and end==0:
                    driveFunct.rotate90CCW()
                    print("heading: ", heading, "turnSum ", turnSum)
                    wallD=0
                    wallD=driveFunct.sense()
                    heading+=90
                    turnSum+=1
                    if(wallD==0):
                        driveFunct.advance()
                        end=Nav1.checkComplete()
                    else:
                        driveFunct.rotate90CW()
                        heading+= -90
                        turnSum-=1
                        print("heading: ", heading, "turnSum ", turnSum)
                        wallD=driveFunct.sense()
                        if(wallD==0):
                            driveFunct.advance()
                            end=Nav1.checkComplete()
                        else:
                            driveFunct.rotate90CW()
                            heading+= -90
                            turnSum-=1    
                            wallD=driveFunct.sense()
                            print("heading: ", heading, "turnSum ", turnSum)
                            if(wallD==0):
                                driveFunct.advance()
                                end=Nav1.checkComplete()
                        
                        if(heading==360 or heading==-360):
                            heading=0
                        

       
                        
                
        
    #left-hand wall follow  
    if ALGORITHM=="WALLFOLLOW":
        driveFunct.advance()
        end=0
        while end==0:
            end=Nav1.checkComplete()
            if end==1:
                break
            
            wallD=0
            driveFunct.rotate90CCW()
            wallD=driveFunct.sense()
            if(wallD==0):
                driveFunct.advance()
            else:
                driveFunct.rotate90CW()
                wallD1=0
                wallD1=driveFunct.sense()
                print(wallD1)
                if(wallD1==0):
                    driveFunct.advance()
                else:
                    wallD2=0
                    driveFunct.rotate90CW()
                    wallD2=driveFunct.sense()
                    if(wallD2==0):
                        driveFunct.advance()
   
        
    end=time.time()
    elapsed=end-start
    f=open("Timings.txt", "a+")
    f.write("%s %d %d %5.2f \n" % (ALGORITHM, MAZECOLS, MAZEROWS, elapsed ))
    f.close()
    print("time elapsed ", elapsed)
    anim=robot.play_anim_trigger(cozmo.anim.Triggers.MajorWin)
    anim.wait_for_completed()    
            



                
   
   
    
  #  driveFunct.rotate90CCW()
  #  driveFunct.rotate90CW()
  #  driveFunct.advance()
 #   driveFunct.retreat()


cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)       
            
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
from _ast import Mult

#set number of columns
MAZECOLS=5
#set number of rows here
MAZEROWS=5

#set wall length here mm
WALLLENGTH=160

#set wall height here mm
WALLHEIGHT=80

#set algorithm here: PLEDGE, COINFLIP, TREMAUX, WALL FOLLOW, TEST
ALGORITHM="TEST"
        
class NavStat:
    
    
    def __init__(self, startCol, startRow, startOrient):
        self.col=startCol
        self.row=startRow
        self.orient=startOrient
        self.startCol=startCol
        self.startRow=startRow
        
        self.navMaze=Tree.Maze();
        self.navMaze.create(MAZECOLS,MAZEROWS);
        
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
        print(currNode.col, currNode.row)
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
    
    def detectedWall(self):
        currNode=self.navMaze.get(self.col, self.row)
        self.navMaze.wallOff(currNode, self.orient)

#make sure you are not at start when testing this        
    def checkComplete(self):
        currNode=self.navMaze.get(self.col, self.row)
        if currNode.isExt==1:
            return 1
        else:
            return 0
        
    def isStart(self):
        if self.col==self.startCol and self.row==self.row:
            return 1
        else:
            return 0
               
           # def driveProg(robot: cozmo.robot.Robot):       
           #     robot.drive_straight(distance_mm(150),speed_mmps(50)).wait_for_completed()
                
            #cozmo.run_program(driveProg)
                        
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
     



     
def handle_object_appeared(evt, **kw):
    if isinstance(evt.obj, CustomObject):
        print ("Cozmo started seeing a ", str(evt.obj.object_type))
        
        
                   
def cozmo_program(robot: cozmo.robot.Robot):
    robot.add_event_handler(cozmo.objects.EvtObjectAppeared, handle_object_appeared)
    robot.world.image_annotator.add_static_text('text', ALGORITHM)
    Nav1=NavStat(1,0,"down")

    # set cozmo headAngle
    robot.set_head_angle(degrees(10)).wait_for_completed()
    #test wall 1 definition
    mazeWall=robot.world.define_custom_wall(CustomObjectTypes.CustomType02, CustomObjectMarkers.Circles2, WALLLENGTH,WALLHEIGHT,60,30,False)
    
    
    
        
    
    #connect data to action
    class DriveImplementation:
        
        globalTurn=0
        
        def __init__(self):
            self.complete=0
            
        def rotate90CW(self):
            Nav1.rotate90CW()
            robot.turn_in_place(90)
            rot=robot.pose.rotation.angle_z
            print(rot)
            #self.courseCorrect()
            
            
            print("robot is facing", Nav1.orient)
            self.globalTurn-=1
            if(self.globalTurn==-4):
                self.globalTurn=0
            
            
        def rotate90CCW(self):
            Nav1.rotate90CCW()
            robot.turn_in_place(90)
            self.globalTurn+=1
            if(self.globalTurn==4):
                self.globalTurn=0
            
            rot=robot.pose.rotation
            print(rot)
            #self.courseCorrect()
            print("robot is facing", Nav1.orient)
            
        def advance(self):
            validDest=Nav1.advance()
            if validDest==1: 
                robot.drive_straight(distance_mm(WALLLENGTH+20),speed_mmps(50)).wait_for_completed()
                
        def retreat(self):
            validDest=Nav1.retreat()
            if validDest==1:
                robot.drive_straight(distance_mm(-150),speed_mmps(50)).wait_for_completed()
        
        def sense(self):
            self.nudgeBack()
            walls=robot.world.wait_until_observe_num_objects(num=1, object_type=None, timeout=2)
            robot.drive_straight(distance_mm(12),speed_mmps(50)).wait_for_completed()
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
               
               
               
               
            
                

                
        def reverse(self):
            self.rotate90CCW()
            self.rotate90CCW()
        
        
        #getting into camera range   
        def nudgeBack(self):
            robot.drive_straight(distance_mm(-12),speed_mmps(50)).wait_for_completed()
                
            
            
                
    driveFunct=DriveImplementation()
    
    #algorithm selector, add new entries here
    def algorithmSelect():
        if ALGORITHM=="COINFLIP":
            coinFlip()
        if ALGORITHM=="TEST":
            test()
    
    #coinflip algorithm
    def coinFlip():
        end=0
        driveFunct.advance()
        while end==0:
            if Nav1.isStart()==1:
                driveFunct.reverse()
            else:
                end=Nav1.checkComplete()
                
            if end==1:
                break
            else:
                direction=randint(0,1)
                wallD=driveFunct.sense()
                if wallD==1:
                    if(direction==1):
                        driveFunct.rotate90CCW()
                    else:
                        driveFunct.rotate90CW()                        
                driveFunct.advance()
        
    
    def pledge():
        end=0
        heading=0
        #1 for CW, -1 for CCW initialized to CW, can reverse if you want
        direction=1
          
        driveFunct.advance()
        while end==0:
            end=Nav1.checkComplete()
            if(end==1):
                break
            wallD=driveFunct.sense()
            if wallD==1:
                if(direction==-1):
                    driveFunct.rotate90CW()
                    heading+=90
                    if(heading==360):
                        direction*=-1
                        heading=0
                elif(direction==1):
                    driveFunct.rotate90CCW()
                    heading+=90
                    if(heading==360):
                        direction*=-1
                        heading=0
            else:
                driveFunct.advance()
                
    #tests alignment, detection etc
    def test():
        driveFunct.advance()
        driveFunct.rotate90CW()
        driveFunct.rotate90CW()
        


    algorithmSelect()

                
   
   
    
  #  driveFunct.rotate90CCW()
  #  driveFunct.rotate90CW()
  #  driveFunct.advance()
 #   driveFunct.retreat()


cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)       
            
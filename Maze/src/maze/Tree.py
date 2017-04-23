


class Node:

	def __init__(self, ext, col, row, up, down, left, right):
		self.up=up
		self.down=down
		self.left=left
		self.right=right
		#preserves connections for data access
		self.datUp=up
		self.datDown=down
		self.datLeft=left
		self.datRight=right
		
		self.col=col
		self.row=row
		self.isExt=ext
		self.isJunct=0
		self.marks=0
		
		
		
		
	
	def retMark(self):
		print("you made it! ",self.marks)
		return self.marks
	
	def sever(self, direct):
		self.direct=direct
		if direct=="left":
			self.left=None
		elif direct=="right":
			self.right=None
		elif direct=="up":
			self.up=None
		else:
			self.down=None
	 
	def iterateMarks(self): 
		self.marks+=1	  
	
	def retExt(self):
		return self.isExt==1
	
	#set if a node is a junction, -1 for undiscovered, 0 for no, 1 for yes
	def setJunct(self, set):
		self.isJunct=set

	
class Maze:
	def __init__(self):
		self.root=0
		self.NUMCOL=2
		self.NUMCOL=0
		self.NUMROW=0
		self.NUMROW=0

		
	def add(self):
		if self.root:
			self._add(self.root, 0, 0)
		else:
			self.root=Node(1,0,0,None,None,None,None)
		
			
	def _add(self, currNode, col, row):
		
		if row==0 or row==self.NUMROW-1 or col==0 or col==self.NUMCOL-1:
			currNode.isExt=1
		
		if(col==0 and row<self.NUMROW-1 and not currNode.down):
			#add new row
			currNode.down=Node(1,col,row+1, currNode, None, None, None)
			currNode.datDown=currNode.down
  
		elif col==self.NUMCOL-1:
			#move down
			if(row!=self.NUMROW-1):
				self._add((self.get(0,row+1)),0, row+1)
				
				
		else:
			if  not currNode.right:
				currNode.right=Node(0, col+1, row, None, None, currNode, None)
				currNode.datRight=currNode.right
				if row!=0:
					currNode.up=self.get(col, row-1)
					currNode.datUp=currNode.up
					currNode.up.down=currNode
					currNode.up.datDown=currNode 
				#end format
				if currNode.right.col==(self.NUMCOL-1):
					currNode.right.isExt=1
			elif col<(self.NUMCOL-1):
				self._add(currNode.right, col+1, row)
				
				
		#time to move to next row
	
	def get(self, col, row):
		if self.root.col==col and self.root.row==row:
			return self.root
		else:
			return self._get(self.root, col, row)
			
	def _get(self, currNode, col, row):
		if currNode.row<row:
			if currNode.datDown:
				return self._get(currNode.datDown, col, row)
			else:
				print("y value out of bounds")
		
		if currNode.col<col:
			if currNode.datRight:
				return self._get(currNode.datRight, col, row)
			else:
				print("x value out of bounds")
		if currNode.row==row and currNode.col==col:
			return currNode

	def create(self, cols, rows):
			self.NUMCOL=cols+2
			self.NUMROW=rows+2
			y=0
			for y in range (0, self.NUMROW):
				x=0
				for x in range (0, self.NUMCOL):
					self.add()
					
	def printCoords(self):
		y=0
		for y in range(0, self.NUMROW):
			x=0
			for x in range(0, self.NUMCOL):
				currNode=self.get(x,y)
				if currNode.isExt==1:
					print("ext", end=" ")
				else:
					print(currNode.col, ",",currNode.row, sep="", end=" ")	
			 
			print("")		  
			
		  
	def wallOff(self, entryNode, direction):
		if direction=="up" and entryNode.up:
			entryNode.up.sever("down")
			entryNode.sever("up")
		elif direction=="down" and entryNode.down:
			entryNode.down.sever("up")
			entryNode.sever("down")
		elif direction=="left" and entryNode.left:
			entryNode.left.sever("right")
			entryNode.sever("left")
		elif direction=="right" and entryNode.right:
			entryNode.right.sever("left")
			entryNode.sever("right")
			
		print ("wall added")
			

        
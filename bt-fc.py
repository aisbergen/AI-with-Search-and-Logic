#!/usr/bin/env python3

#  Answer for both the constraint solving labs of AIPS

#  This model answer differs slightly from the lab sheets: copies of domains
#  for backtracking are stored inside the Domains object rather than being
#  managed by the fc method. 
#  Also, domains are not printed during search. 
#  The program does a complete search and outputs all 4 solutions.

import copy
import sys

class Domains:
    def __init__(self, n, d):
        self.n=n
        self.d=d
        self.domains=[ [True for j in range(d)] for i in range(n) ]
        self.btstack=[]
    
    #  Domains are 1..d,  domains list indexed 0..d-1
    def domainAsList(self, i):
        return [ a+1 for a in range(self.d) if self.domains[i-1][a] ]
    
    def removeFromDomain(self, i, di):
        self.domains[i-1][di-1]=False
    
    def empty(self, i):
        return sum(self.domains[i-1])==0
    
    def checkpoint(self):
        #  Store copy of current domain state
        self.btstack.append(copy.deepcopy(self.domains))
    
    def restore(self):
        # Restore last domain state saved on stack. 
        self.domains=self.btstack[-1]
        self.btstack=self.btstack[:-1]
        
    def assign(self, i, di):
        assert(self.domains[i-1][di-1])
        for val in range(1, self.d+1):
            if val!=di:
                self.domains[i-1][val-1]=False
    
    def display(self):
        for i in range(self.n):
            for di in range(self.d):
                if self.domains[i][di]:
                    print(str(di+1)+" ", end=" ")
                    break
        print("")

class Constraints:
    def __init__(self, n, d):
        # Fill in the 'true' constraint by default. 
        self.cons=[ [ [ (di, dj) for di in range(1, d+1) for dj in range(1, d+1) ] for j in range(n) ] for i in range(n) ]
        
    def setConstraint(self, i, j, tupleList):
        self.cons[i-1][j-1]=tupleList
    
    def getSatisfyingTuples(self, i, j):
        return self.cons[i-1][j-1]

class Search:
    
    def reviseAC3(self, i, j):
        changed=False
        
        for di in self.dom.domainAsList(i):
            supported=False
            
            for dj in self.dom.domainAsList(j):
                if (di,dj) in self.cons.getSatisfyingTuples(i,j): 
                    supported=True
                if supported:
                    break
            
            if not supported:
                self.dom.removeFromDomain(i, di)
                changed=True
                
        return not self.dom.empty(i)
    
    def check(self, i, j):
        Di=self.dom.domainAsList(i)
        Dj=self.dom.domainAsList(j)
        assert(len(Di)==1)
        assert(len(Dj)==1)
        return (Di[0], Dj[0]) in self.cons.getSatisfyingTuples(i,j)
    
    #  Backtrack. The depth parameter indicates the current variable for branching (from 1 to n)
    def bt(self, depth):
        for value in self.dom.domainAsList(depth):
            self.dom.checkpoint()  #  Somehow mark or copy the current state of the domains so they can be restored. 
            
            self.dom.assign(depth, value)
            
            print("BT Assigned: x"+str(depth)+"="+str(value))
            
            consistent=True
            for past in range(1, depth):
                consistent = self.check(depth, past)  #  Check arc from current variable to past variable.
                
                if not consistent:
                    break
            
            if consistent:    
                if depth==self.n:
                    print("Solution: ")
                    self.dom.display()
                    # sys.exit()   #  Exit after first solution
                else:
                    self.bt(depth+1)   # Recursive call to continue search at depth+1
                print("Backtracking: x"+str(depth)+"="+str(value))
            
            self.dom.restore()  #  Restore the state of the variable domains to the last checkpoint. 
            #  This includes undoing the assignment that occurred after the last checkpoint. 
    
    #  Forward checking. The depth parameter indicates the current variable for branching (from 1 to n)
    def fc(self, depth):
        for value in self.dom.domainAsList(depth):
            self.dom.checkpoint()  #  Somehow mark or copy the current state of the domains so they can be restored. 
            
            self.dom.assign(depth, value)
            
            print("FC Assigned: x"+str(depth)+"="+str(value))
            
            consistent=True
            for future in range(depth+1, self.n+1):
                consistent = self.reviseAC3(future, depth)  #  Revise arc from future variable to current variable.
                
                if not consistent:
                    break
            
            if consistent:
                if depth==self.n:
                    print("Solution: ")
                    self.dom.display()
                    # sys.exit()   #  Exit after first solution
                else:
                    self.fc(depth+1)   # Recursive call to continue search at depth+1
                print("Backtracking: x"+str(depth)+"="+str(value))
            
            self.dom.restore()  #  Restore the state of the variable domains to the last checkpoint. 
            #  This includes undoing the assignment that occurred after the last checkpoint. 
    
    #  Set up crystal maze
    def setup(self):
        self.n=8
        self.dom=Domains(8,8)
        self.cons=Constraints(8,8)
        
        # List of pairs of vertices that are adjacent in the original Crystal Maze graph
        # Each pair in only one direction. 
        adjacentEdges=[ (1,2), (1,3), (1,4), (1,5), (2,4), (2,5), (2,6), (3,4), (3,7), (4,5), (4,7), (4,8), (5,6), (5,7), (5,8), (6,8), (7,8) ]
        
        # Satisfying tuple lists for the two constraint types:
        adjCt=[ (di,dj) for di in range(1,9) for dj in range(1,9) if abs(di-dj)>1 ]
        
        diseqCt=[ (di,dj) for di in range(1,9) for dj in range(1,9) if di!=dj ]
        
        for i in range(1, 9):
            for j in range(1, 9):
                if (i,j) in adjacentEdges or (j,i) in adjacentEdges:
                    self.cons.setConstraint(i,j, adjCt)
                else:
                    self.cons.setConstraint(i, j, diseqCt)

#  Make an FC object, set up the crystal maze puzzle, and solve. 

print("Backtrack:")

solver=Search()
solver.setup()
solver.bt(1)

print("="*80)
print("Forward Checking:")

solver=Search()
solver.setup()
solver.fc(1)



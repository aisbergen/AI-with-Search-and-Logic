# -*- coding: utf-8 -*-
"""SR Week 7 & Week 8

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mnkcSqxsFlmEKkDOIcwVzDiMY0H1_uX1

Run the following code to set up the Savile Row environment and define a function for running Savile Row.
"""

import os

srurl="https://www-users.york.ac.uk/peter.nightingale/savilerow/savilerow-1.10.1-linux.tgz"
srdir="savilerow-1.10.1-linux"
![ ! -d $srdir ] && wget $srurl && tar -zxf savilerow-1.10.1-linux.tgz
stub=f"./{srdir}/savilerow -minion-bin {srdir}/bin/minion -satsolver-bin {srdir}/bin/kissat"

def solve(model, param):
  with open("tmp.eprime", "wt") as f:
    f.write(model)
  with open("tmp.param", "wt") as f:
    f.write(param)
  !$stub tmp.eprime tmp.param -run-solver

  try:
    with open("tmp.param.solution", "rt") as f:
      sol=f.read()
    os.remove("tmp.param.solution")
  except FileNotFoundError:
    sol="No solution found."
  print(sol)

"""## **Week 7 Lab**"""

#Forced assign
model = """
language ESSENCE' 1.0
$ The Crystal Maze Puzzle
letting Dom be domain int(1..8)
find x1,x2,x3,x4,x5,x6,x7,x8 : Dom

such that
x1 = 1,

|x1-x2| > 1,
|x1-x3| > 1,
|x1-x4| > 1,
|x1-x5| > 1,
|x2-x4| > 1,
|x2-x5| > 1,
|x2-x6| > 1,
|x3-x4| > 1,
|x3-x7| > 1,
|x4-x5| > 1,
|x4-x7| > 1,
|x4-x8| > 1,
|x5-x6| > 1,
|x5-x7| > 1,
|x5-x8| > 1,
|x6-x8| > 1,
|x7-x8| > 1,

allDiff([x1,x2,x3,x4,x5,x6,x7,x8])


"""
param = """
language ESSENCE' 1.0





"""

solve(model, param)

#Graph parameterized
model = """
$ The Crystal Maze Puzzle

language ESSENCE' 1.0

$ We are fixing the nodes
letting Dom be domain int(1..8)

$ But parameterising on the edges
$ The edges are represented as pairs of integers [i,j]
$  where are i and j are node indices. The edges matrix contains numEdges such pairs
given edges: matrix indexed by[int(1..numEdges), int(1..2)] of int

$ An easy way to get hold of the variables by their names is to put them into an array:
find nodes: matrix indexed by[int(1..8)] of Dom

such that

forAll edge : int(1..numEdges) .
  |nodes[edges[edge,1]] - nodes[edges[edge,2]]| > 1,

allDiff(nodes)

"""
param = """
language ESSENCE' 1.0
letting edges be [[1,2],
                  [1,3],
                  [1,4],
                  [1,5],
                  [2,4],
                  [2,5],
                  [2,6],
                  [3,4],
                  [3,7],
                  [4,5],
                  [4,7],
                  [4,8],
                  [5,6],
                  [5,7],
                  [5,8],
                  [6,8],
                  [7,8]]
"""

solve(model, param)

#Fully parameterized
model = """
language ESSENCE' 1.0

$ The Crystal Maze Puzzle
$ We are fixing the nodes

given noNodes: int

$ But parameterising on the edges
$ The edges are represented as pairs of integers [i,j]
$  where are i and j are node indices. The edges matrix contains numEdges such pairs
given edges: matrix indexed by[int(1..numEdges), int(1..2)] of int

$ An easy way to get hold of the variables by their names is to put them into an array:
find nodes: matrix indexed by[int(1..noNodes)] of int(1..noNodes)

such that

forAll edge : int(1..numEdges) .
  |nodes[edges[edge,1]] - nodes[edges[edge,2]]| > 1,

allDiff(nodes)


"""
param = """
letting noNodes be 8
letting edges be [[1,2],
                  [1,3],
                  [1,4],
                  [1,5],
                  [2,4],
                  [2,5],
                  [2,6],
                  [3,4],
                  [3,7],
                  [4,5],
                  [4,7],
                  [4,8],
                  [5,6],
                  [5,7],
                  [5,8],
                  [6,8],
                  [7,8]]
"""

solve(model, param)

#Two solutions
model = """
language ESSENCE' 1.0

$ The Crystal Maze Puzzle
$ We are fixing the nodes
given noNodes: int

$ But parameterising on the edges
$ The edges are represented as pairs of integers [i,j]
$  where are i and j are node indices. The edges matrix contains numEdges such pairs
given edges: matrix indexed by[int(1..numEdges), int(1..2)] of int

$ An easy way to get hold of the variables by their names is to put them into an array:
find nodes: matrix indexed by[int(1..noNodes)] of int(1..noNodes)

such that

forAll edge : int(1..numEdges) .
  |nodes[edges[edge,1]] - nodes[edges[edge,2]]| > 1,

allDiff(nodes)


"""
param = """
language ESSENCE' 1.0

letting noNodes be 4
letting edges be [[1,2],[1,3],[2,4]]
"""

solve(model, param)

"""WEEK 8 LAB"""

model = """
language ESSENCE' 1.0
letting   RANGE be domain int(1..9)
letting   VALUES be domain int(0..9)

given     values : matrix indexed by [RANGE,RANGE] of VALUES

find      field: matrix indexed by [RANGE, RANGE] of RANGE

such that
  $ all rows have to be different
  forAll row : RANGE .
      allDiff(field[row,..]),

  $ all columns have to be different
  forAll col : RANGE .
      allDiff(field[..,col]),

  $ all 3x3 blocks have to be different
  $ i, j are the coordinates of the upper-left corner of the 3x3 block.
  $forAll i,j : int(1,4,7) .
  $    forAll row1, row2 : int(i..i+2) .
  $        forAll col1, col2 : int(j..j+2) .
  $            ((col1 != col2) \/ (row1 != row2)) ->
  $                field[row1, col1] != field[row2, col2],

  forAll i,j : int(1,4,7) .
    allDiff([ field[k,l] | k : int(i..i+2), l : int(j..j+2)]),


  $ Set some initial values
  forAll row,col : RANGE .
      (values[row,col] > 0) ->
          (field[row,col] = values[row,col])"""


param = """
language ESSENCE' 1.0
letting values be [ [ 5, 3, 0, 0, 7, 0, 0, 0 ,0 ],
                    [ 6, 0, 0, 1, 9, 5, 0, 0, 0 ],
                    [ 0, 9, 8, 0, 0, 0, 0, 6, 0 ],
                    [ 8, 0, 0, 0, 6, 0, 0, 0, 3 ],
                    [ 4, 0, 0, 8, 0, 3, 0, 0, 1 ],
                    [ 7, 0, 0, 0, 2, 0, 0, 0, 6 ],
                    [ 0, 6, 0, 0, 0, 0, 2, 8, 0 ],
                    [ 0, 0, 0, 4, 1, 9, 0, 0, 5 ],
                    [ 0, 0, 0, 0, 8, 0, 0, 7, 9 ]]
"""


solve(model, param)

#Modelling Winner Determination Problem (Combinatorial Auction)
model = """
language ESSENCE' 1.0

given nItems : int(1..)
given nBids : int(1..)

$  For each bid b, price[b] is the amount of money offered.
given price : matrix indexed by [int(1..nBids)] of int(0..)

$  For each bid b, bids[b, ..] is the occurrence representation of the set of items.
given bids : matrix indexed by [int(1..nBids), int(1..nItems)] of bool

$  Occurrence representation of the set of accepted bids.
find accepted : matrix indexed by [int(1..nBids)] of bool

maximising sum([ price[i]*accepted[i] | i : int(1..nBids) ])

$ Alternative with sum quantifier instead of a comprehension:
$maximising sum i : int(1..nBids) . price[i]*accepted[i]

such that

forAll i : int(1..nBids).
  forAll j : int(1..nBids) .
    i<j ->
      (
        (sum k : int(1..nItems). (bids[i,k] /\ bids[j,k]) )!=0 ->
            !(accepted[i] /\ accepted[j])
        $ Alternative with exists instead of sum:
        $(exists k : int(1..nItems). (bids[i,k] /\ bids[j,k]) ) ->
        $   !(accepted[i] /\ accepted[j])
      )


"""
param = """
language ESSENCE' 1.0

letting nItems = 4
letting nBids = 4

letting price = [10,12,13,20]

letting bids=
[[true,true,false,true],
[false, false, true, false],
[true, false, false, true],
[true, true, true, true]]
"""

solve(model, param)


model = """
language ESSENCE' 1.0

letting horizon=12

$  State of robot

$  -- the room the robot is in at each timestep
find room : matrix indexed by [int(1..horizon)] of int(1..2)

$  -- how many balls the robot is carrying
find carrying : matrix indexed by [int(1..horizon)] of int(0..2)

$  State of the environment

find ballsInRoom : matrix [int(1..horizon), int(1..2)] of int(0..4)

$  Action   1: pick up,  2: put down, 3: move
$  No need for a 'no-op' action in this case -- the robot can repeatedly use the 'move' action once the goal has been achieved. 

find action : matrix [int(1..horizon-1)] of int(1..3)

such that

$ Set up initial state
room[1]=1,
carrying[1]=0,
ballsInRoom[1,1]=4,
ballsInRoom[1,2]=0,

$ The 'pick up' action
forAll t : int(1..horizon-1).
    action[t]=1 -> (
        carrying[t+1]=carrying[t]+1  /\   $  Carrying one additional ball
        room[t+1]=room[t]  /\             $  Stays in same room
        ballsInRoom[t+1, room[t]]=ballsInRoom[t, room[t]]-1 /\     $  Number of balls in robot's room is reduced by 1
        ballsInRoom[t+1, 3-room[t]]=ballsInRoom[t, 3-room[t]]      $  Number of balls in other room stays the same
    ),

$ The 'put down' action
forAll t : int(1..horizon-1).
    action[t]=2 -> (
        carrying[t+1]=carrying[t]-1  /\
        room[t+1]=room[t]  /\
        ballsInRoom[t+1, room[t]]=ballsInRoom[t, room[t]]+1 /\
        ballsInRoom[t+1, 3-room[t]]=ballsInRoom[t, 3-room[t]]
    ),

$ The 'move' action
forAll t : int(1..horizon-1).
    action[t]=3 -> (
        carrying[t+1]=carrying[t]  /\
        room[t+1]=3-room[t]  /\
        ballsInRoom[t+1, 1]=ballsInRoom[t, 1] /\
        ballsInRoom[t+1, 2]=ballsInRoom[t, 2]
    ),

$ The goal -- all balls are in room 2
ballsInRoom[horizon,2]=4






"""
param = """
language ESSENCE' 1.0


solve(model, param)

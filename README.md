# Simluated Annealing Assignment for Political Redistricting

For this assignment I used a simulated annealing algorithm to create solutions for a political redistricting problem. The objective is to find the most representative and evenly divided voting districts for the set of data. Requirements for the districts include adjacency between all the nodes and the same number of voters in each district. The number of districts depends upon whether an 8x8 or 10x10 matrix of voters is used. The voter matrix is passed in as a command line argument.

## Requirements
```
Python 2.7.10 
```
## Running
Run main.py passing in either "smallState.txt" or "largeState.txt" as a command line argument.
```
python main.py smallState.txt
python main.py largeState.txt
```

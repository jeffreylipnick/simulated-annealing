# Simluated Annealing Assignment for Political Redistricting
## Introduction
This program was originally completed as an assignment for an Introduction to Artificial Intelligence class at the University of Colorado Boulder. I used a simulated annealing algorithm to create solutions for a political redistricting problem. The objective was to find the most representative and evenly divided voting districts for the set of data. Requirements for the districts include adjacency between all the nodes and the same number of voters in each district. The number of districts depends upon whether an 8x8 or 10x10 matrix of voters is used. The voter matrix is passed in as a command line argument.

## Background
Political Redistricting problems such as this one are NP-hard due to the size of the problem space.  As such, it is impossible to find the optimal solution.  However, using approximation algorithms we can find "good" solutions in a reasonable timeframe.

## Simulated Annealing
The simulated annealing algorithm models the way metals cool as a means to approximate a "good" solution to a computationally complex problem like political redistricting.  The annealing analogy arises as the parallel between the temperature of the algorithm and the temperature of the slowly cooling metal.  Solutions are evaluted with a fitness function, with better solutions being accepted automatically.  Poorer solutions have the opportunity of being accepted with some probability in order to prevent the algorithm from getting stuck at a local optimum. As the temperature of the algorithm changes with more iterations, solutions with poorer fitness scores have a progressively lower probability of being accepted.  Pseudocode for the algorithm is as follows:
```
SimulatedAnnealing:
    s = s0 //generate an initial solution
    T = Tmax //set the initial temperature
    Tmin = .00001 //minimum temp for the algorithm, tunable parameter
    alpha = 0.9   //temperature adjustment, tunable parameter   
    while T > Tmin:
        while !equilibrium:
           s' = random neighbor of s
           ΔE = f(s') - f(s)  //evaluate the fitness of state s and s'
           if ΔE < 0:  //assumes we want to minimize fitness, would be ΔE > 0 if we were maximizing fitness
               s = s'  //accept neighbor solution
           else
            //accept s' with probability e(-ΔE/kT)
        T = T * alpha
    return s
```
Source: http://www.microveggies.com/csci/index.php/9-csci-3202-lecture-notes/34-lecture-13-local-search

## Requirements
```
Python 2.7.10 
```
## Running
In the terminal, run main.py passing in either "smallState.txt" or "largeState.txt" as a command line argument.
```
~ $ python main.py smallState.txt
```
or
```
~ $ python main.py largeState.txt
```
The output will appear below in the terminal.

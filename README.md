# Travelling Salesman Problem (with time window) in Python

The [travelling salesman problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem) is an np-hard problem with application in supply chain and computer science. 

 _tsp_exact_ uses [PuLP module](https://coin-or.github.io/pulp/) to formulate the problem and [CPLEX](https://www.ibm.com/analytics/cplex-optimizer), [GUROBI](https://www.gurobi.com/solutions/gurobi-optimizer/), [COIN_CMD](https://github.com/coin-or/Cbc), and [PULP_solver](https://github.com/coin-or/pulp) to find the exact solution of the TSP. To setup an external solver follow [this link](https://coin-or.github.io/pulp/guides/how_to_configure_solvers.html). 

#### Input Parameters:

1. **_matrix_**: is a **_NxN_** cost matrix between the points that have to be visited by the nodes with 2 requirements:

 a. The row and column index of this matrix should be **INTEGER**
 
 b. Depot is indexed by 0, i.e. Row 0 represents the Depot. 

##### Example:
```
    0     1   2     3   4
0   0  21.0  15  21.0  10
1  21   0.0   5   0.5  11
2  15   5.0   0   5.0   5
3  21   0.5   5   0.0  10
4  10  11.0   5  10.0   0
```
2. **_method_**: The type of solver to use. Default is "PULP_CBC_CMD". Other solvers available are: "CPLEX_CMD", "GUROBI_CMD", and "COIN_CMD".
3. **_message_**: PuLP will display calculation summary if message is set to 1. Default value is 0 (suppress summary).
4. **_route_**: Initial route estimate  **_(only for improvement heuristics & metaheuristics)_**
5. **_trials_**: Number of local search to be made, default is 5000  **_(only for improvement heuristics & metaheuristics)_**
6. **time_window**: a **_Nx1_** matrix containing the time by which node has to be visited by the truck. If $tw_{i}=0$ the solution will assume that there is no time constraint for customer $i$

#### Output attributes:

1. **_route_**[List]: The shortest route coving all the nodes. (The route starts from the depot and ends at the depot)
2. **_route_sum_**[Scalar]: Total cost incurred by the route. 


## Mathematical formulation for the TSP9time window) solution:
Below is the mathematical formulation for the exact solution of tsp with time window which is executed by *tsp_exact()* function

### Sets and Decision variables

$\mathbb{N}$ is the set of all customer node subset $i$ and $j$

We will use  binary variable $x_{ij}$ 

$x_{ij}$ will take the value 1 if truck travels from node $i$ to node $j$, 0 otherwise. $i\in\mathbb{N}$ and $j\in\mathbb{N}$

Other variables are:

$u_{i}$ will take the value of the order of node $i$ in the final route of truck. $i\in\mathbb{N}^{}$

$t_{i}$ represents the arrival time for truck at node $i$. 

$tt_{ij}$ represents the truck travel time between nodes $i$ and $j$. 

$M$ is a very large number

$tw_{i}$ is the time by which node $i$ has to be visited by the truck

Objective: Minimize the total time to visit all nodes

$$ Obj=min\{\sum_{i}t_{i}\} $$

Constraint 1: All nodes have to be visited by truck exactly once

$$ \sum_{i}x_{ij}=1\quad j\in\mathbb{N}$$ 

Constraint 2: Truck leaves depot D and comes back to depot D' exactly once $i=D,D'$

$$ \sum_{j}x_{ij}=1 $$ 

$$ \sum_{j}x_{ji}=1 $$

Constraint 3: If truck arrives at node j then it should also leave node j.

$$ \sum_{i}x_{ij}=\sum_{k}x_{jk} \quad j\in\mathbb{N}$$

Constraint 4: Avoiding sub-tours for truck

$$ u_{j}-u_{k}-1\leq M(1-x_{jk}) \quad j,k\in\mathbb{N}$$ 

Constraint 5: We will add travel time $tt_{ij}$ to arrival time at node $i$ to get arrival time at node $j$ if truck travels in $ij$ path

$$ t_{j}\geq t_{i}+tt_{ij}-M(1-x_{ij}) \quad i,j\in\mathbb{N}$$

Constraint 6: Each node has to be visited before the time specified 

$$ t_{i}\leq tw_{i} \quad i\in\mathbb{N}$$


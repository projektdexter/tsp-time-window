import pandas as pd
import numpy as np
from pulp import *

class tsp:
    '''
    class instance initiaton
    '''
    def __init__(self):
        None

    '''
    Exact formulation of TSP
    '''
    def tsp_exact(self, matrix, method = "", message = 0, time_window=[]):

      if isinstance(matrix.columns[0], str):
        print("Error: Column index should be INT") 
        return None

      result = []
      result_name = []
      result_df = pd.DataFrame()
      row,col = matrix.shape
      
      problem = LpProblem('TravellingSalesmanProblem', LpMinimize)

      # Decision variable X for truck route
      decisionVariableX = LpVariable.dicts('decisionVariable_X', ((i, j) for i in range(row) for j in range(row)), lowBound=0, upBound=1, cat='Integer')

      # subtours elimination
      decisionVariableU = LpVariable.dicts('decisionVariable_U', (i for i in range(row)), lowBound=1, cat='Integer')

      # Decision variable T for truck arrival time
      decisionVariableT = LpVariable.dicts('decisionVariable_T', (i for i in range(row)), lowBound=0, cat='Float')

      # objective variable
      z = LpVariable("Objective_z", lowBound=0, cat='Float')

      # Objective Function
      problem += z + lpSum(matrix.iloc[i,0] * decisionVariableX[i, 0] for i in range(row))

      #time window constraint
      for i in range(row):
        if (i!=0):
            if (time_window[i-1] !=0):
                problem += decisionVariableT[i] <= time_window[i-1]

      # Constraint
      for i in range(row):
          problem += (decisionVariableX[i,i] == 0) # elimination of (1 to 1) route
          if i==0:
              problem += (decisionVariableT[i] == 0) # elimination of (1 to 1) route
          problem += lpSum(decisionVariableX[i,j] for j in range(row))==1 # truck reaches all points once
          problem += lpSum(decisionVariableX[j,i] for j in range(row)) ==1 #truck dispatches from all points once
          for j in range(row):
              if i != j and (i != 0 and j != 0):
                  problem += decisionVariableU[i]  <=  decisionVariableU[j] + row * (1 - decisionVariableX[i, j])-1 # sub-tour elimination for truck
              if i != j and (j != 0):
                  problem += decisionVariableT[j] >= decisionVariableT[i] + matrix.iloc[i,j] - 10000*(1-decisionVariableX[i,j]) # Calculating time of arrival at each node
      
      # last stop time
      for i in range(row):
          problem += decisionVariableT[i] <= z

      # Solving the equation and storing the result
      if method == "CPLEX_CMD":
        status = problem.solve(CPLEX_CMD(msg=message)) 
      if method == "GUROBI_CMD":
        status = problem.solve(GUROBI_CMD(msg=message)) 
      if method == "COIN_CMD":
        status = problem.solve(COIN_CMD(msg=message)) 
      if method == "":
        status = problem.solve(PULP_CBC_CMD(msg=message)) 
      for var in problem.variables():
          if (problem.status == 1):
              if (var.value() !=0):
                  result.append(var.value())
                  result_name.append(var.name)
      result_df['Variable Name'] = result_name
      result_df['Variable Value'] = result
      print(result_df)

      # creating route list      
      route = [0]*row
      for x,value in enumerate(route):
        for j in range(row):
          if (pulp.value(decisionVariableX[value,j])==1):
            if (j!=0):
              route[x+1] = j
      route.append(0)
    
      return(route, problem.objective.value())

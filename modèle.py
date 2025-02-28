import pyomo.environ as pyo

# Create a Pyomo model
model = pyo.ConcreteModel()

# Create a Pyomo model
model = pyo.ConcreteModel()



# Define model parameters
model.PVcost = pyo.Param(initialize=0.18) #€/m²
model.PVprod = pyo.Param(initialize=0.25) #kWh/m²
model.PVemission = pyo.Param(initialize=0.18) #kgCO2/m²
model.PVefficiency = pyo.Param(initialize=0.25)

model.WINDcost = pyo.Param(initialize=0.18) #€/unity
model.WINDprod = pyo.Param(initialize=0.25) #kWh/unity
model.WINDemission = pyo.Param(initialize=0.18) #kgCO2/unity

model.maxCO2 = pyo.Param(initialize=14E6) #kgCO2

# Define model variables
model.PVsurface = pyo.Var(domain=pyo.NonNegativeReals)
model.WINDnumber = pyo.Var(domain=pyo.NonNegativeReals)

# Define objective function
model.objective = pyo.Objective(expr=model.WINDnumber*model.WINDcost+model.PVcost*model.PVsurface, sense=pyo.minimize)

# Define constraints
def maxCO2(model):
    return model.PVemission*model.PVsurface <= model.maxCO2

model.maxCO2Constr = pyo.Constraint(rule=maxCO2)



model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
model.rc = pyo.Suffix(direction=pyo.Suffix.IMPORT)

solver = pyo.SolverFactory('gurobi')
sol = solver.solve(model)


#print(model.boatsCH4.value)
#print(model.boatsNH3.value)
model.display()
model.dual.display()
model.rc.display()
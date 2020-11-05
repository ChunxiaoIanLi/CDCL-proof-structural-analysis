from PMILib import PMI

# Create object
pmi = PMI()

# Put the clauses in dimacs format
clauses = [1,2,3,4,5,0,-1,5,7,8,0,-2,3,5,6,7,0]
numVars = 8

# Load the clauses
pmi.setClauses(clauses)

# Put the variable set in a zero-terminated array
varSet = [1,2,3,4,5,6,7,8,0]

clauseFilterMode = 0

# Calculate mergeability
pmi.calculate(varSet, clauseFilterMode)
print(pmi.getMergeability())
print(pmi.getMergeabilityScoreNorm1())
print(pmi.getMergeabilityScoreNorm2())
print(pmi.getPreResolutionClauseWidth())
print(pmi.getPostResolutionClauseWidth())
print("------")
pmi.calculate([1,2,3,4,5,6,7,0], clauseFilterMode)
print(pmi.getMergeability())
print(pmi.getMergeabilityScoreNorm1())
print(pmi.getMergeabilityScoreNorm2())
print(pmi.getPreResolutionClauseWidth())
print(pmi.getPostResolutionClauseWidth())
print("------")
pmi.calculate([1,3,5,6,7,0], clauseFilterMode)
print(pmi.getMergeabilityScoreNorm1())
print(pmi.getMergeabilityScoreNorm2())
print(pmi.getPreResolutionClauseWidth())
print(pmi.getPostResolutionClauseWidth())
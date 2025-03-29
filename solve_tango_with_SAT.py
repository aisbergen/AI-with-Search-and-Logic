import itertools as it
import json
import logging
from pysat.formula import CNF
from pysat.solvers import Glucose3
import sys

class TangoProblem:

    def __init__(self, shapes, equals=[], diffs=[]):
        self.shapes = shapes
        self.equals = equals
        self.diffs  = diffs

        # construct the formula with string name variables
        self.str_clauses = self.makeStrClauses()

        # create lookup table (dictionary) of variable names to their integer id;
        # convert the string clauses into integer clauses
        self.varnames, self.clauses = self.convertToInts(self.str_clauses)


    def makeStrClauses(self):
        _clauses = []
        size = len(self.shapes)

        # use the convention r_c_s meaning the cell at row r and column c has shape s,
        # where s is either 1 (sun) or 2 (moon)

        # set up the basic clauses for one shape per cell
        for r in range(size):
            for c in range(size):
                # each cell must have at least sun or moon set to true
                _clauses.append( (f'{r}_{c}_1', f'{r}_{c}_2') )
                for s in (1,2): 
                    # if this cell is set to s, we must set the other shape to false
                    _clauses.append( ( f'-{r}_{c}_{s}', f'-{r}_{c}_{3-s}') )

        # add in the given clues
        for r,row in enumerate(self.shapes):
            for c, s in enumerate(row):
                if s in (1,2):
                    _clauses.append( (f'{r}_{c}_{s}',) )

        # now deal with the inter-cell '=' operators
        for (r1,c1),(r2,c2) in self.equals:
            for s in (1,2):
                # double implication, so enforce both ways
                _clauses.append( (f'-{r1}_{c1}_{s}', f'{r2}_{c2}_{s}')  )
                _clauses.append( (f'-{r2}_{c2}_{s}', f'{r1}_{c1}_{s}')  )
                    
        # now deal with the inter-cell 'x' operators
        for (r1,c1),(r2,c2) in self.diffs:
            for s in (1,2):
                # double implication, so enforce both ways
                _clauses.append( (f'-{r1}_{c1}_{s}', f'-{r2}_{c2}_{s}')  )
                _clauses.append( (f'-{r2}_{c2}_{s}', f'-{r1}_{c1}_{s}')  )

        # no more than two of the same shape together in any row
        for r in range(size):
            for c in range(size-2):
                for s in (1,2):
                    # for consecutive cells a, b, c we want (a /\ b) -> (¬c)
                    # which is equivalent to ¬a \/ ¬b \/ ¬c
                    _clauses.append( (f'-{r}_{c}_{s}',f'-{r}_{c+1}_{s}',f'-{r}_{c+2}_{s}') )

        # no more than two of the same shape together in any column
        for c in range(size):
            for r in range(size-2):
                for s in (1,2):
                    # for consecutive cells a, b, c we want (a /\ b) -> (¬c)
                    # which is equivalent to ¬a \/ ¬b \/ ¬c
                    _clauses.append( (f'-{r}_{c}_{s}',f'-{r+1}_{c}_{s}',f'-{r+2}_{c}_{s}') )
                

        # exactly 3 of each shape per row
        for s in range(1,2):
            for r in range(size):
                # find all possible sets of 3 columns
                for (c1,c2,c3) in it.combinations(range(size),r=3):
                    others = [c for c in range(size) if c not in (c1,c2,c3)]
                    for co in others:
                        # we're saying (c1 /\ c2 /\ c3) -> (¬co), which is (¬c1 \/ ¬c2 \/ ¬c3 \/ ¬c4)
                        _clauses.append( (f'-{r}_{c1}_{s}', f'-{r}_{c2}_{s}', f'-{r}_{c3}_{s}', f'-{r}_{co}_{s}') )

        # exactly 3 of each shape per column
        for s in range(1,2):
            for c in range(size):
                for (r1,r2,r3) in it.combinations(range(size),r=3):
                    others = [r for r in range(size) if r not in (r1,r2,r3)]
                    for ro in others:
                        _clauses.append( (f'-{c}_{r1}_{s}', f'-{c}_{r2}_{s}', f'-{c}_{r3}_{s}', f'-{c}_{ro}_{s}') )

        return _clauses


        
    def convertToInts(self, str_cl):
        """Convert clauses expressed as strings into lists of integers"""

        varnames2ints = {}
        clauses = []

        # go clause by clause
        for str_lits in str_cl:
            int_clause = []
            # take each literal in turn
            for str_lit in str_lits:
                is_neg = str_lit.startswith('-')
                justvar = str_lit[1:] if is_neg else str_lit
                var_int = varnames2ints.get(justvar,None)

                # if we haven't seen this variable name before, add it as the next integer
                if var_int == None:
                    var_int = len(varnames2ints)+1
                    varnames2ints[justvar] = var_int

                # now add it into the new clause, as negative int if it's a negative literal
                int_clause.append(var_int * (-1 if is_neg else 1) )
            clauses.append(int_clause)
        return varnames2ints, clauses

    def solve(self):
        """Attempt to find a solution using a SAT solver"""

        formula = CNF()
        for clause in self.clauses:
            formula.append(clause)

        with Glucose3(bootstrap_with=formula) as gluc:
            gluc.solve()
            model = gluc.get_model()
            logging.debug(f"Received model: {model}")
        return model

    def printSolution(self, model):
        """Pretty-print the board given a SAT model"""

        size = len(self.shapes)
        for r in range(size):
            shapes_in_row = []
            for c in range(size):
                # which of 1 or 2 is set to true in the model?
                is_1 = (self.varnames[f'{r}_{c}_1'] in model)
                is_2 = (self.varnames[f'{r}_{c}_2'] in model)
                if (is_1 and is_2):
                    logging.warning("Oops, we can't have both values true at {r}_{c}!")
                    shapes_in_row.append('X')
                elif not (is_1 or is_2):
                    logging.warning("Oops, we have no value set to true at {r}_{c}!")
                    shapes_in_row.append('-')
                else:
                    shapes_in_row.append('1' if is_1 else '2')
            print(' '.join(shapes_in_row))
    

# run from command line, with a single argument giving the path to the data file (json)
if __name__=='__main__':
    if len(sys.argv) < 2:
        print("Pass in the JSON file with the board")
        exit(1)
    # enable debug messages
    logging.basicConfig(level=logging.DEBUG)

    # read in the board data
    with open(sys.argv[1],'rt') as f:
        board = json.loads(f.read())
    logging.debug(f"Loaded board info: {board}")

    # create a TangoProblem instance with the existing shapes, the '=' pairs and the 'x' pairs
    tp = TangoProblem(board['shapes'], board.get('equal',[]), board.get('different',[]))

    # obtain a solution if possible, in terms of the boolean variables
    model = tp.solve()

    # interpret the SAT solver output
    tp.printSolution(model)

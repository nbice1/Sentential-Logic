#these initial classes treat formulas as syntax trees, with each internal node corresponding to a logical connective with 
#one or two branches (negation has one branch, binary connectives have left and right branches), and bottom nodes
#corresponding to atomic sentence variables or truth-values

class Not:
    opStr = '~'
    def __init__(self, formula):
        self.formula = formula
        
    #negations are represented in the form '~p'
    def __str__(self):
        return self.opStr + str(self.formula)
    def __repr__(self):
        return str(self)
    
    #a negation is true exactly if its main subformula is false, and the eval function treats it accordingly; here 'env' is
    #a dictionary containing assignments of truth-values to atomic formulas
    def eval(self, env):
        if self.formula.eval(env) == None:
            return None
        else:
            return not self.formula.eval(env)
        
#this is the main class for binary connectives, which have both left and right branches (corresponding to their left and right
#subformulas)
class BinaryOp:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    #all binary connectives * are represented in the form '(p * q)'
    def __str__(self):
        return '(' + str(self.left) + ' ' + self.opStr + ' ' + \
               str(self.right) + ')'
    def __repr__(self):
        return str(self)
    
class And(BinaryOp): 
    opStr = '^'
    #a conjunction is true exactly if both conjuncts are true
    def eval(self, env):
        return self.left.eval(env) and self.right.eval(env)
    
class Or(BinaryOp): 
    opStr = 'v'
    #a disjunction is true exactly if either the first disjunct is true or the second disjunct is true or both
    def eval(self, env):
        return self.left.eval(env) or self.right.eval(env)
    
class Implies(BinaryOp):
    opStr = '>'
    #a material conditional is true exactly if the conjunction of the antecedent and the negation of the consequent is false
    def eval(self, env):
        return not(self.left.eval(env) and not(self.right.eval(env)))
    
class Bicond(BinaryOp):
    opStr = '='
    #a biconditional is true exactly if either both sides are true or both sides are false
    def eval(self, env):
        return (self.left.eval(env) and self.right.eval(env)) or \
               (not(self.left.eval(env)) and not(self.right.eval(env)))
        
#this is a special class for assigning truth-values to atomic sentence variables
class Assign(BinaryOp):
    opStr = ':'
    #the eval function modifies the environment 'env' (a dictionary) by assigning the truth-value specified to the atomic
    #formula, e.g. '(p : T)' when evaluated assigns the truth-value T to atomic formula 'p'
    def eval(self, env):
        value = self.right.eval(env)
        env[self.left.name] = value
        
#this class handles atomic sentence variables, which are strings of letters and numbers
class Variable:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return str(self.name)
    __repr__ = __str__
    #evaluating a variable will either return its truth-value or print an error message if it doesn't have one
    def eval(self, env):
        if self.name in env:
            return env[self.name]
        else:
            print ("Atomic formula %s has not been assigned a truth-value." \
                   % self.name)
            
#this is a class for the two truth-values: True and False
class TruthValue:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        if self.value == True:
            return 'T'
        else:
            return 'F'
    __repr__ = __str__
    def eval(self, env):
        return self.value
    
#this is a list of special characters used by the parser to parse an inputted string
seps = ['(', ')', '~', '^', 'v', '>', '=', ':', 'T', 'F']

import string

#this function converts a string into a list of its significant parts; e.g. '(p ^ (q v r))' is converted into ['(', 'p', '^', 
#'(', 'q', 'v', 'r', ')', ')']
def tokenize(inputString):
    result = []
    state = 'open'
    #this function loops over the input string, adding a character to the list if it's in seps (see above), ignoring it if 
    #it's a space, and starting another loop otherwise (since it will then be a variable name, see below)
    for n in range(len(inputString)):
        if inputString[n] in seps:
            result.append(inputString[n])
            state = 'open'
        elif inputString[n] == ' ':
            state = 'open'
        else:
            #the character at index n must be the beginning of a variable name, and hence a new loop is constructed in order
            #to find the end of the variable name and then add the whole variable name to the list; this is done by noting 
            #that the end of a variable name will either be a space, a special character (in seps), or the end of the string
            for m in range(n, len(inputString)):
                if state == 'open' and (inputString[m] == ' ' or \
                inputString[m] in seps):
                    result.append(inputString[n:m])
                    state = 'word'
                elif state == 'open' and m+1 == len(inputString):
                    result.append(inputString[n:m+1])
                    state = 'word'
    return result

#this function returns true if its input is 'T' or 'F'
def valueTok(token):
    return token == 'T' or token == 'F'

#this function returns true if its input is a string of letters and numbers not including 'T', 'F', or 'v', all 
#of which have special meanings in the formal language (True, False, and disjunction, respectively)
def variableTok(token):
    for char in token:
        if not(char in string.ascii_letters or char in string.digits) \
           or char == 'T' or char == 'F' or char == 'v':
            return False
    return True

#this function parses a list of significant expressions recursively and returns the appropriate syntax tree (an instance of 
#one of the classes above); the expected input is the output of the tokenize function (above) given a string as input
def parse(tokens):
    #this helper function takes an index and returns a tuple consisting of both the syntax tree beginning at that index 
    #and the index after the tree; if the string at the input index is a '(', then it corresponds to the beginning of a syntax 
    #tree for a binary connective or truth-value assignment, and hence the function is called recursively on the branches 
    #corresponding to that connective or assignment (it will also be called recursively if the string is a '~')
    def parseForm(index):
        token = tokens[index]
        if valueTok(token):
            if token == 'T':
                return (TruthValue(True), index + 1)
            else:
                return (TruthValue(False), index + 1)
        elif variableTok(token):
            return (Variable(token), index + 1)
        elif token == '~':
            (tree, nextIndex) = parseForm(index + 1)
            return (Not(tree), nextIndex)
        else:
            #here we take advantage of the fact that in this case the string at the input index will be a '(', and hence 
            #the next index will correspond to the left branch of a binary connective or truth-value assignment
            (leftTree, opIndex) = parseForm(index + 1)
            op = tokens[opIndex]
            (rightTree, parIndex) = parseForm(opIndex + 1)
            if op == '^':
                return (And(leftTree, rightTree), parIndex + 1)
            elif op == 'v':
                return (Or(leftTree, rightTree), parIndex + 1)
            elif op == '>':
                return (Implies(leftTree, rightTree), parIndex + 1)
            elif op == '=':
                return (Bicond(leftTree, rightTree), parIndex + 1)
            elif op == ':':
                return (Assign(leftTree, rightTree), parIndex + 1)
    #we then call the helper function on the index 0 to construct the full syntax tree, which is then returned
    try:
        (parsedForm, nextIndex) = parseForm(0)
        return parsedForm
    #this checks for common user input mistakes and prints an error message
    except (IndexError, TypeError):
        print ("That is not a well-formed formula.")

#this is one of the two main functions of the program, which requests a string from the user as input and either outputs the 
#truth-value of the corresponding logical formula or commits a truth-value assignment to the environment
def evaluator():
    env = {}
    while True:
        e = input('%')
        if e == 'exit':
            break
        else:
            #here we use our parser to determine the appropriate syntax tree and then run its eval method and print both the 
            #result and the current environment of truth-value assignments
            try:
                print ('%', parse(tokenize(e)).eval(env))
                print ('   env =', env)
            #if the user inputted an improper string, they will get an error message and the program will continue to run
            except AttributeError:
                print ('   env =', env)

#this function is similar to tokenize above, except it constructs a list of whole formula-expressions or special expressions
#separated by ',' or ':'
def listMaker(string):
    result = []
    state = 'open'
    for n in range(len(string)):
        #the end of a token string will either be a ',' or a ':' or the end of the full input string, and we take advantage 
        #of this to add the full token string to the constructed list
        for m in range(n, len(string)):
            if state == 'open' and (string[m] == ',' or string[m] == ':'):
                result.append(string[n:m])
                state = 'formula'
            elif state == 'open' and m+1 == len(string):
                result.append(string[n:m+1])
                state = 'formula'
        if string[n] == ',' or string[n] == ':':
            state = 'open'
    return result

#this is the second main function of our program, which allows the user to construct a proof in a sound and complete 
#derivation system for sentential logic
def prover():
    #the proof will be treated as a list of formulas and further lists (which correspond to assumptions and subproofs)
    proof = []
    e = input('Please state the premises: ')
    if e == 'exit':
        return None
    else:
        #the premises are separated by commas, and hence listMaker can separate them before we feed them into our parser and
        #construct the initial proof, which is then printed (see README for details)
        prems = listMaker(e)
        for pr in prems:
            #this if condition catches user input errors and reruns prover (parse will print an error message)
            if parse(tokenize(pr)) == None:
                prover()
                return None
            else:
                proof.append([parse(tokenize(pr))])
        print ('  proof =', proof)
        while True:
            e = input('Please apply an inference rule: ')
            if e == 'exit':
                break
            else:
                #there are 18 separate inference rules that can be applied, each of which must be handled separately (see 
                #README for details on the separate inference rules; I am only including comments on the first rule and a
                #couple others since the rest are all handled in a similar way); I assume the reader has a basic
                #understanding of natural deduction systems in sentential/propositional logic
                rule = listMaker(e)
                #these first few conditions simply assign values to variables pr1, etc. to make the rest of the code cleaner 
                #and check for a couple simple user mistakes
                if len(rule) == 2 and not rule[0] == 'Assume':
                    pr1 = proof[int(rule[1])]
                elif len(rule) == 3 and not rule[0] == 'Assume':                   
                    pr1 = proof[int(rule[1])]
                    pr2 = proof[int(rule[2])]
                elif rule[0] == 'Assume' and not len(rule) == 2:
                    print ('You can only assume a single formula.')
                elif rule[0] == 'Assume' and len(rule) == 2:
                    pass
                elif rule[0] == 'TI' or rule[0] == 'delete':
                    pass
                elif rule[0] == 'vE' and len(rule) == 4:
                    pr1 = proof[int(rule[1])]
                    pr2 = proof[int(rule[2])]
                    pr3 = proof[int(rule[3])]
                else:
                    print ('That is not an acceptable inference rule.')
                if rule[0] == '^E1':
                    #as an example, if the inputted inference rule is conjunction elimination on the left conjunct, we first 
                    #check that the formula the user specified is in fact a conjunction, and then add its left conjunct to 
                    #the proof (which is then printed)
                    if type(pr1) == And:
                        proof.append(pr1.left)
                    #here (and for each inference rule) we must check whether the formula the user specified is an assumption, 
                    #since in that case it will be contained within a single-element list and must be treated accordingly
                    elif type(pr1) == list and len(pr1) == 1 and \
                         type(pr1[0]) == And:
                        proof.append(pr1[0].left)
                    else:
                        print ('That formula is not a conjunction.')
                    print ('  proof =', proof)
                elif rule[0] == '^E2':
                    if type(pr1) == And:
                        proof.append(pr1.right)
                    elif type(pr1) == list and len(pr1) == 1 and \
                         type(pr1[0]) == And:
                        proof.append(pr1[0].right)
                    else:
                        print ('That formula is not a conjunction.')
                    print ('  proof =', proof)
                elif rule[0] == '^I':
                    if type(pr1) == list and len(pr1) == 1 and not type(pr2) \
                       == list:
                        proof.append(And(pr1[0], pr2))
                        print ('  proof =', proof)
                    elif (not type(pr1) == list) and type(pr2) == list and \
                         len(pr2) == 1:
                        proof.append(And(pr1, pr2[0]))
                        print ('  proof =', proof)
                    elif type(pr1) == list and type(pr2) == list and len(pr1) \
                         == 1 and len(pr2) == 1:
                        proof.append(And(pr1[0], pr2[0]))
                        print ('  proof =', proof)
                    else:
                        proof.append(And(pr1, pr2))
                        print ('  proof =', proof)
                elif rule[0] == '~E':
                    if type(pr1) == Not and type(pr1.formula) == Not:
                        proof.append(pr1.formula.formula)
                        print ('  proof =', proof)
                    elif type(pr1) == list and len(pr1) == 1 and type(pr1[0]) \
                         == Not and type(pr1[0].formula) == Not:
                        proof.append(pr1[0].formula.formula)
                        print ('  proof =', proof)
                    else:
                        print ('That is not a double negation.')
                elif rule[0] == '>E':
                    if type(pr1) == list and len(pr1) == 1 and type(pr2) == \
                       Implies and str(pr1[0]) == str(pr2.left):
                        proof.append(pr2.right)
                        print ('  proof =', proof)
                    elif (not type(pr1) == list) and type(pr2) == list and \
                         len(pr2) == 1 and type(pr2[0]) == Implies and \
                         str(pr1) == str(pr2[0].left):
                        proof.append(pr2[0].right)
                        print ('  proof =', proof)
                    elif type(pr1) == list and len(pr1) == 1 and type(pr2) == \
                         list and len(pr2) == 1 and type(pr2[0]) == Implies \
                         and str(pr1[0]) == str(pr2[0].left):
                        proof.append(pr2[0].right)
                        print('  proof =', proof)
                    elif (not type(pr1) == list) and type(pr2) == Implies \
                         and str(pr1) == str(pr2.left):
                        proof.append(pr2.right)
                        print ('  proof =', proof)
                    else:
                        print('That is not an acceptable use of >E.')
                elif rule[0] == '=E1':
                    if type(pr1) == list and len(pr1) == 1 and type(pr2) == \
                       Bicond and str(pr1[0]) == str(pr2.left):
                        proof.append(pr2.right)
                        print ('  proof =', proof)
                    elif (not type(pr1) == list) and type(pr2) == list and \
                         len(pr2) == 1 and type(pr2[0]) == Bicond and \
                         str(pr1) == str(pr2[0].left):
                        proof.append(pr2[0].right)
                        print ('  proof =', proof)
                    elif type(pr1) == list and len(pr1) == 1 and type(pr2) == \
                         list and len(pr2) == 1 and type(pr2[0]) == Bicond \
                         and str(pr1[0]) == str(pr2[0].left):
                        proof.append(pr2[0].right)
                        print('  proof =', proof)
                    elif (not type(pr1) == list) and type(pr2) == Bicond\
                         and str(pr1) == str(pr2.left):
                        proof.append(pr2.right)
                        print ('  proof =', proof)
                    else:
                        print('That is not an acceptable use of =E1.')
                elif rule[0] == '=E2':
                    if type(pr1) == list and len(pr1) == 1 and type(pr2) == \
                       Bicond and str(pr1[0]) == str(pr2.right):
                        proof.append(pr2.left)
                        print ('  proof =', proof)
                    elif (not type(pr1) == list) and type(pr2) == list and \
                         len(pr2) == 1 and type(pr2[0]) == Bicond and \
                         str(pr1) == str(pr2[0].right):
                        proof.append(pr2[0].left)
                        print ('  proof =', proof)
                    elif type(pr1) == list and len(pr1) == 1 and type(pr2) == \
                         list and len(pr2) == 1 and type(pr2[0]) == Bicond \
                         and str(pr1[0]) == str(pr2[0].right):
                        proof.append(pr2[0].left)
                        print('  proof =', proof)
                    elif (not type(pr1) == list) and type(pr2) == Bicond\
                         and str(pr1) == str(pr2.right):
                        proof.append(pr2.left)
                        print ('  proof =', proof)
                    else:
                        print('That is not an acceptable use of =E2.')
                elif rule[0] == 'Assume':
                    #here we begin a subproof with an assumption specified by the user, now contained within a single-element
                    #list (see README for details)
                    #this if condition catches user input errors (parse will print an error message)
                    if parse(tokenize(rule[1])) == None:
                        print ('  proof =', proof)
                    else:
                        assumption = parse(tokenize(rule[1]))
                        proof.append([assumption])
                        print ('  proof =', proof)
                elif rule[0] == 'FI':
                    if type(pr2) == Not and str(pr2.formula) == str(pr1):
                        proof.append(TruthValue(False))
                        print ('  proof =', proof)
                    elif type(pr2) == list and len(pr2) == 1 and \
                        type(pr2[0]) == Not and str(pr2[0].formula) == str(pr1):
                        proof.append(TruthValue(False))
                        print ('  proof =', proof)
                    elif type(pr1) == list and len(pr1) == 1 and \
                         type(pr2) == Not and str(pr2.formula) == str(pr1[0]):
                        proof.append(TruthValue(False))
                        print ('  proof =', proof)
                    elif type(pr1) == list and len(pr1) == 1 and type(pr2) == \
                         list and len(pr2) == 1 and type(pr2[0]) == Not and \
                         str(pr2[0].formula) == str(pr1[0]):
                        proof.append(TruthValue(False))
                        print ('  proof =', proof)
                    else:
                        print ('That is not a contradiction.')
                elif rule[0] == 'FE':
                    #here we ask the user to provide a formula, which will be added to the proof as a consequence of the 
                    #contradiction specified by the user
                    if type(pr1) == TruthValue and pr1.value == False:
                        e = input('Please provide a formula: ')
                        if parse(tokenize(e)) == None:
                            print ('  proof =', proof)
                        else:
                            proof.append(parse(tokenize(e)))
                            print ('  proof =', proof)
                    elif type(pr1) == list and len(pr1) == 1 and \
                         type(pr1[0]) == TruthValue and pr1[0].value == False:
                        e = input('Please provide a formula: ')
                        if parse(tokenize(e)) == None:
                            print ('  proof =', proof)
                        else: 
                            proof.append(parse(tokenize(e)))
                            print ('  proof =', proof)
                    else:
                        print ('That is not a contradiction.')
                elif rule[0] == '~I':
                    #here we must first make sure additional subproofs within the specified subproof have been closed, which 
                    #is accomplished with a for loop checking for additional single-element lists (corresponding to the 
                    #beginning of additional open subproofs); see README for details
                    nested = False
                    for n in range(int(rule[1]) + 1, len(proof)):
                        if type(proof[n]) == list and len(proof[n]) == 1:
                            print('You must first close the current subproof.')
                            nested = True
                    if type(pr1) == list and len(pr1) == 1 and type(pr2) == \
                       TruthValue and pr2.value == False and nested == False:
                        subproof = []
                        for n in range(int(rule[1]), int(rule[2]) + 1):
                            subproof.append(proof[n])
                        proof = proof[:int(rule[1])]
                        proof.append(subproof)
                        proof.append(Not(pr1[0]))
                        print ('  proof =', proof)
                    else:
                        print ('That is not an acceptable use of ~I.')
                elif rule[0] == 'R':
                    if type(pr1) == list and len(pr1) == 1:
                        proof.append(pr1[0])
                        print ('  proof =', proof)
                    else:
                        proof.append(pr1)
                        print ('  proof =', proof)
                elif rule[0] == '>I':
                    #just as with rule '~I' above, we must first check for additional subproofs with a for loop
                    nested = False
                    for n in range(int(rule[1]) + 1, len(proof)):
                        if type(proof[n]) == list and len(proof[n]) == 1:
                            print('You must first close the current subproof.')
                            nested = True
                    if type(pr1) == list and len(pr1) == 1 and nested == False:
                        subproof = []
                        for n in range(int(rule[1]), len(proof)):
                            subproof.append(proof[n])
                        proof = proof[:int(rule[1])]
                        proof.append(subproof)
                        proof.append(Implies(pr1[0], pr2))
                        print ('  proof =', proof)
                    else:
                        print('That is not an acceptable use of >I.')
                elif rule[0] == 'TI':
                    proof.append(TruthValue(True))
                    print ('  proof =', proof)
                elif rule[0] == '=I':
                    if type(pr1) == Implies and type(pr2) == Implies and \
                       str(pr1.left) == str(pr2.right) and str(pr1.right) == \
                       str(pr2.left):
                        proof.append(Bicond(pr1.left, pr1.right))
                        print ('  proof =', proof)
                    elif type(pr1) == list and len(pr1) == 1 and type(pr2) == \
                         Implies and str(pr1[0].left) == str(pr2.right) and \
                         str(pr1[0].right) == str(pr2.left):
                        proof.append(Bicond(pr1[0].left, pr1[0].right))
                        print ('  proof =', proof)
                    elif type(pr1) == Implies and type(pr2) == list and \
                         len(pr2) == 1 and str(pr1.left) == str(pr2[0].right) \
                         and str(pr1.right) == str(pr2[0].left):
                        proof.append(Bicond(pr1.left, pr1.right))
                        print ('  proof =', proof)
                    elif type(pr1) == list and len(pr1) == 1 and type(pr2) == \
                         list and len(pr2) == 1 and str(pr1[0].left) == \
                         str(pr2[0].right) and str(pr1[0].right) == \
                         str(pr2[0].left):
                        proof.append(Bicond(pr1[0].left, pr1[0].right))
                        print ('  proof =', proof)
                    else:
                        print ('That is not an acceptable use of =I.')
                elif rule[0] == 'vI1':
                    e = input('Please provide a formula: ')
                    if parse(tokenize(e)) == None:
                        print ('  proof =', proof)
                    else:
                        if type(pr1) == list and len(pr1) == 1:
                            proof.append(Or(pr1[0], parse(tokenize(e))))
                            print ('  proof =', proof)
                        else:
                            proof.append(Or(pr1, parse(tokenize(e))))
                            print ('  proof =', proof)
                elif rule[0] == 'vI2':
                    e = input('Please provide a formula: ')
                    if parse(tokenize(e)) == None:
                        print ('  proof =', proof)
                    else: 
                        if type(pr1) == list and len(pr1) == 1:
                            proof.append(Or(parse(tokenize(e)), pr1[0]))
                            print ('  proof =', proof)
                        else:
                            proof.append(Or(parse(tokenize(e)), pr1))
                            print ('  proof =', proof)
                elif rule[0] == 'vE':
                    if type(pr1) == Or and type(pr2) == Implies and type(pr3) \
                       == Implies and str(pr1.left) == str(pr2.left) and \
                       str(pr1.right) == str(pr3.left) and str(pr2.right) \
                       == str(pr3.right):
                        proof.append(pr2.right)
                        print ('  proof =', proof)
                    elif type(pr1) == list and len(pr1) == 1 and type(pr2) == \
                         Implies and type(pr3) == Implies and str(pr1[0].left) \
                         == str(pr2.left) and str(pr1[0].right) == \
                         str(pr3.left) and str(pr2.right) == str(pr3.right):
                        proof.append(pr2.right)
                        print ('  proof =', proof)
                    elif type(pr2) == list or type(pr3) == list:
                        print ('Conditionals cannot be assumptions.', \
                               'Use rule R to discharge assumptions.')
                    else:
                        print ('That is not an acceptable use of vE.')
                elif rule[0] == 'delete':
                    #removes the last line of the proof
                    proof = proof[:len(proof) - 1]
                    print ('  proof =', proof)
                else:
                    print ('That is not an acceptable inference rule.') 
                

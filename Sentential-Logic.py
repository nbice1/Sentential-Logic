class Not:
    opStr = '~'
    def __init__(self, formula):
        self.formula = formula
    def __str__(self):
        return self.opStr + str(self.formula)
    def __repr__(self):
        return str(self)
    def eval(self, env):
        if self.formula.eval(env) == None:
            return None
        else:
            return not self.formula.eval(env)
class BinaryOp:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return '(' + str(self.left) + ' ' + self.opStr + ' ' + \
               str(self.right) + ')'
    def __repr__(self):
        return str(self)
class And(BinaryOp): 
    opStr = '^'
    def eval(self, env):
        return self.left.eval(env) and self.right.eval(env)
class Or(BinaryOp): 
    opStr = 'v'
    def eval(self, env):
        return self.left.eval(env) or self.right.eval(env)
class Implies(BinaryOp):
    opStr = '>'
    def eval(self, env):
        return not(self.left.eval(env) and not(self.right.eval(env)))
class Bicond(BinaryOp):
    opStr = '='
    def eval(self, env):
        return (self.left.eval(env) and self.right.eval(env)) or \
               (not(self.left.eval(env)) and not(self.right.eval(env)))
class Assign(BinaryOp):
    opStr = ':'
    def eval(self, env):
        value = self.right.eval(env)
        env[self.left.name] = value
class Variable:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return str(self.name)
    __repr__ = __str__
    def eval(self, env):
        if self.name in env:
            return env[self.name]
        else:
            print ("Atomic formula %s has not been assigned a truth-value." \
                   % self.name)
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
    
seps = ['(', ')', '~', '^', 'v', '>', '=', ':', 'T', 'F']

import string

def tokenize(inputString):
    result = []
    state = 'open'
    for n in range(len(inputString)):
        if inputString[n] in seps:
            result.append(inputString[n])
            state = 'open'
        elif inputString[n] == ' ':
            state = 'open'
        else:
            for m in range(n, len(inputString)):
                if state == 'open' and (inputString[m] == ' ' or \
                inputString[m] in seps):
                    result.append(inputString[n:m])
                    state = 'word'
                elif state == 'open' and m+1 == len(inputString):
                    result.append(inputString[n:m+1])
                    state = 'word'
    return result

def valueTok(token):
    return token == 'T' or token == 'F'

def variableTok(token):
    for char in token:
        if not(char in string.ascii_letters or char in string.digits) \
           or char == 'T' or char == 'F' or char == 'v':
            return False
    return True

def parse(tokens):
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
    (parsedForm, nextIndex) = parseForm(0)
    return parsedForm

def evaluator():
    env = {}
    while True:
        e = input('%')
        if e == 'exit':
            break
        else:
            print ('%', parse(tokenize(e)).eval(env))
            print ('   env =', env)

def listMaker(string):
    result = []
    state = 'open'
    for n in range(len(string)):
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

def prover():
    proof = []
    e = input('Please state the premises: ')
    if e == 'exit':
        return None
    else:
        prems = listMaker(e)
        for pr in prems:
            proof.append([parse(tokenize(pr))])
        print ('  proof =', proof)
        while True:
            e = input('Please apply an inference rule: ')
            if e == 'exit':
                break
            else:
                rule = listMaker(e)
                if len(rule) == 2 and not rule[0] == 'Assume':
                    pr1 = proof[int(rule[1])]
                elif len(rule) == 3 and not rule[0] == 'Assume':                   
                    pr1 = proof[int(rule[1])]
                    pr2 = proof[int(rule[2])]
                elif rule[0] == 'Assume' and not len(rule) == 2:
                    print ('You can only assume a single formula.')
                elif rule[0] == 'Assume' and len(rule) == 2:
                    pass
                elif rule[0] == 'TI':
                    pass
                elif rule[0] == 'vE' and len(rule) == 4:
                    pr1 = proof[int(rule[1])]
                    pr2 = proof[int(rule[2])]
                    pr3 = proof[int(rule[3])]
                else:
                    print ('That is not an acceptable inference rule.')
                if rule[0] == '^E1':
                    if type(pr1) == And:
                        proof.append(pr1.left)
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
                    if type(pr1) == TruthValue and pr1.value == False:
                        e = input('Please provide a formula: ')
                        proof.append(parse(tokenize(e)))
                        print ('  proof =', proof)
                    elif type(pr1) == list and len(pr1) == 1 and \
                         type(pr1[0]) == TruthValue and pr1[0].value == False:
                        e = input('Please provide a formula: ')
                        proof.append(parse(tokenize(e)))
                        print ('  proof =', proof)
                    else:
                        print ('That is not a contradiction.')
                elif rule[0] == '~I':
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
                    if type(pr1) == list and len(pr1) == 1:
                        proof.append(Or(pr1[0], parse(tokenize(e))))
                        print ('  proof =', proof)
                    else:
                        proof.append(Or(pr1, parse(tokenize(e))))
                        print ('  proof =', proof)
                elif rule[0] == 'vI2':
                    e = input('Please provide a formula: ')
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
                else:
                    print ('That is not an acceptable inference rule.') 
                

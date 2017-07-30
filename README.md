# Sentential-Logic
This program can both determine the truth-value of complex formulas and construct proofs. 

The program contains two primary functions: evaluator() and prover(). 

The evaluator() function allows the user to assign truth-values to atomic formulae and then determine the truth-value of a complex formula. The prover() function allows the user to construct proofs in a sound and complete natural deduction system. 

Both functions begin by asking for user input. All formulae constructed via binary connectives must be surrounded by parentheses. For example: ((p ^ q) ^ r) is a well-formed formula while (p ^ q) ^ r is not. The single unary connective, negation, does not use parentheses. For example: ~p is a well-formed formula while ~(p) is not. ~(p ^ q) is also a well-formed formula. 

The following symbols are used as logical connectives: ~ for negation, ^ for conjunction, v for disjunction, > for the material conditional, and = for the biconditional. T and F are used for the two truth-values: True and False. In the evaluator() environment, the symbol : is used for truth-value assignments, which must also be surrounded by parentheses. For example: (p : T) assigns the truth-value T to the atomic formula p, while p : T is not a well-formed expression and will lead to an error message. 

Atomic formulae may be any strings of letters (case-sensitive) and numerical digits not containing v, T, or F, since v, T, and F all have special meanings in the formal language (disjunction, True, and False, respectively). Traditionally, atomic formulae are lower-case letters such as p, q, and r, or upper-case letters such as Q, R, and S, but longer strings such as jim or p123 are also allowed in this program. 

Either function can be exited by inputting exit. 

evaluator()

When running the evaluator() function, one should begin by assigning truth-values to atomic formulae using expressions of the form (p : T) or (q : F). All current assignments will be printed as a dictionary called env. One can then construct a complex formula using the logical connectives and the function will print its truth-value in the environment (i.e. relative to the truth-value assignments to the relevant atomic formulae), followed by the printing the dictionary of assignments. For example, if p is True and q is False, (p > (p ^ q)) will be evaluated as False. If an atomic formula in the complex formula being evaluated has not been assigned a truth-value, you will receive an error message. 

One can also use the truth-values T and F to construct complex formulae: e.g. after entering (T ^ (T v F)) the function will print True, followed by the current assignments. One can also assign atomic formulae the truth-values of complex formulae, provided the latter formulae can be evaluated as True or False. For example, if p is True and q is False, (r: (p ^ q)) will assign the truth-value False to atomic formula r. 

prover()

The prover() function begins by asking for the premises of the proof. Premises must be separated by commas. For example: inputting (p ^ (q v r)), r will construct a proof beginning with two premises. Simply pressing return (inputting an empty string) will construct a proof with no premises. 


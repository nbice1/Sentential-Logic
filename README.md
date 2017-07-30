# Sentential-Logic
This program can both determine the truth-value of complex formulas and construct proofs. 

The program contains two primary functions: evaluator() and prover(). 

The evaluator() function allows the user to assign truth-values to atomic formulas and then determine the truth-value of a complex formula. The prover() function allows the user to construct proofs in a sound and complete natural deduction system. 

Both functions begin by asking for user input. All formulas constructed via binary connectives must be surrounded by parentheses. For example: '((p ^ q) ^ r)' is a well-formed formula while '(p ^ q) ^ r' is not. The single unary connective, negation, does not use parentheses. For example: '~p' is a well-formed formula while '~(p)' is not. '~(p ^ q)' is also a well-formed formula. 

The following symbols are used as logical connectives: '~' for negation, '^' for conjunction, 'v' for disjunction, '>' for the material conditional, and '=' for the biconditional. 'T' and 'F' are used for the two truth-values: True and False. When using the evaluator() function, the symbol ':' is used for truth-value assignments, expressions for which must also be surrounded by parentheses. For example: '(p : T)' assigns the truth-value 'T' to the atomic formula 'p', while 'p : T' is not a well-formed expression and will lead to an error message. 

Atomic formulas may be any strings of letters (case-sensitive) and numerical digits not containing 'v', 'T', or 'F', since 'v', 'T', and 'F' all have special meanings in the formal language (disjunction, True, and False, respectively). Traditionally, atomic formulas are lower-case letters such as 'p', 'q', and 'r' (don't use 'v'!), or upper-case letters such as 'Q', 'R', and 'S' (don't use 'T' or 'F'!), but longer strings such as 'jim' or 'p123' are also allowed in this program. 

Either function can be exited by inputting 'exit'. 

evaluator()

When running the evaluator() function, one should begin by assigning truth-values to atomic formulas by inputting expressions of the form '(p : T)' or '(q : F)'. All current assignments will be printed as a dictionary called 'env'. One can then construct a complex formula using the logical connectives and the function will print its truth-value in the environment (i.e. relative to the truth-value assignments to the relevant atomic formulas), followed by the printing the dictionary of assignments. For example, if 'p' is True and 'q' is False, '(p > (p ^ q))' will be evaluated as False. If an atomic formula in the complex formula being evaluated has not been assigned a truth-value, you will receive an error message. 

One can also use the truth-values 'T' and 'F' to construct complex formulas: e.g. after entering '(T ^ (T v F))' the function will print True, followed by the current assignments. One can also assign atomic formulas the truth-values of complex formulas, provided the latter formulas can be evaluated as True or False. For example, if 'p' is True and 'q' is False, '(r: (p ^ q))' will assign the truth-value False to atomic formula 'r'. 

prover()

The prover() function begins by asking for the premises of the proof. Premises must be separated by commas. For example: inputting '(p ^ (q v r)), r' will construct a proof beginning with two premises. Simply pressing return (inputting an empty string) will construct a proof with no premises. The user will then be asked to apply an inference rule. 

A proof is represented as a list. All elements of the list are either formulas or further lists. All assumptions (including the initial premises) are contained within single-element lists. For example, if the user inputs '(p ^ (q v r)), r' as the initial premises, the initial proof will be stored and printed as the list [[(p ^ (q v r))], [r]]. If the user then applies conjunction elimination to the first conjunct of the first premise (as explained below), the proof will be printed as [[(p ^ (q v r))], [r], p]. Each application of an inference rule adds a new element to the list corresponding to the derived formula. 

The following inference rules can be used, leading to a sound and complete natural deduction system: 

1. '^E1, n': This applies conjunction elimination to the first conjunct of the formula located at position n in the proof-list. For example, if the proof is [[(p ^ q)]], inputting '^E1, 0' will modify and print the proof as [[(p ^ q)], p]. 

2. '^E2, n': This applies conjunction elimination to the first conjunct of the formula located at position n in the proof-list. For example, if the proof is [[(p ^ q)]], inputting '^E2, 0' will modify and print the proof as [[(p ^ q)], q]. 

3. '^I, n, m': This applies conjunction introduction to the formulas located at postions n and m in the proof-list. For example, if the proof is [[p], [q]], inputting '^I, 0, 1' will modify and print the proof as [[p], [q], (p ^ q)]. 

4. 'Assume: X': This creates a subproof beginning with the formula 'X' as assumption. Further inference rules will be applied within the subproof until an inference rule is used which exits the subproof. For example, if the initial proof has no premises [], inputting 'Assume: (~p v ~q)' will begin a subproof with '(~p v ~q)' as assumption, where the proof will be stored and printed as [[(~p v ~q)]]. Note that the formula is embedded within a single-element list to indicate that it is an assumption rather than a derived formula. 

5. 

#!/usr/bin/env python3
# Jeff Shao IT361 Final Project: logic.py
# A simple script to generate truth tables and analyze Boolean equations, written in Python 3.

import re


# Function to get a Boolean equation from the user.
def getEquation():

    # Logical loop for equation input. The only way to terminate this loop is the final return call.
    while True:
        # Get input from user.
        equation = input(f'Please enter a Boolean equation.\n')

        # Logic for parentheses. We make a counter that increments for every open paren '(' and decrements
        # for every close paren ')'. If we ever find a close paren that doesn't correspond to an open paren,
        # or if at the end of the equation we don't have an equal number of open and close parens, the equation is invalid.
        paren_count = 0

        for char in equation:
            if char == '(':
               paren_count += 1 # No need to check for anything here: starting with multiple open parens is not illegal.
            elif char == ')':
                paren_count -= 1
                # If we ever have too many close parens though, that is illegal. Stop counting parens and let the
                # paren_count != 0 clause trigger.
                if paren_count < 0:
                    break

        # Finally, we make sure that there is a close paren for each open paren.
        if paren_count != 0:
            print('Misplaced parentheses. Please try again.')
            continue # Restart the while loop.

        # Remove whitespace and () from input.
        stripped_equation = re.sub('\s+|[()]', '', equation)

        # Very basic logic check: once whitespace and () are removed from equation, check that the
        # equation consists of capital letters (potentially with "not"s in front of them) separated by operators.
        if not re.match('^(not)*[A-Z]((and|or|xor)(not)*[A-Z])*$', stripped_equation):
            print('Invalid syntax detected. Please try again.')
            continue # Restart the while loop.

        # If we get this far, congratulations! The equation appears to be valid and we can break out of the loop.
        return equation


# Function to return a list of all the different variables that exist in an equation.
def getVars(equation):
    vars = []
    for char in equation:
        if re.match('[A-Z]', char) and char not in vars:
            vars.append(char)
    return vars


# Function to evaluate the result of a particular Boolean equation.
def evalEquation(equation, vars, varVals={}):

    # If we have assigned values for variables already, usually through genTruthTable, then simply put them into
    # the equation. Note that we check to make sure we're not accidentally matching the "T" in "True" or the "F"
    # in "False" by using the negative lookahead assertion (?!alse|rue).
    if varVals:
        for var in vars:
            equation = re.sub(f'{var}(?!alse|rue)', str(varVals[var]), equation)

    # Otherwise, we ask the user to input values for each variable.
    else:
        print(f'\nPlease enter "T" or "1" for True and "F" or "0" for False.')

        for var in vars:
            # Non-terminating while loop that only exits if user input is found to be valid.
            while True:
                replacement = input(f'What is the value of {var}? ')
                if replacement in ['T', 't', '1']:
                    equation = re.sub(f'{var}(?!alse|rue)', 'True', equation)
                    varVals[var] = True
                    break
                elif replacement in ['F', 'f', '0']:
                    equation = re.sub(f'{var}(?!alse|rue)', 'False', equation)
                    varVals[var] = False
                    break

                # If value is not recognized, reprompt for user input by continuing the while loop.
                else:
                    print('Input not recognized. Please resubmit.')

    # Since "xor" is not actually a legal Python command, we replace it with "!=", which effectively does the same thing
    # on Boolean values.
    equation = re.sub('xor', '!=', equation)

    # Evaluate the final equation with our replacements for the variables, then save the result into varVals, which doubles as
    # our return output.
    varVals['Result'] = bool(eval(equation))

    return varVals


# Recursive function to generate a truth table for all possible values of a Boolean equation.
def genTruthTable(equation, vars, varVals={}):

    # Recursive condition: as long as there are items in vars, remove one of them
    # and call genTruthTable again.
    if vars:
        nextVar = vars.pop(0)
        varVals[nextVar] = True
        # Note the "vars.copy()". Since Python only passes the _reference_ to a set/list,
        # we need to ensure that we make copies of vars instead of passing the original reference:
        # otherwise, the second genTruthTable call below will contain less vars than the first.
        genTruthTable(equation, vars.copy(), varVals)
        varVals[nextVar] = False
        genTruthTable(equation, vars.copy(), varVals)

    # Termination condition: when we run out of vars, we've iterated across all the possible variables.
    else:
        # Submit the equation and the various varVals to evalEquation and get the results.
        results = evalEquation(equation, getVars(equation), varVals)

        # Print out a line containing the results obtained.
        print('| ', end='')
        for key, data in results.items():
            if key != 'Result':
                if data:
                    print('T | ', end='')
                else:
                    print('F | ', end='')
            else:
                if data:
                    print('  T    |')
                else:
                    print('  F    |')


# Main program function.
def main():
    print(f'Welcome to logic.py!\n')

    # Get an equation from the user.
    equation = getEquation()

    # Analyze the equation and find out what the individual variables are. We use this
    # no matter which mode the user picks, so better to do this now than later.
    vars = getVars(equation)

    print(f'\n1. Analyze a specific equation.\n2. Generate the entire truth table.\n')

    # Have user choose which mode they want to activate.
    while True:
        choice = input('Select "1" or "2". ')

        # Single equation solve.
        if choice == '1':
            # Submit the equation and its variables to evalEquation, then get the results.
            results = evalEquation(equation, vars)

            # Print the results.
            resultStatement = f'\nThe result of "{equation}" for '
            for key, data in results.items():
                if key != 'Result':
                    resultStatement += f'{key} = "{data}"; '
                else:
                    resultStatement += f'is "{data}".\n'
            print(resultStatement)
            break

        # Truth table generation.
        elif choice == '2':
            print(f'\nHere is the truth table for "{equation}":\n')

            # Table header.
            headerText = '| '
            for var in vars:
                headerText += var + ' | '
            headerText += 'Result |'
            sepLength = len(headerText)
            print('+' + '-' * (sepLength - 2) + '+')
            print(headerText)
            print('+' + '-' * (sepLength - 2) + '+')

            # Call genTruthTable, which prints out the rest of the table.
            genTruthTable(equation, vars)

            # Close table off with another separator.
            print('+' + '-' * (sepLength - 2) + '+')
            print()
            break

        # Input not understood. Reprompt user.
        else:
            print('Invalid input.')

    # Farewell statement.
    print('Thank you for using logic.py!')
    input('PRESS ANY KEY TO EXIT')
    return 0


if __name__ == '__main__':
    main()

# logic.py
A simple Python command-line utility that evaluates and outputs the result of Boolean equations inputted by the user.

## Features
* Two modes: specific variable evaluation and truth table generation.
* Supports xor!

## Compatibility
Requires Python 3 or later.

## Usage
A direct command-line call to `./logic.py` inside the appropriate directory should work on most systems with Python 3 installed; if it does not, try `python logic.py` or `python3 logic.py`.

You should also be able to double-click the file itself and launch it in Windows at least.

## Boolean Equation Syntax
As of now, logic.py only supports the following Boolean operators, along with parentheses:  
  
`and`  
`or`  
`xor`   
`not` - All statements involving "not" should be wrapped in parentheses, just to avoid any potential errors. e.g. "A and (not B)" instead of "A and not B"
  
**No other operators are available at this time.** Note that all operators are in lowercase.
  
Additionally, all variables must be entered in UPPERCASE.

The program will try to enforce these conditions, but may not be able to do so perfectly. if you encounter an error, double-check your syntax.

An example of a valid equation is:

`(A and B) xor (not C)`

## Disclaimer
This program comes without warranty of any kind. It may or may not harm your device. Please use with care, as any damage cannot be related back to the author.

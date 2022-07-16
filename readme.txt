relative - a simple stack based language but i put the syntax into a woodchipper and then into a sausage grinder and then into a pressure cooker and then ate it and shat it out
and then fed it to my dog

user defined variables are in the same "id space" as the built in functions/constants, so a built in user defined variable
cannot have the same id as a built in function/constant

all variables are resizeable arrays of numbers that can represent integers, strings, or functions

variables do not have to contain data, a variable can contain executable code too

it is a stack based programming language, and each stack "cell" (idk the actual name) works like a variable

all variables are global. fuck scoping i dont want to deal with stack frames or whatever

how the language works:

everything is based on an id system, where the ids are integer numbers.

variables are used via id, functions are called by id, *everything* is an id.

This means that the programs are just a list of numbers seperated by spaces and/or newlines. comments are not yet supported.

this is somewhat difficult to explain in text, but you don't actually write many ids in the program. The appropriate ids and data
for the program are generated from the source code, which consists of a lists of numbers that add together to make ids.

you start with 0, so the first number in the program will always be an id. but to get the next id, you don't type it in, 
you write the number that you would add to the id before it(not the number before it) in the program to demonstrate this, 
i'll write an example program, a basic "HELLO WORLD!":

0  ; the id for pushing data to the stack
13 ; the argument for the call to push (the only function to be called like this), states that the next 13 numbers should be pushed to the top cell
59 ; 72 is the ascii code for 'H', 72-13 is 59
-3 ; 69 is the ascii code for 'E', 69-72 is -3
7  ; 76 is the ascii code for 'L', 76-69 is 7
0  ; 76 is the ascii code for 'L', 76-76 is 0
3  ; 79 is the ascii code for 'O', 79-76 is 3
-47; 32 is the ascii code for ' ', 32-79 is -47
55 ; 87 is the ascii code for 'W', 87-32 is 55
-8 ; 79 is the ascii code for 'O', 79-87 is -8
3  ; 82 is the ascii code for 'R', 82-79 is 3
-6 ; 76 is the ascii code for 'L', 76-82 is -6
-8 ; 67 is the ascii code for 'D', 67-76 is -8
-35; 33 is the ascii code for '!', 33-67 is -35
-23; 10 is the ascii code for '\n',10-33 is -23
12 ; 22 is the id for printing the top cell of the stack, 10+12 = 22
-1 ; 21 is the id for ending the program, 22-1 = 21


built in id's:

stack manipulation
0 - push(n) pushes n amount of numbers after the function call onto the top cell of the stack
1 - pushvar(id) pushes contents of the variable referenced by id to the top cell of the stack
2 - store(id) stores the top cell of the stack to the variable referenced by id. if a variable with the id does not exist,
it is created.
3 - duplicate() pushes a copy of the top cell of the stack to the stack
4 - pop() removes the top cell of the stack
5 - set_index(val, index) takes the top cell of the stack as an index into the third to top cell of the stack, and the second to top cell of the stack as the value to set the
index to. 
6 - get_index(index) takes the top cell of the stack as an index into the second to top cell, and pushes that value to the stack
7 - get_length pushes length of the top cell of the stack to the stack
8 - set_length(length) takes the second to top cell of the stack as length, and resizes the top cell of the stack to be that length, either filling the empty space with zero,
or truncating the cell to the desired length

math (only valid if the affected cells are single numbers)
9 - add(n1,n2) adds top 2 cells of the stack (re-aligned to be relative to 0).
10 - subtract(n1,n2) subtracts the second cell of the stack from the top cells on the stack (both re-aligned to be relative to 0).
11 - multiply(n1,n2) multiplies the top 2 cells of the stack
12 - divide(n1,n2) divides second cell of the stack by the top cell

comparisons - all comparisons push 1 to the top of the stack if true, or 9 if false
13 - and(n1,n2) ands the top 2 cells of the stack
14 - not(n) inverts the top cell on the stack (if its not 0, switch it to 0. if it is 0, switch it to 1).
15 - or(n1,n2) ors the top 2 cells of the stack
16 - less_than(n1,n2) checks if the second to top cell of the stack is less than the top cell
17 - greater_than(n1,n2) checks if the second to top cell of the stack is greater than the top cell 

18 - equal(n1,n2) checks if the top 2 cells of the stack are equal, valid even if the top 2 cells are not single numbers

flow control
19 - conditional(condition,trueblock,falseblock) - takes the top 3 cells of the stack. the third to top is the condition and  must be a single number, 0 is treated as false and 
non-0 is true.  the second to top and top cells must contain executable code. the second to top cell of the stack is run if the condition is true, and the top cell is run if
the condition is false.
20 - run(block) runs the top cell of the stack as executable code, will repeat it until a break()/return() is found
21 - break()/return() breaks out of the current code section, essentially a return statement. if called in the main section (not inside a variable), it will exit the program.

i/o
22 - print_string() - prints the top cell of the stack (only valid if the top cell of the stack is a valid ascii string)
23 - print_numbers() - prints the top cell of the stack as a list of numbers seperated by a space
24 - input() - takes in a line of stdin input and pushes it to the top of the stack
25 - input_int() - takes in a line of stdin input, converts it to an integer, and pushes it to the top of the stack
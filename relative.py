import re
import sys
# for running code blocks: create code block class that has an array of instructions and a instruction pointer.
# then, have the code blocks be stored in an array, basically another stack
# the codeblock at the top of the stack runs repeatedly
# a return statement pops the current code block off the stack and increments the new current code block's instruction pointer by 1

class Block:
    instructions = []
    instruction_pointer = 0
    
    def __init__(self, instructions):
        self.instructions = instructions

def derelativize(relative_prog):
    last_id = 0
    new_id = 0

    program = []

    for relative_id in relative_prog:
        new_id = relative_id+last_id
        program.append(new_id)
        last_id=new_id
    return program

file = open(sys.argv[1])
filestring = file.read()
relative_program = re.split(r" +|\n+",filestring)
relative_program2 = []

for i in range(0,len(relative_program)):
    if relative_program[i] != '':
        relative_program2.append(int(relative_program[i]))

print(relative_program2)
instructions = derelativize(relative_program2)
print(instructions)

blocks = []

program = Block(instructions)

blocks.append(program)


stack = []

vars = {
    
}

def push():
    blocks[len(blocks)-1].instruction_pointer+=1
    count = blocks[len(blocks)-1].instructions[blocks[len(blocks)-1].instruction_pointer]
    pushedval = []
    while count > 0:
        blocks[len(blocks)-1].instruction_pointer+=1
        pushedval.append(blocks[len(blocks)-1].instructions[blocks[len(blocks)-1].instruction_pointer])
        count-=1
    stack.append(pushedval)

def push_var():
    blocks[len(blocks)-1].instruction_pointer+=1
    id = blocks[len(blocks)-1].instructions[blocks[len(blocks)-1].instruction_pointer]
    stack.append(vars[id])

def store():
    id = stack.pop()[0]
    vars[id] = stack.pop()

def duplicate():
    topval = stack.pop()
    stack.append(topval)
    stack.append(topval)

def pop():
    stack.pop()

def set_index():
    index = stack.pop()
    val = stack.pop()
    arr = stack.pop()
    arr[index] = val
    stack.append(arr)

def get_index():
    index = stack.pop()
    arr = stack.pop()
    stack.append(arr)
    stack.append([arr[index]])

def get_length():
    arr = stack.pop()
    stack.append(arr)
    stack.append([len(arr)])

def set_length():
    length = stack.pop()
    arr = stack.pop()
    if length < len(arr):
        arr = arr[:length-len(arr)]
    elif length > len(arr):
        for i in range(0,length-len(arr)):
            arr.append(0)
    stack.append(arr)

def add():
    n2 = stack.pop()[0]
    n1 = stack.pop()[0]
    stack.append([n1+n2])

def subtract():
    n2 = stack.pop()[0]
    n1 = stack.pop()[0]
    stack.append([n1-n2])

def multiply():
    n2 = stack.pop()[0]
    n1 = stack.pop()[0]
    stack.append([n1*n2])

def divide():
    n2 = stack.pop()[0]
    n1 = stack.pop()[0]
    stack.append([n1/n2])

def rel_and():
    n2 = stack.pop()[0]
    n1 = stack.pop()[0]
    if n1 and n2:
        stack.append([1])
    else:
        stack.append([0])

def rel_not():
    n1 = stack.pop()[0]
    if n1 == 0:
        stack.append([1])
    else:
        stack.append([0])

def rel_or():
    n2 = stack.pop()[0]
    n1 = stack.pop()[0]
    if n1 or n2:
        stack.append([1])
    else:
        stack.append([0])

def less_than():
    n2 = stack.pop()[0]
    n1 = stack.pop()[0]
    if n1<n2:
        stack.append([1])
    else:
        stack.append([0])

def greater_than():
    n2 = stack.pop()[0]
    n1 = stack.pop()[0]
    if n1>n2:
        stack.append([1])
    else:
        stack.append([0])

def equal():
    n2 = stack.pop()
    n1 = stack.pop()
    if n1 == n2:
        stack.append([1])
    else:
        stack.append([0])

def conditional():
    falserun = stack.pop()
    truerun = stack.pop()
    condition = stack.pop()[0]
    if condition != 0:
        blocks.append(Block(truerun))
    else:
        blocks.append(Block(falserun))
    blocks[len(blocks)-1].instruction_pointer -= 1

def run():
    code = stack.pop()
    blocks.append(Block(code))

def rel_return():
    blocks.pop()

def print_string():
    arr = stack.pop()
    string = ""
    for c in arr:
        string += chr(c)
    print(string,end="")

def print_numbers():
    arr = stack.pop()
    for n in arr:
        print(n,end=" ")
    print("\n")

def rel_input():
    string = input()
    arr = []
    for c in string:
        arr.append(ord(c))
    stack.append(arr)

def rel_input_int():
    val = int(input())
    stack.append([val])

vars = {
    0:push,
    1:push_var,
    2:store,
    3:duplicate,
    4:pop,
    5:set_index,
    6:get_index,
    7:get_length,
    8:set_length,
    9:add,
    10:subtract,
    11:multiply,
    12:divide,
    13:rel_and,
    14:rel_not,
    15:rel_or,
    16:less_than,
    17:greater_than,
    18:equal,
    19:conditional,
    20:run,
    21:rel_return,
    22:print_string,
    23:print_numbers,
    24:rel_input,
    25:rel_input_int
}
while len(blocks) > 0:
    vars[blocks[len(blocks)-1].instructions[blocks[len(blocks)-1].instruction_pointer]]()
    if len(blocks) > 0:
        blocks[len(blocks)-1].instruction_pointer+=1
        if blocks[len(blocks)-1].instruction_pointer >= len(blocks[len(blocks)-1].instructions):
            blocks[len(blocks)-1].instruction_pointer = 0
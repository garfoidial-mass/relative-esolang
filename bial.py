import re
import sys
class Block:
    instructions = []
    instruction_pointer = 0
    
    def __init__(self, instructions):
        self.instructions = instructions


file = open(sys.argv[1])
filestring = file.read()
filestring+="\n"
filestring = re.sub(r"\;(.*)(.*?)\n","",filestring)
program = re.split(r" +|\n+",filestring)
program2 = []

for i in range(0,len(program)):
    if program[i] != '':
        program2.append(int(program[i]))

print(program2)

#i need an if and skip

blocks = []

program = Block(program2)

blocks.append(program)


stack = []

vars = {
    
}

def bial_push():
    blocks[len(blocks)-1].instruction_pointer+=1
    count = blocks[len(blocks)-1].instructions[blocks[len(blocks)-1].instruction_pointer]
    pushedval = []
    while count > 0:
        blocks[len(blocks)-1].instruction_pointer+=1
        pushedval.append(blocks[len(blocks)-1].instructions[blocks[len(blocks)-1].instruction_pointer])
        count-=1
    stack.append(pushedval)

def bial_push_var():
    blocks[len(blocks)-1].instruction_pointer+=1
    id = blocks[len(blocks)-1].instructions[blocks[len(blocks)-1].instruction_pointer]
    stack.append(vars[id])

def bial_store():
    id = stack.pop()[0]
    vars[id] = stack.pop()

def bial_duplicate():
    if len(stack) > 0:
        topval = stack.pop()
        stack.append(topval)
        stack.append(topval)

def bial_pop():
    stack.pop()

def bial_set_index():
    index = stack.pop()
    val = stack.pop()
    arr = stack.pop()
    arr[index] = val
    stack.append(arr)

def bial_get_index():
    index = stack.pop()
    arr = stack.pop()
    stack.append(arr)
    stack.append([arr[index]])

def bial_get_length():
    arr = stack.pop()
    stack.append(arr)
    stack.append([len(arr)])

def bial_set_length():
    length = stack.pop()
    arr = stack.pop()
    if length < len(arr):
        arr = arr[:length-len(arr)]
    elif length > len(arr):
        for i in range(0,length-len(arr)):
            arr.append(0)
    stack.append(arr)

def bial_swap():
    top = stack.pop()
    second = stack.pop()
    stack.append(top)
    stack.append(second)

def bial_add():
    n2 = stack.pop()[0]
    n1 = stack.pop()[0]
    
    stack.append([n1+n2])

def bial_subtract():
    n2 = stack.pop()[0]
    n1 = stack.pop()[0]
    stack.append([n1-n2])

def bial_multiply():
    n2 = stack.pop()[0]
    n1 = stack.pop()[0]
    stack.append([n1*n2])

def bial_divide():
    n2 = stack.pop()[0]
    n1 = stack.pop()[0]
    stack.append([n1/n2])

def bial_and():
    n2 = stack.pop()[0]
    n1 = stack.pop()[0]
    if n1 and n2:
        stack.append([1])
    else:
        stack.append([0])

def bial_not():
    n1 = stack.pop()[0]
    if n1 == 0:
        stack.append([1])
    else:
        stack.append([0])

def bial_or():
    n2 = stack.pop()[0]
    n1 = stack.pop()[0]
    if n1 or n2:
        stack.append([1])
    else:
        stack.append([0])

def bial_less_than():
    n2 = stack.pop()[0]
    n1 = stack.pop()[0]
    if n1<n2:
        stack.append([1])
    else:
        stack.append([0])

def bial_greater_than():
    n2 = stack.pop()[0]
    n1 = stack.pop()[0]
    if n1>n2:
        stack.append([1])
    else:
        stack.append([0])

def bial_equal():
    n2 = stack.pop()
    n1 = stack.pop()
    if n1 == n2:
        stack.append([1])
    else:
        stack.append([0])

def bial_skip():
    count = stack.pop()[0]
    blocks[len(blocks)-1].instruction_pointer += count

def bial_if():
    truelen = stack.pop()
    condition = stack.pop()[0]
    if condition != 0:
        return
    else:
        stack.append(truelen)
        bial_skip()

def bial_run():
    code = stack.pop()
    blocks.append(Block(code))
    blocks[len(blocks)-1].instruction_pointer -= 1

def bial_return():
    blocks.pop()


def bial_print_string():
    arr = stack.pop()
    string = ""
    for c in arr:
        string += chr(c)
    print(string,end="")

def bial_print_numbers():
    arr = stack.pop()
    for n in arr:
        print(n,end=" ")
    print("\n")

def bial_input():
    string = input()
    arr = []
    for c in string:
        arr.append(ord(c))
    stack.append(arr)

def bial_input_int():
    val = int(input())
    stack.append([val])

funcs = {
    0:bial_push,
    1:bial_push_var,
    2:bial_store,
    3:bial_duplicate,
    4:bial_pop,
    5:bial_set_index,
    6:bial_get_index,
    7:bial_get_length,
    8:bial_set_length,
    9:bial_add,
    10:bial_subtract,
    11:bial_multiply,
    12:bial_divide,
    13:bial_and,
    14:bial_not,
    15:bial_or,
    16:bial_less_than,
    17:bial_greater_than,
    18:bial_equal,
    19:bial_skip,
    20:bial_if,
    21:bial_run,
    22:bial_return,
    23:bial_print_string,
    24:bial_print_numbers,
    25:bial_input,
    26:bial_input_int,
    27:bial_swap
}
while len(blocks) > 0:
    funcs[blocks[len(blocks)-1].instructions[blocks[len(blocks)-1].instruction_pointer]]()
    if len(blocks) > 0:
        blocks[len(blocks)-1].instruction_pointer+=1
        if blocks[len(blocks)-1].instruction_pointer >= len(blocks[len(blocks)-1].instructions):
            blocks[len(blocks)-1].instruction_pointer = 0
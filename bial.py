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
    id = stack.pop()[0]
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
    val = stack.pop()[0]
    arr = stack.pop()
    arr[index] = val
    stack.append(arr)

def bial_get_index():
    index = stack.pop()
    arr = stack.pop()
    stack.append([arr[index]])

def bial_get_length():
    arr = stack.pop()
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
    temp = []
    n2 = stack.pop()
    n1 = stack.pop()
    if len(n1) <= len(n2):
        for i in range(0, len(n2)-len(n1)):
            n1.append(0)
    else:
        for i in range(0, len(n1)-len(n2)):
            n2.append(0)

    for i in range(0,len(n2)):
        temp.append(n2[i]+n1[i])
    
    stack.append(temp)

def bial_subtract():
    temp = []
    n2 = stack.pop()
    n1 = stack.pop()
    if len(n1) <= len(n2):
        for i in range(0, len(n2)-len(n1)):
            n1.append(0)
    else:
        for i in range(0, len(n1)-len(n2)):
            n2.append(0)

    for i in range(0,len(n2)):
        temp.append(n2[i]-n1[i])
    
    stack.append(temp)

def bial_multiply():
    temp = []
    n2 = stack.pop()
    n1 = stack.pop()
    if len(n1) <= len(n2):
        for i in range(0, len(n2)-len(n1)):
            n1.append(0)
    else:
        for i in range(0, len(n1)-len(n2)):
            n2.append(0)

    for i in range(0,len(n2)):
        temp.append(n2[i]*n1[i])
    
    stack.append(temp)

def bial_divide():
    temp = []
    n2 = stack.pop()
    n1 = stack.pop()
    if len(n1) <= len(n2):
        for i in range(0, len(n2)-len(n1)):
            n1.append(0)
    else:
        for i in range(0, len(n1)-len(n2)):
            n2.append(0)

    for i in range(0,len(n2)):
        temp.append(n2[i]/n1[i])
    
    stack.append(temp)

def bial_and():
    temp = []
    n2 = stack.pop()
    n1 = stack.pop()
    if len(n1) <= len(n2):
        for i in range(0, len(n2)-len(n1)):
            n1.append(0)
    else:
        for i in range(0, len(n1)-len(n2)):
            n2.append(0)

    for i in range(0,len(n2)):
        temp.append(int(n2[i] and n1[i]))
    
    stack.append(temp)

def bial_not():
    temp = []
    n1 = stack.pop()
    for i in range(0,len(n1)):
        if n1[i] == 0:
            temp.append(1)
        else:
            temp.append(0)
    stack.append(temp)

def bial_or():
    temp = []
    n2 = stack.pop()
    n1 = stack.pop()
    if len(n1) <= len(n2):
        for i in range(0, len(n2)-len(n1)):
            n1.append(0)
    else:
        for i in range(0, len(n1)-len(n2)):
            n2.append(0)

    for i in range(0,len(n2)):
        temp.append(int(n2[i] or n1[i]))
    
    stack.append(temp)

def bial_less_than():
    temp = []
    n2 = stack.pop()
    n1 = stack.pop()
    if len(n1) <= len(n2):
        for i in range(0, len(n2)-len(n1)):
            n1.append(0)
    else:
        for i in range(0, len(n1)-len(n2)):
            n2.append(0)

    for i in range(0,len(n2)):
        temp.append(int(n2[i] < n1[i]))
    
    stack.append(temp)

def bial_greater_than():
    temp = []
    n2 = stack.pop()
    n1 = stack.pop()
    if len(n1) <= len(n2):
        for i in range(0, len(n2)-len(n1)):
            n1.append(0)
    else:
        for i in range(0, len(n1)-len(n2)):
            n2.append(0)

    for i in range(0,len(n2)):
        temp.append(int(n2[i] > n1[i]))
    
    stack.append(temp)

def bial_equal():
    temp = []
    n2 = stack.pop()
    n1 = stack.pop()
    if len(n1) <= len(n2):
        for i in range(0, len(n2)-len(n1)):
            n1.append(0)
    else:
        for i in range(0, len(n1)-len(n2)):
            n2.append(0)

    for i in range(0,len(n2)):
        temp.append(int(n2[i] == n1[i]))
    
    stack.append(temp)

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
    print("")

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
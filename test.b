[0] ; push initial count for the loop
;push loop code to the stack
[dup 30 < ; checks if the the top value of the stack is less than 30 
 if ; if top of stack isnt 0, run section between if and colon, else run block between colon and period
 dup printn [1] + : ; print the top cell of the stack as numbers, then add 1 to it
 pop return . ; return from the loop
]
run ; run the loop
return
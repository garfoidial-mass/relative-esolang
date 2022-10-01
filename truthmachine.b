[
    inputi
    [   
        dup [1] = if [1] printn return : .
        dup [0] = if [[0] printn] run : .
        return
    ]
    run return
]

truthmachine store
truthmachine val run
return
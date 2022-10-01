package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"unicode"
)

type TokenType string

type NodeType string

const (
	TOK_Value      TokenType = "Value"
	TOK_Identifier TokenType = "Identifier"
	TOK_Builtin    TokenType = "Builtin"
	TOK_Control    TokenType = "Control"
	TOK_ControlEnd TokenType = "ControlEnd"
	TOK_None       TokenType = "None"
)

const (
	NODE_None      NodeType = "None"
	NODE_IfBlock   NodeType = "IfBlock"
	NODE_PushBlock NodeType = "PushBlock"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

type Token struct {
	tokenType TokenType
	chars     string
}

var ids = map[string]int{
	"[":      0,
	"val":    1,
	"store":  2,
	"dup":    3,
	"pop":    4,
	"seti":   5,
	"geti":   6,
	"getl":   7,
	"setl":   8,
	"+":      9,
	"-":      10,
	"*":      11,
	"/":      12,
	"&":      13,
	"!":      14,
	"|":      15,
	"<":      16,
	">":      17,
	"=":      18,
	"skip":   19,
	"if":     20,
	"run":    21,
	"return": 22,
	"prints": 23,
	"printn": 24,
	"inputs": 25,
	"inputi": 26,
	"swap":   27,
	":":      30,
}

func createTokens(tokenStrings [][]string) []Token {
	tokens := make([]Token, 0)
	for _, tok := range tokenStrings {
		var token Token
		token.chars = tok[0]
		if (token.chars == "[") || (token.chars == "if") {
			token.tokenType = TOK_Control
		} else if (token.chars == "]") || (token.chars == ".") {
			token.tokenType = TOK_ControlEnd
		} else if ids[token.chars] != 0 {
			token.tokenType = TOK_Builtin
		} else if unicode.IsLetter(rune(token.chars[0])) {
			token.tokenType = TOK_Identifier
		} else if token.chars[0] == byte('"') || unicode.IsNumber(rune(token.chars[0])) {
			token.tokenType = TOK_Value
		} else {
			token.tokenType = TOK_None
		}
		tokens = append(tokens, token)
	}
	return tokens
}

type Node struct {
	tokens   []Token
	parent   *Node
	children [](*Node)
	nodeType NodeType
	start    int
	end      int
}

func buildtree(basenode *Node, i int) int {
	for c := i + 1; c < len(basenode.tokens); c++ {
		currentToken := basenode.tokens[c]
		if currentToken.tokenType == TOK_Control {
			newNode := new(Node)
			switch currentToken.chars {
			case "if":
				newNode.nodeType = NODE_IfBlock
			case "[":
				newNode.nodeType = NODE_PushBlock
			}
			newNode.start = c
			newNode.end = basenode.end
			newNode.tokens = basenode.tokens
			newNode.parent = basenode
			newNode.children = make([]*Node, 0)
			fmt.Println("Going further: ", c, currentToken)
			c = buildtree(newNode, c)
			basenode.children = append(basenode.children, newNode)
		} else if currentToken.tokenType == TOK_ControlEnd {
			fmt.Println("going back: ", c, currentToken)
			if basenode.parent != nil {
				print("i", c)
				basenode.end = c
				return c
			}
		}
	}
	return -1
}

func printtree(basenode *Node) {
	fmt.Println("next node:")
	fmt.Println(basenode.nodeType)
	fmt.Println(*basenode)
	if len(basenode.children) > 0 {
		for _, child := range basenode.children {
			printtree(child)
		}
	}
}

var nextID int = 35
var VarIDs map[string]int

func insert(a []int, index int, value int) []int {
	if len(a) == index { // nil or empty slice or after last element
		return append(a, value)
	}
	a = append(a[:index+1], a[index:]...) // index < len(a)
	a[index] = value
	return a
}

func translatetree(basenode *Node) []int {
	localprogram := make([]int, 0)
	childprograms := make([][]int, 0)

	if len(basenode.children) > 0 {
		for _, child := range basenode.children {
			childprograms = append(childprograms, translatetree(child))
		}
	}
	childcounter := 0
	for i := basenode.start; i <= basenode.end; i++ {
		if childcounter < len(basenode.children) {
			if i == basenode.children[childcounter].start {
				localprogram = append(localprogram, childprograms[childcounter]...)
				i = basenode.children[childcounter].end
				childcounter++
			}
		}

		currentToken := basenode.tokens[i]

		switch currentToken.tokenType {
		case TOK_Builtin:
			localprogram = append(localprogram, ids[currentToken.chars])
		case TOK_Identifier:
			if VarIDs[currentToken.chars] == 0 {
				VarIDs[currentToken.chars] = nextID
				nextID++
			}
			localprogram = append(localprogram, VarIDs[currentToken.chars])
		case TOK_Value:
			if currentToken.chars[0] == '"' {
				for _, character := range currentToken.chars {
					localprogram = append(localprogram, int(character))
				}
			} else {
				v, err := strconv.Atoi(currentToken.chars)
				if err != nil {
					fmt.Println("Invalid Integer: ", currentToken.chars)
					panic("Compilation Error!")
				}
				localprogram = append(localprogram, v)
			}
		}
	}

	switch basenode.nodeType {
	case NODE_PushBlock:
		localprogram = append([]int{0, len(localprogram)}, localprogram...)
	case NODE_IfBlock:
		truelen := 0
		for truelen = 0; truelen < len(localprogram); truelen++ { // 30 is id for ':', start of else block
			if localprogram[truelen] == 30 {
				break
			}
		}
		falselen := len(localprogram) - truelen - 1
		//skip false block
		localprogram[truelen] = 0
		localprogram = insert(localprogram, truelen+1, 1)
		localprogram = insert(localprogram, truelen+2, falselen)
		localprogram = insert(localprogram, truelen+3, ids["skip"])
		truelen += 4

		localprogram = append([]int{0, 1, truelen, ids["if"]}, localprogram...)

	}
	return localprogram
}

func main() {
	args := os.Args[1:]
	fmt.Println("compiling", args[0])

	VarIDs = make(map[string]int)

	commentre := regexp.MustCompile(`(\;(.*))`)
	tokenre := regexp.MustCompile(`(["|a-z|A-Z|0-9]+|[^a-z|^A-Z|^0-9|^ \r\n])`)
	dat, err := os.ReadFile(args[0])
	check(err)
	filestring := string(dat)
	filestring = commentre.ReplaceAllString(filestring, "")

	tokensstrings := tokenre.FindAllStringSubmatch(filestring, -1)

	tokens := createTokens(tokensstrings)

	fmt.Println("Tokens:")
	for _, tok := range tokens {
		fmt.Print(tok, ", ")
	}
	fmt.Print("\n")

	var basenode *Node = new(Node)
	basenode.children = make([]*Node, 0)
	basenode.parent = nil
	basenode.tokens = tokens
	basenode.nodeType = NODE_None
	basenode.start = 0
	basenode.end = len(tokens) - 1
	buildtree(basenode, -1)

	fmt.Println("Tree:")
	//printtree(basenode)

	program := translatetree(basenode)

	fmt.Println(program)

}

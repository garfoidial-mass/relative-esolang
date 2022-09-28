package main

import (
	"fmt"
	"os"
	"regexp"
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

func translatetree(basenode *Node, program []int) []int {
	localprogram := make([]int, 0)
	switch basenode.nodeType {
	case NODE_PushBlock:
		blocktokens := basenode.tokens[basenode.start+1 : basenode.end]
		localprogram = append(localprogram, 0, len(blocktokens))
	case NODE_IfBlock:

	}

	childCount := 0
	if len(basenode.children) > 0 {
		for i, child := range basenode.children {
			translatetree(child, localprogram)
		}
	}
}

func main() {
	args := os.Args[1:]
	fmt.Println("compiling", args[0])

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
	printtree(basenode)

}

package main

import "fmt"

func main() {
	// Declaring a single variable
	var a int
	a = 10
	fmt.Println("a:", a)

	// Declaring and initializing a variable
	var b int = 20
	fmt.Println("b:", b)

	// Type inference
	var c = 30
	fmt.Println("c:", c)

	// Short variable declaration
	d := 40
	fmt.Println("d:", d)

	// Declaring multiple variables
	var e, f, g int
	e, f, g = 50, 60, 70
	fmt.Println("e:", e, "f:", f, "g:", g)

	// Declaring and initializing multiple variables
	var h, i, j int = 80, 90, 100
	fmt.Println("h:", h, "i:", i, "j:", j)

	// Short variable declaration for multiple variables
	k, l, m := 110, 120, 130
	fmt.Println("k:", k, "l:", l, "m:", m)
}
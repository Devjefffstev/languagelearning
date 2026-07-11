package main

import "fmt"

func main() {
	// For loop
	for i := 0; i < 5; i++ {
		fmt.Println("i:", i)
	}

	// For loop with multiple variables
	for i, j := 0, 0; i < 5; i, j = i+1, j+2 {
		fmt.Println("i:", i, "j:", j)
	}

	// For loop with a single condition
	k := 0
	for k < 5 {
		fmt.Println("k:", k)
		k++
	}

	// For loop with no condition
	l := 0
	for {
		if l >= 5 {
			break
		}
		fmt.Println("l:", l)
		l++
	}

	// For loop with a continue statement
	for m := 0; m < 5; m++ {
		if m%2 == 0 {
			continue
		}
		fmt.Println("m:", m)
	}

	fmt.Println("Looping through an slice")
	taskItems := []string{"Task 1", "Task 2", "Task 3", "Task 4", "Task 5"}
	for index, task := range taskItems {
		fmt.Println("Index:", index, "Task:", task)
	}
	
	fmt.Println("Looping through an slice without index")
	taskItemW := []string{"Task 1", "Task 2", "Task 3", "Task 4", "Task 5"}
	for _, task := range taskItemW {
		fmt.Println("Task:", task)
	}

	fmt.Println("filling through a slice")
	itemsFilled := make([]int, 5)
	for index := range itemsFilled {
		itemsFilled[index] = index
	}

	fmt.Println("Looping through a map")
	taskItemsMap := map[int]string{1: "Task 1", 2: "Task 2", 3: "Task 3", 4: "Task 4", 5: "Task 5"}
	for key, task := range taskItemsMap {
		fmt.Println("Key:", key, "Task:", task)
	}

}

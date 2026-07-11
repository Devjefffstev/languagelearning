package main

import "fmt"

func main() {

	// Declaring an slice
	var taskItems= []string {"Task 1", "Task 2", "Task 3", "Task 4", "Task 5"}

	fmt.Println("taskItems:", taskItems)

	//arrays has a fixed size, slices are dynamic
	// Declaring an array
	var taskItemsArray = [5]string{"Task 1", "Task 2", "Task 3", "Task 4", "Task 5"}
	fmt.Println("taskItemsArray:", taskItemsArray)

}

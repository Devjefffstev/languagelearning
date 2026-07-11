package com.aslinformationservices.calculator;

import java.util.Scanner;

public class Calculator {

    public double add(double a, double b) {
    	// TODO: Implement custom feature logic
        return a+b;
    }

    public double subtract(double a, double b) {
    	// TODO: Implement custom feature logic
        return a-b;
    }

    public double multiply(double a, double b) {
    	// TODO: Implement custom feature logic
        return a*b;
    }

    public double divide(double a, double b) {
    	// TODO: Implement custom feature logic
        if(b==0){
         throw new IllegalArgumentException("Cannot divide by zero");

        }
        return a/b;
    }
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Taking user input for arithmetic operations
        System.out.print("Enter the first number: ");
        double num1 = scanner.nextDouble();

        System.out.print("Enter the second number: ");
        double num2 = scanner.nextDouble();

        // Example usage of Calculator methods
        Calculator calculator = new Calculator();
        System.out.println("Addition result: " + calculator.add(num1, num2));
        System.out.println("Subtraction result: " + calculator.subtract(num1, num2));
        System.out.println("Multiplication result: " + calculator.multiply(num1, num2));

        // Handling division by zero
        try {
            System.out.println("Division result: " + calculator.divide(num1, num2));
        } catch (IllegalArgumentException e) {
            System.out.println(e.getMessage());
        }

        // Taking user input for the custom mean feature
        System.out.print("Enter the number of elements for mean calculation: ");
        int numElements = scanner.nextInt();

        double[] numbers = new double[numElements];
        for (int i = 0; i < numElements; i++) {
            System.out.print("Enter number " + (i + 1) + ": ");
            numbers[i] = scanner.nextDouble();
        }

        // Example usage of CustomFeature
        CustomFeature customFeature = new CustomFeature();
        try {
            System.out.println("Mean result: " + customFeature.calculateMean(numbers));
        } catch (IllegalArgumentException e) {
            System.out.println(e.getMessage());
        }

        // Example usage of EquationSolver
        EquationSolver equationSolver = new EquationSolver();
        System.out.print("Enter co-efficient 'a' for the linear equation: ");
        double a = scanner.nextDouble();

        System.out.print("Enter co-efficient 'b' for the linear equation: ");
        double b = scanner.nextDouble();

        System.out.print("Enter constant 'c' for the linear equation: ");
        double c = scanner.nextDouble();

        // Example usage of EquationSolver
        try {
            System.out.println("Linear equation result: " + equationSolver.solveLinearEquation(a, b, c));
        } catch (IllegalArgumentException e) {
            System.out.println(e.getMessage());
        }

        // Close the scanner to prevent resource leaks
        scanner.close();
    }
}
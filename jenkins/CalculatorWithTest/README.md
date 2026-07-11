# Custom Calculator Project

## Introduction
This project is a coding exercise designed to evaluate the logical and programmatic skills of candidates. The goal is to develop the backend logic for a custom calculator application in Java 11. The application will include basic arithmetic operations and two unique features that differentiate it from standard calculators.

## Setup and Execution
- Ensure Java 11 is installed on your system.
- Clone or download this repository to your local machine.
- Use your preferred IDE or command line to compile and run the Java files.
- Implement the logic for each method in the provided classes.
- Run the tests to verify the correctness of your implementation.

## Project Structure
- `src/main/java/com/aslinformationservices/calculator`: This directory contains the Java classes where the main logic for the calculator is to be implemented.
  - `Calculator.java`: Implements basic arithmetic operations such as addition, subtraction, multiplication, and division.
  - `EquationSolver.java`: Contains the method to solve simple linear equations.
  - `CustomFeature.java`: Implements a custom feature for calculating the mean of a set of numbers.
- `src/test/java/com/aslinformationservices/calculator`: This directory contains JUnit tests for the calculator logic.
  - `CalculatorTest.java`: Test class for `Calculator.java`.

## Classes and Methods
### Calculator.java
Implement the following methods:
- `add(double a, double b)`: Returns the sum of `a` and `b`.
- `subtract(double a, double b)`: Returns the difference between `a` and `b`.
- `multiply(double a, double b)`: Returns the product of `a` and `b`.
- `divide(double a, double b)`: Returns the quotient of `a` divided by `b`.

### EquationSolver.java
Implement the following method:
- `solveLinearEquation(double a, double b, double c)`: Solves the linear equation `ax + b = c` and returns the value of `x`.

### CustomFeature.java
- `calculateMean(double... numbers)`: Calculates and returns the mean (average) of a given set of numbers. This method throws an `IllegalArgumentException` if no numbers are provided.

## Testing
Write unit tests in `CalculatorTest.java` to validate the functionality of your implementation. Ensure that your tests cover a variety of cases, including edge cases.

## Documentation
Provide detailed comments within your code to explain your logic and approach. Update this README file with any additional instructions or information about your unique feature.

## Submission
After completing the implementation and testing, submit your project as instructed by the evaluators.

Good luck!


## Note to Candidates
- Do not change the names of the provided classes and methods. Your implementation should be within the structure provided.
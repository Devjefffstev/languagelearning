package com.aslinformationservices.calculator;

public class CustomFeature {

    public double calculateMean(double... numbers) {
    	 if (numbers.length == 0) {
             throw new IllegalArgumentException("At least one number is required to calculate the mean");
         }

         double sum = 0;
         for (double num : numbers) {
             sum += num;
         }
    	// TODO: Implement custom feature logic
        return sum/numbers.length;
    }
}
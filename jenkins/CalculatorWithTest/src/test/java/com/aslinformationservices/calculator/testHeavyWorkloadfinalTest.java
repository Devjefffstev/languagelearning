package com.aslinformationservices.calculator;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class testHeavyWorkloadfinalTest {
	private static final double DELTA = 1e-15;

	@Test
	void testHeavyWorkloadfinal() {
		CustomFeature customFeature = new CustomFeature();
		int iterations = 10000; // Number of iterations to simulate workload
		System.out.println("testHeavyWorkloadfinal: " + iterations);
		int datasetSize = 1_000_000; // Size of each dataset
		double[] dataset = new double[datasetSize];

		// Populate the dataset with random values
		for (int i = 0; i < datasetSize; i++) {
			dataset[i] = Math.random() * 100;
		}

		long startTime = System.currentTimeMillis();

		// Perform multiple iterations of mean calculations
		for (int i = 0; i < iterations; i++) {
			double mean = customFeature.calculateMean(dataset);
			assertTrue(mean >= 0 && mean <= 100, "Mean should be within the expected range");
		}

		long endTime = System.currentTimeMillis();

		System.out.println("Total Execution Time for testHeavyWorkloadfinal: " + ((endTime - startTime) / (1000 * 60))
				+ " minutes" + " or " + ((endTime - startTime) / (1000)) + " seconds" + " or " + (endTime - startTime)
				+ " milliseconds");
	}
	@Test
	void testHeavyWorkloadfinal_2() {
		CustomFeature customFeature = new CustomFeature();
		int iterations = 10000; // Number of iterations to simulate workload
		System.out.println("testHeavyWorkloadfinal: " + iterations);
		int datasetSize = 1_000_000; // Size of each dataset
		double[] dataset = new double[datasetSize];

		// Populate the dataset with random values
		for (int i = 0; i < datasetSize; i++) {
			dataset[i] = Math.random() * 100;
		}

		long startTime = System.currentTimeMillis();

		// Perform multiple iterations of mean calculations
		for (int i = 0; i < iterations; i++) {
			double mean = customFeature.calculateMean(dataset);
			assertTrue(mean >= 0 && mean <= 100, "Mean should be within the expected range");
		}

		long endTime = System.currentTimeMillis();

		System.out.println("Total Execution Time for testHeavyWorkloadfinal: " + ((endTime - startTime) / (1000 * 60))
				+ " minutes" + " or " + ((endTime - startTime) / (1000)) + " seconds" + " or " + (endTime - startTime)
				+ " milliseconds");
	}
}

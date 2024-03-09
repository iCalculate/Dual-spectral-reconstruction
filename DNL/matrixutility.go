package main

/**
This module offers basic matrix operations. Matrices are represented as [][]float64 slices.
The upper level resembles rows, the lower one represents columns.
*/

/*
Returns a matrix with a single column that contains all of the array's values.
*/
func TransposeArray(array []float64) [][]float64 {
	var arrayTransposed [][]float64 = make([][]float64, len(array))
	for i, _ := range arrayTransposed {
		arrayTransposed[i] = []float64{array[i]}
	}
	return arrayTransposed
}

/*
Returns the transpose of the specified matrix
*/
func TransposeMatrix(matrix [][]float64) [][]float64 {
	if len(matrix) < 1 {
		return matrix
	}
	var matrixTransposed [][]float64 = make([][]float64, len(matrix[0]))
	for i, _ := range matrixTransposed {
		matrixTransposed[i] = make([]float64, len(matrix))
		for j, _ := range matrixTransposed[i] {
			matrixTransposed[i][j] = matrix[j][i]
		}
	}
	return matrixTransposed
}

/*
Computes the dot product of two matrices
*/
func DotProduct(matrixA, matrixB [][]float64) [][]float64 {
	var outMatrix [][]float64 = make([][]float64, len(matrixA))
	for i, _ := range matrixA {
		outMatrix[i] = make([]float64, len(matrixB[0]))
		for j, _ := range matrixB[0] {
			var sum float64 = 0
			for k, _ := range matrixB {
				sum += matrixA[i][k] * matrixB[k][j]
			}
			outMatrix[i][j] = sum
		}
	}
	return outMatrix
}

/*
Expects two matrices of the same shape. Performs an operation expressed with the provided func on each cell
and returns a matrix that contains the operation results.
*/
func MatrixOperation(matrixA, matrixB [][]float64, operator func(float64, float64) float64) [][]float64 {
	var outMatrix [][]float64 = make([][]float64, len(matrixA))
	for i, _ := range matrixA {
		outMatrix[i] = make([]float64, len(matrixA[i]))
		for j, _ := range matrixB[i] {
			outMatrix[i][j] = operator(matrixA[i][j], matrixB[i][j])
		}
	}
	return outMatrix
}

/*
Returns the top level index of the subarray with the highest value
*/
func Argmax(values [][]float64) int {
	curMax := values[0][0]
	index := 0
	for i, _ := range values {
		localMax := values[i][0]
		for j, _ := range values[i] {
			if values[i][j] > localMax {
				localMax = values[i][j]
			}
		}
		if localMax > curMax {
			curMax = localMax
			index = i
		}
	}
	return index
}

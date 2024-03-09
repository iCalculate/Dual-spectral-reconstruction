package main

import "testing"

func TestTransposeMatrix(t *testing.T) {
	correct := [][]float64{{1, 2}, {3, 4}}
	impl := TransposeMatrix([][]float64{{1, 3}, {2, 4}})
	for i, _ := range correct {
		for j, _ := range correct[i] {
			if correct[i][j] != impl[i][j] {
				t.Error("Expected matrix of {{1,2},{3,4}}")
			}
		}
	}
}
func TestTransposeMatrixSingleRow(t *testing.T) {
	correct := [][]float64{{1}, {2}, {3}, {4}}
	impl := TransposeMatrix([][]float64{{1, 2, 3, 4}})
	for i, _ := range correct {
		for j, _ := range correct[i] {
			if correct[i][j] != impl[i][j] {
				t.Error("Expected matrix of {{1},{2},{3},{4}}")
			}
		}
	}
}
func TestTransposeMatrixSingleColumn(t *testing.T) {
	correct := [][]float64{{1, 2, 3, 4}}
	impl := TransposeMatrix([][]float64{{1}, {2}, {3}, {4}})
	for i, _ := range correct {
		for j, _ := range correct[i] {
			if correct[i][j] != impl[i][j] {
				t.Error("Expected matrix of {{1, 2, 3, 4}}")
			}
		}
	}
}
func TestTransposeArray(t *testing.T) {
	correct := [][]float64{{1}, {2}, {3}, {4}}
	impl := TransposeArray([]float64{1, 2, 3, 4})
	for i, _ := range correct {
		for j, _ := range correct[i] {
			if correct[i][j] != impl[i][j] {
				t.Error("Expected matrix of {{1},{2},{3},{4}}")
			}
		}
	}
}
func TestDotProduct(t *testing.T) {
	correct := [][]float64{{11}, {25}}
	impl := DotProduct([][]float64{{1, 2}, {3, 4}}, [][]float64{{3}, {4}})
	for i, _ := range correct {
		for j, _ := range correct[i] {
			if correct[i][j] != impl[i][j] {
				t.Error("Expected matrix of {{11},{25}}")
			}
		}
	}
	correct = [][]float64{{7, 10}, {15, 22}}
	impl = DotProduct([][]float64{{1, 2}, {3, 4}}, [][]float64{{1, 2}, {3, 4}})
	for i, _ := range correct {
		for j, _ := range correct[i] {
			if correct[i][j] != impl[i][j] {
				t.Error("Expected matrix of {{7, 10}, {15, 22}}")
			}
		}
	}
}
func TestMatrixOperation(t *testing.T) {
	correct := [][]float64{{2}, {-5}}
	impl := MatrixOperation([][]float64{{1}, {3}}, [][]float64{{1}, {-8}}, func(a float64, b float64) float64 {
		return a + b
	})
	for i, _ := range correct {
		for j, _ := range correct[i] {
			if correct[i][j] != impl[i][j] {
				t.Error("Expected matrix of {{2}, {-5}}")
			}
		}
	}
}

package main

import (
	"fmt"
	"testing"
)

func TestCreateWeights(t *testing.T) {
	rows, cols := 10, 20
	weights := CreateWeights(rows, cols, func() float64 { return 0.0 })
	if len(weights) != rows {
		t.Error(fmt.Sprintf("Weights must have %v rows but has %v rows.", rows, len(weights)))
	}
	if len(weights[0]) != cols {
		t.Error(fmt.Sprintf("Weights must have %v columns but has %v columns.", cols, len(weights[0])))
	}
}

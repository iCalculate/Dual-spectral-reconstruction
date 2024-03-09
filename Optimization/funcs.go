package Optimization

import (
	"fmt"
	"math"

	"gonum.org/v1/gonum/mat"
)

func Min(a, b int) int {
	if a < b {
		return a
	}

	return b
}

func MatPrint(X mat.Matrix) {
	fa := mat.Formatted(X, mat.Prefix(""), mat.Squeeze())
	fmt.Printf("%v\n", fa)
}

type ActivationFunction struct {
	Function   func(units *mat.Dense)
	Derivative func(units *mat.Dense) *mat.Dense
}

func SigmoidF(units *mat.Dense) {
	size_out, size_in := units.Dims()

	for r := 0; r < size_in; r++ {
		for c := 0; c < size_out; c++ {
			v := units.At(r, c)
			units.Set(r, c, 1/(1+math.Exp(-1*v)))
		}
	}
}

func SigmoidDeriv(units *mat.Dense) *mat.Dense {
	var units_minus *mat.Dense

	units_minus.Apply(func(i, j int, v float64) float64 { return 1 - v }, units_minus)
	SigmoidF(units)
	SigmoidF(units_minus)

	units_minus.MulElem(units, units_minus)
	return units_minus
}

var Sigmoid ActivationFunction = ActivationFunction{Function: SigmoidF, Derivative: SigmoidDeriv}

func Linear(units *mat.Dense) {}

type Cost struct {
	Function   func(*mat.Dense, *mat.Dense) float64
	Derivative func(*mat.Dense, *mat.Dense) *mat.Dense
}

func MSE(y_hat, y *mat.Dense) float64 {
	var mses *mat.Dense
	mse := 0.0

	mses.Sub(y, y_hat)
	mses.Mul(mses, mses.T())
	mses.Scale(2, mses)

	n_examples, _ := mses.Dims()

	for i := 0; i < n_examples; i++ {
		mse += mses.At(i, 0)
	}
	mse /= float64(n_examples)

	return mse
}

func MSE_Deriv(y_hat, y *mat.Dense) *mat.Dense {

	var mses_d *mat.Dense

	mses_d.Sub(y, y_hat)

	return mses_d
}

package MLP

import (
	. "goDeep/Optimization"
	"math/rand"

	"gonum.org/v1/gonum/mat"
)

type Dense struct {
	N_Units                                        int
	Units, Activation, Weights, WeightsGrad, Delta *mat.Dense
	G                                              ActivationFunction
}

func (l *Dense) InitWeights() {
	r, c := l.Weights.Dims()
	for ri := 0; ri < r; ri++ {
		for ci := 0; ci < c; ci++ {
			l.Weights.Set(ri, ci, rand.NormFloat64())
		}
	}
}

func (ly *Dense) Init(size_in, mini_batch_size int) {
	ly.Units = mat.NewDense(mini_batch_size, ly.N_Units, nil)
	ly.Activation = mat.NewDense(mini_batch_size, ly.N_Units, nil)

	ly.Weights = mat.NewDense(ly.N_Units, size_in, nil)

	ly.Delta = mat.NewDense(ly.N_Units, size_in, nil)
	ly.WeightsGrad = mat.NewDense(ly.N_Units, size_in, nil)

	ly.InitWeights()

}

//gradient with of G with respect to Units
func (l *Dense) Gradient() *mat.Dense {
	return l.G.Derivative(l.Units)
}

package MLP

import (
	"fmt"
	. "goDeep/Optimization"
	"math/rand"

	"gonum.org/v1/gonum/mat"
)

type MLP struct {
	N_Hiddens, MiniBatchSize, Input_len int
	Hiddens                             []*Dense
	Out                                 *Dense
	J                                   Cost
}

func NewMLP(hidden_layers []Dense, input_size int, out_l *Dense) *MLP {
	nn := &MLP{N_Hiddens: 0}
	nn.Input_len = input_size

	for lj := 0; lj < len(hidden_layers); lj++ {
		nn.addHiddenLayer(&hidden_layers[lj])
	}

	// for _,v := range(nn.Hiddens){
	//     MatPrint(v.Weights)
	// }

	nn.Out = out_l
	nn.Out.Init(hidden_layers[nn.N_Hiddens-1].N_Units, nn.MiniBatchSize)

	return nn
}

func (nn *MLP) addHiddenLayer(ly *Dense) {
	nn.Hiddens = append(nn.Hiddens, ly)

	if nn.N_Hiddens > 1 {
		ly.Init(nn.Hiddens[nn.N_Hiddens-1].N_Units, nn.MiniBatchSize)
	} else {
		ly.Init(nn.Input_len, nn.MiniBatchSize)
	}

	nn.N_Hiddens++
}

/*func(nn *MLP) FeedForward() *mat.VecDense{
    nn.Hiddens[0].Units.MulVec(nn.Hiddens[0].Weights, nn.In)
    nn.Hiddens[0].Sigma(nn.Hiddens[0].Units)

    for lj := 1; lj < nn.N_Hiddens; lj++{
        nn.Hiddens[lj].Units.MulVec(nn.Hiddens[lj].Weights, nn.Hiddens[lj - 1].Units)
        nn.Hiddens[lj].Sigma(nn.Hiddens[lj].Units)
        //MatPrint(nn.Hiddens[lj].Units)
    }

    nn.Out.Units.MulVec(nn.Out.Weights, nn.Hiddens[nn.N_Hiddens - 1].Units)
    nn.Out.Sigma(nn.Out.Units)

    return nn.Out.Units
}
*/

func (nn *MLP) FeedForward(mini_batch *mat.Dense) *mat.Dense {

	nn.Hiddens[0].Units.Mul(nn.Hiddens[0].Weights, mini_batch.T())

	nn.Hiddens[0].Activation = nn.Hiddens[0].Units
	nn.Hiddens[0].G.Function(nn.Hiddens[0].Activation)

	for lj := 1; lj < nn.N_Hiddens; lj++ {
		nn.Hiddens[lj].Units.Mul(nn.Hiddens[lj].Weights, nn.Hiddens[lj-1].Units.T())
		nn.Hiddens[0].Activation = nn.Hiddens[0].Units
		nn.Hiddens[lj].G.Function(nn.Hiddens[lj].Activation)
		//MatPrint(nn.Hiddens[lj].Units)
	}

	nn.Out.Units.Mul(nn.Out.Weights, nn.Hiddens[nn.N_Hiddens-1].Units.T())
	nn.Out.Activation = nn.Out.Units
	nn.Out.G.Function(nn.Out.Activation)

	return nn.Out.Units
}

func (nn *MLP) BackwardFeed(input, y_hat *mat.Dense) {
	mini_batch_size, _ := input.Dims()

	nn.Out.Delta = nn.J.Derivative(nn.Out.Units, y_hat)

	nn.Hiddens[nn.N_Hiddens-1].WeightsGrad.Mul(nn.Out.Delta, nn.Hiddens[nn.N_Hiddens-1].Activation.T())

	nn.Hiddens[nn.N_Hiddens-1].Delta.Mul(nn.Out.Delta, nn.Hiddens[nn.N_Hiddens-1].Weights.T())
	nn.Hiddens[nn.N_Hiddens-1].Delta.MulElem(nn.Hiddens[nn.N_Hiddens-1].Gradient(), nn.Hiddens[nn.N_Hiddens-1].Delta)

	if nn.N_Hiddens > 2 {
		nn.Hiddens[nn.N_Hiddens-1].WeightsGrad.Mul(nn.Hiddens[nn.N_Hiddens-1].Delta, nn.Hiddens[nn.N_Hiddens-2].Activation.T())
		nn.Hiddens[nn.N_Hiddens-1].WeightsGrad.Scale(1.0/float64(mini_batch_size), nn.Hiddens[nn.N_Hiddens-1].WeightsGrad)

	}

	for l := nn.N_Hiddens - 2; l >= 0; l++ {
		nn.Hiddens[l].Delta.Mul(nn.Hiddens[l+1].Delta, nn.Hiddens[l+1].Weights.T())
		nn.Hiddens[l].Delta.MulElem(nn.Hiddens[l].Gradient(), nn.Hiddens[l].Delta)
		if l > 0 {
			nn.Hiddens[l].WeightsGrad.Mul(nn.Hiddens[l].Delta, nn.Hiddens[l-1].Activation.T())
			nn.Hiddens[l].WeightsGrad.Scale(1.0/float64(mini_batch_size), nn.Hiddens[l].WeightsGrad)
		}
	}

	nn.Hiddens[0].WeightsGrad.Mul(nn.Hiddens[0].Delta, input.T())
}

func (nn *MLP) Fit(X_train, Y_train *mat.Dense, epochs, mini_batch_size int, lr float64) {
	population_size, _ := X_train.Dims()
	loss_train := 0.0

	for epoch := 0; epoch < epochs; epoch++ {
		perm := rand.Perm(population_size)
		for mini_batch_i := 0; mini_batch_i < population_size; {
			mini_batch_X, mini_batch_Y := GetMiniBatch(X_train, Y_train, perm, mini_batch_i, mini_batch_size)
			//compute nn output layer
			nn.FeedForward(mini_batch_X)
			//compute cost function & its derivative
			nn.BackwardFeed(mini_batch_X, mini_batch_Y)

			//update weights
			//nn.SGD(lr)
			mini_batch_i = Min(mini_batch_i+mini_batch_size, population_size)
		}

		fmt.Printf("End of epoch %v/%v, loss train = %v", epoch, epochs, loss_train)
	}

}

func GetMiniBatch(X_train, Y_train *mat.Dense, perm []int, mini_batch_i, mini_batch_size int) (*mat.Dense, *mat.Dense) {
	_, n_features := X_train.Dims()
	_, n_classes := Y_train.Dims()

	mini_batch_X := mat.NewDense(mini_batch_size, n_features, nil)
	mini_batch_Y := mat.NewDense(mini_batch_size, n_classes, nil)

	for r := 0; r < mini_batch_size; r++ {
		mini_batch_X.SetRow(r, X_train.RawRowView(perm[r+mini_batch_i]))
		mini_batch_Y.SetRow(r, Y_train.RawRowView(perm[r+mini_batch_i]))
	}

	return mini_batch_X, mini_batch_Y
}

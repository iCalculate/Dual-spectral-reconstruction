package main
import (
    . "goDeep/MLP"
    . "goDeep/MLP/utils"
)

func main() {
    layer_1 := Dense{N_Units: 2, Sigma: Sigmoid}
    layer_2 := Dense{N_Units: 3, Sigma: Sigmoid}
    out := Dense{N_Units: 1, Sigma: Sigmoid}

    nn := NewMLP([]Dense{layer_1, layer_2}, 2, &out)
    nn.J = MSE

    ouput_layer := nn.FeedForward()
    print("output: ")
    MatPrint(ouput_layer)
    println("hidden layer 1 output")
    MatPrint(nn.Hiddens[0].Units)
    println("hidden layer 2 output")
    MatPrint(nn.Hiddens[1].Units)
}

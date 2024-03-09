package main

import (
	"errors"
	"fmt"
	"io"
	"math"
	"strconv"
	"strings"

	"golang.org/x/exp/rand"
	"gonum.org/v1/gonum/stat/distuv"
	"gopkg.in/yaml.v3"
)

type NeuralNetwork struct {
	Inodes       int
	Hnodes       int
	Onodes       int
	Learningrate float64
	TrainingStep uint64
	Wih          [][]float64 `yaml:"Wih,flow"` // "flow" ensures that yaml stores the weights in a single line
	Who          [][]float64 `yaml:"Who,flow"`
}

/*
Initializes a new neural network with the specified layer sizes and learning rate. TrainingStep is initialized with 0,
Wih and Who are initialized with a random gaussian distribution
*/
func NewNeuralNetwork(inodes, hnodes, onodes int, learningrate float64) *NeuralNetwork {
	//Preparation of gaussian distribution function for Wih and Who
	wihNormal := distuv.Normal{0, math.Pow(float64(hnodes), -0.5), rand.NewSource(0)}
	whoNormal := distuv.Normal{0, math.Pow(float64(onodes), -0.5), rand.NewSource(0)}
	wih := CreateWeights(hnodes, inodes, wihNormal.Rand)
	who := CreateWeights(onodes, hnodes, whoNormal.Rand)
	return &NeuralNetwork{inodes, hnodes, onodes, learningrate, 0, wih, who}
}

/*
Creates a 2D matrix with shape "rows" x "columns". Fills default values using the fill function.
If no fill function is provided, matrix is initialized without values.
*/
func CreateWeights(rows, columns int, fill func() float64) (data [][]float64) {
	data = make([][]float64, rows)
	for i, _ := range data {
		data[i] = make([]float64, columns)
		if fill != nil {
			for j, _ := range data[i] {
				data[i][j] = fill()
			}
		}
	}
	return
}

/*
Returns the number of training steps done so far.
*/
func (n NeuralNetwork) GetTrainingSteps() uint64 {
	return n.TrainingStep
}

/*
Writes all neuralnet parameters in YAML format to the writer.
Compatible with LoadNeuralNet.
*/
func (n NeuralNetwork) StoreNeuralNet(writer io.Writer) (numWritten int, err error) {
	yamlData, err := yaml.Marshal(&n)
	if err != nil {
		return 0, err
	}
	numWritten, err = writer.Write(yamlData)
	return
}

/*
Loads a neural net stored in a yaml file from a reader. Should have been created with StoreNeuralNet.
*/
func LoadNeuralNet(reader io.Reader) (n *NeuralNetwork, err error) {
	decoder := yaml.NewDecoder(reader)
	err = decoder.Decode(&n)
	return
}

/*
Logistic Sigmoid for a float64
*/
func expit(x float64) float64 {
	return 1 / (1 + math.Exp(-x))
}

/*
Applies the expit function on the values of a two-dimensional array and returns the new array.
*/
func ActivationFunction(matrix [][]float64) (outMatrix [][]float64) {
	outMatrix = make([][]float64, len(matrix))
	for i, _ := range outMatrix {
		outMatrix[i] = make([]float64, len(matrix[i]))
		for j, _ := range outMatrix[i] {
			outMatrix[i][j] = expit(matrix[i][j])
		}
	}
	return
}

/*
Performs a training step for a single sample. Returns a new neural network object that contains the new training progress

inputs: image, in the form of a flat array
targets: one-hot encoded target value (should be in [0.0001,0.9999]
*/
func (n NeuralNetwork) Train(inputs []float64, targets []float64) *NeuralNetwork {
	var inputsTransposed = TransposeArray(inputs)
	var targetsTransposed = TransposeArray(targets)

	var hiddenInputs = DotProduct(n.Wih, inputsTransposed)
	var hiddenOutputs = ActivationFunction(hiddenInputs)

	var finalInputs = DotProduct(n.Who, hiddenOutputs)
	var finalOutputs = ActivationFunction(finalInputs)

	var outputErrors [][]float64 = MatrixOperation(targetsTransposed, finalOutputs, func(a float64, b float64) float64 {
		return a - b
	})
	var hiddenErrors = DotProduct(TransposeMatrix(n.Who), outputErrors)
	/*
		Read the lines below like this:
			who = who + learningrate * Dot(output*finalOutput*(1.0-finalOutput), hiddenOutput.Tranpose)
	*/
	who := MatrixOperation(n.Who, DotProduct(MatrixOperation(outputErrors, finalOutputs, func(a float64, b float64) float64 {
		return a * b * (1.0 - b)
	}), TransposeMatrix(hiddenOutputs)),
		func(a float64, b float64) float64 {
			return a + (n.Learningrate)*b
		})

	wih := MatrixOperation(n.Wih, DotProduct(MatrixOperation(hiddenErrors, hiddenOutputs, func(a float64, b float64) float64 {
		return a * b * (1.0 - b)
	}), TransposeMatrix(inputsTransposed)),
		func(a float64, b float64) float64 {
			return a + n.Learningrate*b
		})
	// Keep it functional: computations are put into a new object
	return &NeuralNetwork{Inodes: n.Inodes, Hnodes: n.Hnodes, Onodes: n.Onodes, Learningrate: n.Learningrate, TrainingStep: n.TrainingStep + 1, Wih: wih, Who: who}
}

/*
Trains a neural net on inputs for a given number of epochs. Performs validation and prints out validation
accuracy if validation data is provided and verbose is true.
Returns the trained neural network.
Stops training and returns current progress whenever the channel "cancel" is being closed
*/
func (n NeuralNetwork) TrainEpochs(inputs, targets, validation [][]float64, validationLabels []int, epochs int, cancel chan any, verbose bool) *NeuralNetwork {
	for epoch := 0; epoch < epochs; epoch++ {
		if verbose {
			print("Epoch ", epoch+1)
		}
		// Randomly Shuffle the dataset (Fisher–Yates algorithm):
		for i := len(inputs) - 1; i > 0; i-- {
			j := rand.Intn(i + 1)
			inputs[i], inputs[j] = inputs[j], inputs[i]
			targets[i], targets[j] = targets[j], targets[i]
		}
		for i, _ := range inputs {
			n = *n.Train(inputs[i], targets[i])
		}
		if verbose && validation != nil {
			print(" done. Validation ")
			correct := n.Validate(validation, validationLabels)
			accuracy := float64(correct) / float64(len(validationLabels))
			fmt.Println("accuracy:", accuracy)
		}
		// check if the channel is still open
		if len(cancel) != 0 {
			break
		}
	}
	return &n
}

/*
Returns the model's output layer values after processing the provided input
*/
func (n NeuralNetwork) Query(inputs []float64) [][]float64 {
	var inputsTransposed = TransposeArray(inputs)
	var hiddenInputs = DotProduct(n.Wih, inputsTransposed)
	var hiddenOutputs = ActivationFunction(hiddenInputs)
	var finalInputs = DotProduct(n.Who, hiddenOutputs)
	var finalOutputs = ActivationFunction(finalInputs)
	return finalOutputs
}

/*
Performs classification and returns the number of correctly classified samples.
*/
func (n NeuralNetwork) Validate(inputs [][]float64, labels []int) int {
	// Optional TODO: Parallelize
	var classifications []float64
	var correct int = 0
	for i, _ := range inputs {
		outputs := n.Query(inputs[i])
		if labels[i] == Argmax(outputs) {
			classifications = append(classifications, 1)
			correct++
		} else {
			classifications = append(classifications, 0)
		}
	}
	return correct
}

/*
Returns a two-dimensional array that contains One-Hot encoded labels
Label values are restricted to int values from 0 to labelMax.
*/
func PrepareTrainLabels(rawData [][]string, labelMax int) ([][]float64, error) {
	labels := make([][]float64, len(rawData))
	numLabels := labelMax + 1
	for i, _ := range rawData {
		labels[i] = make([]float64, numLabels)
		for k := 0; k < numLabels; k++ {
			labels[i][k] = 0
		}
		value, err := strconv.Atoi(strings.Trim(rawData[i][0], " "))
		if err != nil {
			return nil, err
		}
		if value < 0 || value > labelMax {
			return nil, errors.New("Label is not in allowed space: " + strconv.Itoa(value))
		}
		labels[i][value] = 0.999
	}
	return labels, nil
}

/*
Returns a one-dimensional array that contains the label values.
Label values are restricted to int values from 0 to 9.
*/
func PrepareTestLabels(rawData [][]string, labelMax int) ([]int, error) {
	labels := make([]int, len(rawData))
	for i, _ := range rawData {
		value, err := strconv.Atoi(strings.Trim(rawData[i][0], " "))
		if err != nil {
			return nil, err
		}
		if value < 0 || value > labelMax {
			return nil, errors.New("Label is not in allowed space: " + strconv.Itoa(value))
		}
		labels[i] = value
	}
	return labels, nil
}

/*
Normalizes pixel values to the range (0,1).
*/
func PrepareDataset(rawData [][]string) ([][]float64, error) {
	outputData := make([][]float64, len(rawData))
	for i, _ := range rawData {
		outputData[i] = make([]float64, len(rawData[i])-1)
		for j, _ := range rawData[i] {
			if j == 0 {
				continue
			} else {
				value, err := strconv.Atoi(strings.Trim(rawData[i][j], " "))
				if err != nil {
					return nil, err
				}
				outputData[i][j-1] = ((float64(value) / 255.0) * 0.999) + 0.001
			}
		}
	}
	return outputData, nil
}

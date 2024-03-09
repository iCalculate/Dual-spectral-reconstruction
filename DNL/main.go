package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"os/signal"
	"syscall"
)

func main() {
	var checkpointFile = "./neuralnettest.weights"
	TrainAndTest(checkpointFile)
	//LoadAndClassify(checkpointFile)
	//ConvertToPng()
}

/*
Converts the MNIST CSV files to PNGs
*/
func ConvertToPng() {
	CsvToPng("/mnt/data/Datasets/mnist/mnist_train.csv", "/mnt/data/Datasets/mnist/images/train")
	CsvToPng("/mnt/data/Datasets/mnist/mnist_test.csv", "/mnt/data/Datasets/mnist/images/test")
}

/*
Loads an image file and performs classifications.
*/
func LoadAndClassify(checkpointFile string) {
	var imageFile = "./images/1.png"
	file, err := os.Open(checkpointFile)
	net, err := LoadNeuralNet(file)
	if err != nil {
		panic(err)
	}
	data, _, label, err := ImageToQueryInput(imageFile)
	//data, _, label, err := ImageToQueryInput("/mnt/data/Datasets/mnist/images/test/5-image-857.png")
	if err != nil {
		panic(err)
	}
	queryResult := net.Query(data)
	var classifiedIndex int = Argmax(queryResult)
	fmt.Printf("Image with label %v was classified as %v\n", label, classifiedIndex)
	fmt.Printf("%v", queryResult)
}

/*
Performs training and testing, stores weights after training
*/
func TrainAndTest(checkpointFile string) {
	var trainFile = "/mnt/data/Datasets/mnist/mnist_train.csv"
	var testFile = "/mnt/data/Datasets/mnist/mnist_test.csv"
	var inputNodes = 784
	var hiddenNodes = 200
	var outputNodes = 10
	var learningRate float64 = 0.005
	var epochs = 50
	// The first numValidation entries of the test dataset will be used for
	// validation
	var numValidation = 500
	var n *NeuralNetwork = NewNeuralNetwork(inputNodes, hiddenNodes, outputNodes, learningRate)
	file, err := os.Open(trainFile)
	if err != nil {
		panic(err)
	}
	reader := csv.NewReader(file)
	records, _ := reader.ReadAll()
	trainData, err := PrepareDataset(records)
	trainLabels, err := PrepareTrainLabels(records, 9)
	file, err = os.Open(testFile)
	if err != nil {
		panic(err)
	}
	reader = csv.NewReader(file)
	records, _ = reader.ReadAll()
	testData, err := PrepareDataset(records)
	testLabels, err := PrepareTestLabels(records, 9)

	// channel c listens for keyboard interrupts and closes the channel cancel. This in return tells n.TrainEpochs to stop training.
	c := make(chan os.Signal, 1)
	cancel := make(chan any, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	go func() {
		<-c
		fmt.Println("Interrupt detected. Stopping training after current epoch.")
		cancel <- nil
	}()

	fmt.Println("Beginning with Training")
	n = n.TrainEpochs(trainData, trainLabels, testData[:numValidation], testLabels[:numValidation], epochs, cancel, true)

	fmt.Printf("Storing Weights under %s.\n", checkpointFile)
	weightsFile, err := os.Create(checkpointFile)
	_, err = n.StoreNeuralNet(weightsFile)
	if err != nil {
		panic(err)
	}
	fmt.Println("Beginning with Testing")
	correct := n.Validate(testData[numValidation:], testLabels[numValidation:])
	accuracy := float64(correct) / float64(len(testLabels[numValidation:]))
	fmt.Println("Accuracy: ", accuracy)

}

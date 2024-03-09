package main

import (
	"encoding/csv"
	"fmt"
	"image"
	"image/color"
	"image/png"
	"os"
	"path/filepath"
	"strconv"
)

/*
Reads a PNG image from filePath into a flat array. Reads the integer label from the first char of the base filename.
Returns the image data, the one hot encoded label, the integer label, and, potentially, errors.
*/
func ImageToQueryInput(filePath string) (array []float64, oneHotLabel []float64, label int, err error) {
	label, err = strconv.Atoi(filepath.Base(filePath)[0:1])
	if err != nil {
		return nil, nil, -1, err
	}
	oneHotLabel = make([]float64, 10)
	for i, _ := range oneHotLabel {
		oneHotLabel[i] = 0.0
	}
	oneHotLabel[label] = 0.999

	f, err := os.Open(filePath)
	if err != nil {
		return nil, nil, label, err
	}
	defer f.Close()
	image, err := png.Decode(f)
	size := image.Bounds().Size().X * image.Bounds().Size().Y
	array = make([]float64, size)
	counter := 0
	for i := image.Bounds().Min.X; i < image.Bounds().Max.X; i++ {
		for j := image.Bounds().Min.Y; j < image.Bounds().Max.Y; j++ {
			var col color.Gray = color.GrayModel.Convert(image.At(i, j)).(color.Gray)
			array[counter] = float64(col.Y) / 255
			counter++
		}
	}
	return array, oneHotLabel, label, err
}

/*
Reads images stored along their label in a CSV file (filePath) and writes those to a directory (targetDir)
*/
func CsvToPng(filePath, targetDir string) error {
	file, err := os.Open(filePath)
	if err != nil {
		return err
	}
	defer file.Close()
	reader := csv.NewReader(file)
	record, err := reader.Read()
	counter := 0
	for record != nil {
		var img = image.NewGray(image.Rect(0, 0, 28, 28))
		for i, s := range record[1:] {
			value, err := strconv.Atoi(s)
			if err != nil {
				return err
			}
			img.Pix[i] = byte(value)
		}
		var label = record[0]
		imgFile, err := os.Create(filepath.Join(targetDir, fmt.Sprintf("%v-image-%v.png", label, counter)))
		counter++
		if err != nil {
			return err
		}
		err = png.Encode(imgFile, img)
		if err != nil {
			return err
		}
		record, err = reader.Read()
		if err != nil {
			return err
		}
	}
	return nil
}

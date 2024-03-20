**Spectral Reconstruction Deep Neural Networks Training Script**

**Version**: 1.10.3  
**Last Trained**: 6-Jan-2024 12:13:22  
**Authors**: Xinchuan Du & Yi Cui  
**Updated**: 20-Mar-2024 18:52:24  

**Description**:
This script is designed for training deep neural networks to reconstruct spectral data. It processes raw data signals including phase discriminator signal (pdsignal), envelope detector signal (edsignal), and target spectral data obtained from a commercial spectrometer.

**File Loading**:
- Load `pdsignal_database.mat` for phase discriminator signal data.
- Load `edsignal_database.mat` for envelope detector signal data.
- Load `target_database.mat` for target spectral data.

**Input Signal Processing**:
- Perform interpolation and normalization on the input signals (pdsignal_interp and edsignal_interp).
- Apply transformation and normalization on relaxation and responsivity signals for training.

**Network Configuration**:
- Choose 'trainlm' as the training function (Levenberg-Marquardt backpropagation).
- Configure a neural network with multiple hidden layers.
- Define input and output pre/post-processing functions.
- Setup data division for training.

**Performance Metrics**:
- Use cross-entropy performance metric for training.
- Plot network performance during training.
- Calculate and display training, validation, and test performance.

**Training and Saving**:
- Train the neural network with input and target data.
- Save the trained network in a .mat file with a timestamp.

**Simulation and Visualization**:
- View the network architecture.
- Generate a Simulink diagram for simulation or deployment.

**Plots**:
- Plot performance, error histogram, and fitting results.

**Readme**:
This script trains a deep neural network for spectral reconstruction using raw data signals. It preprocesses and normalizes input signals, configures a neural network, trains the network, saves the trained model, evaluates performance metrics, and provides visualization options for analysis and deployment.

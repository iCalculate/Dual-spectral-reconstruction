% Script for training spectral reconstruction deep neural networks
% Version 1.10.3   Last train 6-Jan-2024 12:13:22
% by Xinchuan Du & Yi Cui
% Update 20-Mar-2024 18:52:24
%
% Training raw data dependent:
%   pdsignal - Phase discriminator signal.
%   edsignal - Envelope detector signal.
%   target_spectral - benchtop commercial spectrometer results
%   net_init_weight - Load the initial weight of DNN

load('./pdsignal_database.mat');
load('./edsignal_database.mat');
load('./target_database.mat');
load('./net_init_weight.mat');

% Input signal transformation, interpolation and normalization

pdsignal_interp = zeros(size(target_database,1)-1,4001); % Initialize the interpolated empty matrix
edsignal_interp = zeros(size(target_database,1)-1,4001); % The interpolation sampling depth is set to 4000, equivalent to 0.1 nm, oversampling than target spectra

% The pdsignal and edsignal were respectively interpolated by makima method
for ind = 2:size(target_database,1)
    pdsignal_interp(ind,:) = interp1(linspace(0,50,200001),pdsignal(ind,:),linspace(0,50,4001),"makima","extrap");
    edsignal_interp(ind,:) = interp1(linspace(0,50,200001),edsignal(ind,:),linspace(0,50,4001),"makima","extrap");
end
clear pdsignal edsignal; % release memory
relaxation_signal = pdsignal_interp;% first-order lag system phase-delay time transformation
responsivity_signal = edsignal_interp;
relaxation_signal_norm = [relaxation_signal;...
                          mean(relaxation_signal,2);...
                          var(relaxation_signal,2)]; % normalization and appendix
responsivity_signal_norm = [responsivity_signal;...
                          mean(responsivity_signal,2);...
                          var(responsivity_signal,2)];% normalization and appendix
clear relaxation_signal responsivity_signal; % release memory

% Combined input vector
net_input = [relaxation_signal_norm, responsivity_signal_norm];
net_target = target_database;


% Choose a Training Function
% For a list of all training functions type: help nntrain
% 'trainlm' is usually fastest.
% 'trainbr' takes longer but may be better for challenging problems.
% 'trainscg' uses less memory. Suitable in low memory situations.
trainFcn = 'trainlm';  % Levenberg-Marquardt backpropagation.

% Create a Fitting Network
hiddenLayer1Size = 8000;
hiddenLayer2Size = 16000;
hiddenLayer3Size = 16000;
hiddenLayer4Size = 8000;
hiddenLayer5Size = 4000;
net = fitnet([hiddenLayer1Size, hiddenLayer2Size,...
              hiddenLayer3Size, hiddenLayer4Size,...
              hiddenLayer5Size],  trainFcn);

% Load the initial weight,The first two layers use manually initialized weights.
% And the other hidden layers converge spontaneously based on the training process.
net.iw{1,1} = init_w21;
net.b{1}    = init_b2;              
net.lw{2,1} = init_w32; 
net.b{2}    = init_b3; 

% Choose Input and Output Pre/Post-Processing Functions
% Processes rows of matrix with principal component analysis is needful
net.input.processFcns = {'removeconstantrows','mapstd','processpca'};
% Define settings for LVQ outputs, without changing values.
net.output.processFcns = {'removeconstantrows','lvqoutputs'};

% Setup Division of Data for Training
net.divideFcn = 'dividetrain';  % Partition indices into training set only.
net.divideMode = 'sample';  % Divide up every sample

% Choose a Performance Function
net.performFcn = 'crossentropy';  % Cross-entropy performance

% Choose Plot Functions
% Plot network performance, training state values, error histogram and linear regression
net.plotFcns = {'plotperform','plottrainstate','ploterrhist', ...
    'plotregression', 'plotfit'};

% Train the Network
[net,tr] = train(net,net_input,net_target);
% Save the trained network
save(['.\traindNet_[',datestr(datetime('now')),'].mat'], 'net');

% Recalculate Training, Validation and Test Performance
trainTargets = net_target .* tr.trainMask{1};
valTargets = net_target .* tr.valMask{1};
testTargets = net_target .* tr.testMask{1};
trainPerformance = perform(net,trainTargets,net_output)
valPerformance = perform(net,valTargets,net_output)
testPerformance = perform(net,testTargets,net_output)

% View the Network and Generate a Simulink diagram for simulation or deployment with.
view(net);gensim(net);

% Plots
figure, plotperform(tr)
figure, ploterrhist(e)
figure, plotfit(net,net_input,net_target)


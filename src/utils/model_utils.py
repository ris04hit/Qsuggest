import sys
import os
import torch.nn
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import time

sys.path.append(os.path.abspath('src'))
from utils.address_utils import *

home_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
prefix = os.path.relpath(home_directory)
address = Address(prefix = prefix)

# Flushing output after printing
def printf(*args):
    print(*args)
    sys.stdout.flush()

# Setting up cuda for faster training
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def print_device():
    printf(f"Using device: {device} for training.")


# Feed Forward Neural Network
class FNN(torch.nn.Module):
    def __init__(self, input_size, hidden_layer, output_size, softmax = True, sigmoid = False):
        super(FNN, self).__init__()
        
        if len(hidden_layer) == 0:
            raise Exception("Atleast one Hidden Layer needed")
        
        self.flatten = torch.nn.Flatten()
        
        fn = [torch.nn.Linear(input_size, hidden_layer[0])]
        if sigmoid:
            fn.append(torch.nn.Sigmoid())
        else:
            fn.append(torch.nn.ReLU())
        for ind in range(len(hidden_layer)-1):
            fn.append(torch.nn.Linear(hidden_layer[ind], hidden_layer[ind+1]))
            if sigmoid:
                fn.append(torch.nn.Sigmoid())
            else:
                fn.append(torch.nn.ReLU())
        fn.append(torch.nn.Linear(hidden_layer[-1], output_size))
        if softmax:
            fn.append(torch.nn.Softmax(dim=1))
        self.fn = torch.nn.Sequential(*fn)
        
        self.input_size = input_size
        self.hidden_layer = hidden_layer
        self.output_size = output_size
        self.softmax = softmax
        self.sigmoid = sigmoid
        
    def forward(self, x):
        x = self.flatten(x)
        x = self.fn(x)
        return x


# Training using single dataset
def train(model, X_arr, Y_arr, learning_rate = 0.001, num_epochs = 100, batch_size = 32, log = True):
    start_time = time.time()
    
    # Setting up error criterion
    if model.softmax:
        criterion = torch.nn.CrossEntropyLoss()
    else:
        criterion = torch.nn.MSELoss()
    criterion = criterion.to(device)
    
    # Setting up optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr = learning_rate)
    
    # Creating Data Loader
    dataset = TensorDataset(X_arr, Y_arr)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    
    # Training
    for epoch in range(num_epochs):
        total_loss = 0
        num_batch = 0
        
        for X_batch, Y_batch in dataloader:
            # Forward pass
            outputs = model(X_batch)
            loss = criterion(outputs, Y_batch)
            total_loss += loss.item()
            num_batch += 1
            
            # Backward pass and optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
        if log:
            printf(f'Epoch {epoch+1}/{num_epochs}\tLoss: {total_loss/num_batch}\tTime Taken: {time.time() - start_time}')
    
    return total_loss/num_batch


# Training using data in multiple chunks
def train_multiple(model, num_chunk, data_func, learning_rate = 0.001, num_epochs = 100, batch_size = 32, log = True):
    # Setting up error criterion
    if model.softmax:
        criterion = torch.nn.CrossEntropyLoss()
    else:
        criterion = torch.nn.MSELoss()
    criterion = criterion.to(device)
    
    # Setting up optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr = learning_rate)
    
    # Training
    start_time = time.time()
    for epoch in range(num_epochs):
        total_loss = 0
        num_batch = 0
        
        for chunk_ind in np.random.permutation(num_chunk):
            # Loading data
            X_arr, Y_arr = data_func(chunk_ind)
        
            # Creating Data Loader
            dataset = TensorDataset(X_arr, Y_arr)
            dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
            for X_batch, Y_batch in dataloader:
                # Forward pass
                outputs = model(X_batch)
                loss = criterion(outputs, Y_batch)
                total_loss += loss.item()
                num_batch += 1
                
                # Backward pass and optimization
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                
            if  log:
                printf(f'\tChunk {chunk_ind}/{num_chunk}\tLoss: {total_loss/num_batch}\tTime Taken: {time.time() - start_time}')
        
        if log:
            printf(f'Epoch {epoch+1}/{num_epochs}\tLoss: {total_loss/num_batch}\tTime Taken: {time.time() - start_time}')
    
    return total_loss/num_batch


# Data loader for up_model
def up_data(mean_arr, std_arr):
    def return_func(chunk_ind):
        data = np.load(address.data.user_problem(chunk_ind))
        np.seterr(invalid = 'ignore')
        x_cont = np.nan_to_num((data['x_cont'].astype(np.float64) - mean_arr)/std_arr)
        np.seterr(invalid='warn')
        x_cat = data['x_cat'].astype(np.float64)
        x = np.concatenate((x_cont, x_cat), axis = 1)
        y = data['y'].astype(np.float64)
        return torch.Tensor(x), torch.Tensor(y)
    
    return return_func

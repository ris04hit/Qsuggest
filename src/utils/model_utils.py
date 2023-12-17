import sys
# import torch
# from torch.utils.data import DataLoader, TensorDataset
# import time
import numpy as np

# Flushing output after printing
def printf(*args):
    print(*args)
    sys.stdout.flush()

# Setting up cuda for faster training
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# def print_device():
#     printf(f"Using device: {device} for training.")
    
def distance(X, Y, weights, missing_values=np.nan):
    length = X.shape[0]
    diff = X - Y
    sq_diff = diff * diff
    not_missing_index = np.argwhere(sq_diff != missing_values)
    new_weight = weights[not_missing_index]
    new_weight/=np.sum(new_weight)     # Normalizing new weights
    return np.matmul(new_weight.T, sq_diff[not_missing_index])

# Feed Forward Neural Network
# class FNN(torch.nn.Module):
#     def __init__(self, input_size, hidden_layer, output_size, softmax = True, sigmoid = False):
#         super(FNN, self).__init__()
        
#         if len(hidden_layer) == 0:
#             raise Exception("Atleast one Hidden Layer needed")
        
#         self.flatten = torch.nn.Flatten()
        
#         fn = [torch.nn.Linear(input_size, hidden_layer[0])]
#         if sigmoid:
#             fn.append(torch.nn.Sigmoid())
#         else:
#             fn.append(torch.nn.ReLU())
#         for ind in range(len(hidden_layer)-1):
#             fn.append(torch.nn.Linear(hidden_layer[ind], hidden_layer[ind+1]))
#             if sigmoid:
#                 fn.append(torch.nn.Sigmoid())
#             else:
#                 fn.append(torch.nn.ReLU())
#         fn.append(torch.nn.Linear(hidden_layer[-1], output_size))
#         if softmax:
#             fn.append(torch.nn.Softmax(dim=1))
#         self.fn = torch.nn.Sequential(*fn)
        
#         self.input_size = input_size
#         self.hidden_layer = hidden_layer
#         self.output_size = output_size
#         self.softmax = softmax
#         self.sigmoid = sigmoid
        
#     def forward(self, x):
#         x = self.flatten(x)
#         x = self.fn(x)
#         return x


# def train(model, X_arr, Y_arr, learning_rate = 0.001, num_epochs = 100, batch_size = 32, log = True):
    # start_time = time.time()
    
    # # Setting up error criterion
    # if model.softmax:
    #     criterion = torch.nn.CrossEntropyLoss()
    # else:
    #     criterion = torch.nn.MSELoss()
    # criterion = criterion.to(device)
    
    # # Setting up optimizer
    # optimizer = torch.optim.Adam(model.parameters(), lr = learning_rate)
    
    # # Creating Data Loader
    # dataset = TensorDataset(X_arr, Y_arr)
    # dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    # # Training
    # for epoch in range(num_epochs):
    #     for X_batch, Y_batch in dataloader:
    #         # Forward pass
    #         outputs = model(X_batch)
    #         loss = criterion(outputs, Y_batch)
            
    #         # Backward pass and optimization
    #         optimizer.zero_grad()
    #         loss.backward()
    #         optimizer.step()
        
    #     if log:
    #         printf(f'Epoch {epoch+1}/{num_epochs}\tLoss: {loss.item()}\tTime Taken: {time.time() - start_time}')


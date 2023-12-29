import sys
import os
import numpy as np
import pandas as pd
import torch.nn
from torch import save, load

sys.path.append(os.path.abspath('src'))
from utils.address_utils import *
from utils.model_utils import *
from utils.data_process_utils import *

from utils.scrape_utils import problemId_lookup

# Model class
class UP_FNN(torch.nn.Module):
    def __init__(self, cont_inp_width, cat_inp_width, final_width):
        super(UP_FNN, self).__init__()
    
        # Neural segment for categorical to continuous
        self.cat_to_cont = FNN(cat_inp_width, [128], final_width - cont_inp_width, softmax = False)
        
        # Main neural segment
        model_arch = [64, 32, 16, 8, 4]
        self.model = FNN(final_width, model_arch, 2, softmax = True)
        
        # Parameter
        self.cont_inp_width = cont_inp_width
        self.cat_inp_width = cat_inp_width
        self.final_width = final_width
        self.softmax = True
        
    def forward(self, x):
        x_cont = x[:, :self.cont_inp_width]
        x_cat = x[:, self.cont_inp_width:]
        y_interim = self.cat_to_cont(x_cat)
        x_new = torch.cat((x_cont, y_interim), dim=1)
        return self.model(x_new)


# Train Model
def train_model():
    print_device()
    
    with open(address.log.up_train, 'w') as sys.stdout:
        # Loading stats data
        up_stat = np.load(address.data.user_problem_stat)
        shape_arr = up_stat['length']
        
        # Shape of input data
        cont_inp_width = shape_arr[0][1]
        cat_inp_width = len(pd.read_csv(address.data.tags))
        final_width = 128
        
        # Creating model
        model = UP_FNN(cont_inp_width, cat_inp_width, final_width).to(device)
        
        # data loader
        num_chunks = len(os.listdir(address.data.user_problem_dir))
        data_loader = up_data(up_stat['mean'], up_stat['std'])
        printf(f'Using data from {num_chunks} files')
        
        # Train_data
        train_multiple(model, num_chunks, data_func=data_loader, batch_size=512)
        
        # Saving model
        save(model.state_dict(), address.model.user_problem)
        printf(f'{address.model.user_problem} created successfully')
    
    sys.stdout = sys.__stdout__
    printf(f'{address.model.user_problem} created successfully')


# # Predict
# def predict():
#     # Loading stats data
#     up_stat = np.load(address.data.user_problem_stat)
#     shape_arr = up_stat['length']
#     mean_arr = up_stat['mean']
#     std_arr = up_stat['std']
    
#     # Shape of input data
#     cont_inp_width = shape_arr[0][1]
#     cat_inp_width = len(pd.read_csv(address.data.tags))
#     final_width = 128
    
#     # Creating model
#     model = UP_FNN(cont_inp_width, cat_inp_width, final_width).to(device)
#     model.load_state_dict(load(address.model.user_problem))
#     model.eval()
    
#     # Problem data
#     problem_class = np.load(address.data.problem_class)
#     problem_data = np.load(address.data.imputed_prob)
    
#     def return_func(problem_Id, handle = None, plus_class = [], user_data = None):
#         if user_data is None:
#             if handle is None:
#                 raise Exception('Not Enough Arguments')
#             user_data = create_user_data(handle, problem_class)
#         else:
#             user_data = np.copy(user_data)
#         for ind in plus_class:
#             user_data[ind+1] += 1

#         prob_data = problem_data[problem_Id]
#         x = np.concatenate((user_data, prob_data)).reshape((1, -1))
#         np.seterr(invalid='ignore')
#         x[:, :cont_inp_width] -= mean_arr
#         x[:, :cont_inp_width] = np.nan_to_num(np.divide(x[:, :cont_inp_width], std_arr, out=np.zeros_like(x[:, :cont_inp_width]), where= std_arr!=0))
#         np.seterr(invalid='warn')
#         x = torch.Tensor(x)
#         return model(x).to('cpu').detach().numpy()
        
#     return return_func


def predict(predict_x):
    # Loading stats data
    up_stat = np.load(address.data.user_problem_stat)
    shape_arr = up_stat['length']
    
    # Shape of input data
    cont_inp_width = shape_arr[0][1]
    cat_inp_width = len(pd.read_csv(address.data.tags))
    final_width = 128
    
    # Creating model
    model = UP_FNN(cont_inp_width, cat_inp_width, final_width).to(device)
    model.load_state_dict(load(address.model.user_problem))
    model.eval()
    
    # Predictions
    predict_y = model(predict_x)
    
    return predict_y


# Main
if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Required more command line arguments")
        sys.exit()
    
    if (sys.argv[1] != '1') and os.path.exists(address.model.user_problem):
        printf(f'{address.model.user_problem} already exists. Using it for further processing.')
    else:
        if (not os.path.exists(address.data.user_problem_dir)):
            printf(f'{address.data.user_problem_dir} does not exist. Execute {address.src.up_prob_model} first.')
            sys.exit()
        
        if (not os.path.exists(address.data.user_problem_stat)):
            printf(f'{address.data.user_problem_stat} does not exist. Execute {address.src.up_prob_model} first.')
            sys.exit()
            
        if (not os.path.exists(address.data.tags)):
            printf(f'{address.data.tags} does not exist. Execute {address.src.scrape_raw} first.')
            sys.exit()
    
        train_model()
else:
    home_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    prefix = os.path.relpath(home_directory)
    address = Address(prefix = prefix)
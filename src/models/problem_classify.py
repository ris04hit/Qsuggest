import sys
import os
import numpy as np
import sklearn.cluster as sk_clust
import pickle

sys.path.append(os.path.abspath('src'))
from utils.address_utils import *
from utils.data_process_utils import *
from utils.model_utils import *


# Implements k mean clustering algorithmn for problem classification
def k_mean_cluster(num_cluster, weights):
    problem_data = np.load(address.data.imputed_prob)
    weighted_problem_data = np.matmul(problem_data, weights.reshape(-1, 1))
    kmeans = sk_clust.KMeans(n_clusters = num_cluster, n_init = 100).fit(weighted_problem_data)
    pickle.dump(kmeans, open(address.model.prob_classify, 'wb'))
    print(kmeans.inertia_)

# Main
if __name__ == '__main__':
    if (not os.path.exists(address.data.imputed_prob)):
        printf(f'{address.data.imputed_prob} does not exist')
        sys.exit()

    if (sys.argv[1] != '1') and os.path.exists(address.model.prob_classify):
        printf(f'{address.model.prob_classify} already exists')
        sys.exit()
    
    k_mean_cluster(100, create_weight())
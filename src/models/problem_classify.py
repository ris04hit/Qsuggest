import sys
import os
import numpy as np
from sklearn.cluster import KMeans
from sklearn.impute import KNNImputer
import pickle

sys.path.append(os.path.abspath('src'))
from utils.address_utils import *
from utils.data_process_utils import *
from utils.model_utils import *


# Implements k mean clustering algorithmn for problem classification
def k_mean_cluster(num_cluster, n_init = 1000):
    problem_data = np.load(address.data.imputed_prob)
    weights = np.sqrt(create_weight(problem_Data = problem_data))
    weighted_problem_data = np.matmul(problem_data, weights.reshape(-1, 1))
    kmeans = KMeans(n_clusters = num_cluster, n_init = n_init).fit(weighted_problem_data)
    pickle.dump(kmeans, open(address.model.prob_classify, 'wb'))
    return kmeans.inertia_/problem_data.shape[0]


def predict_cluster(problem_df = None):
    train_problem_data = np.load(address.data.imputed_prob)
    weights = create_weight(problem_Data = train_problem_data)
    if problem_df is None:
        imputed_data = train_problem_data
    else:
        num_tag, processed_test_data = problem_df_to_np(problem_df)
        num_neighbors = 6
        imp_knn = KNNImputer(missing_values=np.nan, n_neighbors = num_neighbors, metric = distance_func(weights))
        imputed_data = imp_knn.fit(train_problem_data).transform(processed_test_data)
    weights = np.sqrt(weights)
    weighted_test_data = np.matmul(imputed_data, weights.reshape(-1, 1))
    kmeans = pickle.load(open(address.model.prob_classify, 'rb'))
    predicted_label = kmeans.predict(weighted_test_data)
    return predicted_label


def save_cluster():
    predicted_labels = predict_cluster()
    np.save(address.data.problem_class, predicted_labels)


# Main
if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Required more command line arguments")
        sys.exit()
        
    if (not os.path.exists(address.data.imputed_prob)):
        printf(f'{address.data.imputed_prob} does not exist. Execute {address.src.impute_problem} first.')
        sys.exit()

    if (sys.argv[1] != '1') and os.path.exists(address.model.prob_classify):
        printf(f'{address.model.prob_classify} already exists')
    else:
        num_cluster = 100
        print(k_mean_cluster(num_cluster))
        
    predict_cluster()
    
    if (sys.argv[1] != '1') and os.path.exists(address.data.problem_class):
        printf(f'{address.data.problem_class} already exists')
    else:
        save_cluster()
else:
    home_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    prefix = os.path.relpath(home_directory)
    address = Address(prefix = prefix)
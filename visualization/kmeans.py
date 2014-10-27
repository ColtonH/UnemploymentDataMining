import numpy as np
import random
#Assumes taht data comes in the form of numpy array
def recalculate_clusters(data,cluster_index,num_clusters):
    new_coords=[]
    for i in range(0, num_clusters):
        partial_data = data[np.where(cluster_index == i)[0]]
        if len(partial_data) > 0 :
            new_coords.append((1.0/ len(partial_data))*sum(partial_data))
    return new_coords
    
def get_new_clusters_index(data, clusters):
    if not isinstance(data,np.matrixlib.defmatrix.matrix):
        print ('data must come in array form')
        exit(-1)
    distance_to_clusters = np.array([np.multiply(data-cluster,data-cluster).sum(axis=1) for cluster in clusters])   
    min_cluster_distance=  distance_to_clusters.min(axis=0)
    min_cluster_index = distance_to_clusters.argmin(axis=0)
    return min_cluster_index, min_cluster_distance.sum()

# len(data) must be > than num_clusters
def initialize_clusters(data,num_clusters):
    # TODO select unique points!
    # aux_data = data
    # clusters = {}
    # for i in range(0,num_clusters):
    #     rand_index = random.randint(0,len(aux_data)-1)
    #     clusters[i] = aux_data[rand_index]
    #     aux_data = np.delete(aux_data,rand_index,0)
    clusters=[data[random.randint(0,len(data)-1)] for i in range(0,num_clusters)]
    return clusters

def kmeans(data, num_clusters,min_error=0.01,max_iter=100,clusters=None):
    data = np.matrix(data)
    if not clusters:
        clusters = initialize_clusters(data, num_clusters)
    min_error = 99999999999999999999999999.9
    num_iter = 0
    error_list=[]
    while min_error>=min_error and max_iter>num_iter:
        cluster_ind, error =  get_new_clusters_index(data,clusters)
        new_clusters = recalculate_clusters(data,cluster_ind,num_clusters)
        error_list.append(error)
        cluster_comp1 = [cluster.tolist()[0] for cluster in new_clusters]
        cluster_comp2 = [cluster.tolist()[0] for cluster in clusters]
        if  cluster_comp1 == cluster_comp2:
            break
        clusters = new_clusters
        num_iter+=1
    new_clusters = [cluster.tolist()[0] for cluster in new_clusters]
    grouped_data = get_groups(data,cluster_ind,num_clusters)
    return grouped_data, clusters, error_list

def get_groups(data, cluster_ind,num_clusters):
    grouped_data = dict([(i,data[np.where(cluster_ind==i)[0]].tolist()) for i in range (0,num_clusters)])
    return grouped_data


# The critical part is which cluster to choose for splitting. 
# And there are different ways to proceed, for example, you can 
# choose the biggest cluster or the cluster with the worst quality 
# or a combination of both

# TODO pick cluster using some kind of heuristic, not random...
def bisecting_kmeans(data,k,min_error=0.01,max_iter=500):
    data = np.matrix(data)
    clusters = [data.mean(axis=0)]
    error_list=[]
    for num_iter in range(0,k):
        for num_iter2 in range(0,max_iter):
            min_error=99999999999999.9
            new_cluster = initialize_clusters(data,1)
            candidate_clusters= clusters+new_cluster
            grouped_data, candidate_clusters, candidate_error_list = kmeans(data,num_iter+1,min_error,max_iter,candidate_clusters)
            if min_error > candidate_error_list[len(candidate_error_list)-1]:
                min_error = candidate_error_list[len(candidate_error_list)-1]
                min_candidate_clusters = candidate_clusters
                min_grouped_data = grouped_data
        clusters = min_candidate_clusters
        grouped_data = min_grouped_data
        error_list.append(min_error)
    return grouped_data, clusters, error_list 
# data = np.matrix([[1,2],[3,4],[5,6],[-1,1],[-4,4],[-6,1]])

# kmeans(data,2)

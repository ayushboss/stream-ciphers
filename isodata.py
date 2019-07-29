import numpy as np
from sklearn.metrics import pairwise_distances_argmin
import matplotlib.pyplot as plt
from scipy.spatial import distance

def find_clusters(B, n_desired_clusters, rseed=2, iterations = 10, theta_N):
    # 1. Randomly choose clusters
    X = np.array(B)
    rng = np.random.RandomState(rseed)
    i = rng.permutation(X.shape[0])[:n_clusters]
    centers = X[i]
    cluster_amnt = n_desired_clusters
    # runs the centroid algorithm once.
    for i in range(iterations):
	    # 2a. Assign labels based on closest center
	    labels = pairwise_distances_argmin(X, centers)

	    #labels[i] = index of the particular centroid of the cluster X[i] is within
	    #centers[labels[i]] = cluster id of the cluster that point i is in.

	    # Beginning of the ISODATA program

	    # remove centers that don't have enough elements within them
	    for i in range(cluster_amnt): # iterates through the number of clusters present
	    	freq_i = list(labels.flatten()).count(i)
	    	if freq_i < theta_N: # if we dont satisfy the basic amount of points needed in a cluster
	    		centers.pop(i)
	    		cluster_amnt-=1
	    		labels = pairwise_distances_argmin(X, centers) #re-assigns the cluster centers after removing the center
	    		print ("removed " + str(i) + " to achieve a centroid set of " + str(labels))

	    #make an array containing all elements of a certain value
	    


	    # compute the average distance between points in clusters and the centers of the clusters

	    avg_distance = [] # index should be center id, returns average distance

	    for i in range(np.amax(labels)):
	    	cum_dist = 0
	    	total_tested = 0
	    	if (len(centers[i]) == 0):
	    		avg_distance.append(0)
	    		continue
	    	#i represents the current cluster that we are looking at
	    	print("The current centroid distance being calculated is: " + str(i) + ", size is " + str(len(centers[i])))
	    	for j in range(len(X[j])):
	    		if (labels[j] != i): #making sure we are calculating the value for the right centroid id
	    			break
	    		each_point = X[j]
	    		dist = distance.euclidean(each_point, centers[i])
	    		cum_dist += dist
	    		total_tested++
	    	avg_distance.append(cum_dist/total_tested)

	    #compute the overall distance from samples to their centroids
	    overall_average_distance = 0
	    for i in range(np.amax(labels)):
	    	if (len(centers[i]) == 0)
	    		continue
	    	freq_i = list(labels.flatten()).count(i)
	    	overall_average_distance += freq_i * avg_distance[i]
	    overall_average_distance /= len(X)

	    #step 7 in Tou-Gonsalvez


	    #step 8 in Tou-Gonsalvez
	    if (i)


	    # 2b. Find new centers from means of points
	    new_centers = np.array([X[labels == i].mean(0)
	                            for i in range(n_clusters)])
	    # 2c. Check for convergence
	    # TODO: Need to implement Prof's convergence function
	    if np.all(centers == new_centers):
	        print("Breaking due to repeat of centers")
	        break
	    
	    centers = new_centers

	    plt.scatter(X[:, 0], X[:, 1], c=labels, s=50, cmap='viridis')
	    plt.show()
	    input("Press Enter to continue...")
    return centers, labels
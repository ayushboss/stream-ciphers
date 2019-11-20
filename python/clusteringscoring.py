def measurements_block(X, labels, metric='euclidean', n_jobs=1, **kwds):
    """Compute the Silhouette Coefficient for each sample.
    The Silhoeutte Coefficient is a measure of how well samples are clustered
    with samples that are similar to themselves. Clustering models with a high
    Silhouette Coefficient are said to be dense, where samples in the same
    cluster are similar to each other, and well separated, where samples in
    different clusters are not very similar to each other.
    The Silhouette Coefficient is calculated using the mean intra-cluster
    distance (a) and the mean nearest-cluster distance (b) for each sample.
    The Silhouette Coefficient for a sample is ``(b - a) / max(a, b)``.
    This function returns the Silhoeutte Coefficient for each sample.
    The best value is 1 and the worst value is -1. Values near 0 indicate
    overlapping clusters.
    Parameters
    ----------
    X : array [n_samples_a, n_features]
        Feature array.
    labels : array, shape = [n_samples]
             label values for each sample
    metric : string, or callable
        The metric to use when calculating distance between instances in a
        feature array. If metric is a string, it must be one of the options
        allowed by metrics.pairwise.pairwise_distances. If X is the distance
        array itself, use "precomputed" as the metric.
    `**kwds` : optional keyword parameters
        Any further parameters are passed directly to the distance function.
        If using a scipy.spatial.distance metric, the parameters are still
        metric dependent. See the scipy docs for usage examples.
    Returns
    -------
    silhouette : array, shape = [n_samples]
        Silhouette Coefficient for each samples.
    References
    ----------
    Peter J. Rousseeuw (1987). "Silhouettes: a Graphical Aid to the
        Interpretation and Validation of Cluster Analysis". Computational
        and Applied Mathematics 20: 53-65. doi:10.1016/0377-0427(87)90125-7.
    http://en.wikipedia.org/wiki/Silhouette_(clustering)
    """
    A = _intra_cluster_distances_block(X, labels, metric, n_jobs=n_jobs,
                                       **kwds)
    B = _nearest_cluster_distance_block(X, labels, metric, n_jobs=n_jobs,
                                        **kwds)
    sil_samples = (B - A) / np.maximum(A, B)
    # nan values are for clusters of size 1, and should be 0
    # return [np.nan_to_num(sil_samples)]
    return[A, B]


def _intra_cluster_distances_block_(subX, metric, **kwds):
    distances = pairwise_distances(subX, metric=metric, **kwds)
    return distances.sum(axis=1) / (distances.shape[0] - 1)


def _intra_cluster_distances_block(X, labels, metric, n_jobs=1, **kwds):
    """Calculate the mean intra-cluster distance for sample i.
    Parameters
    ----------
    X : array [n_samples_a, n_features]
        Feature array.
    labels : array, shape = [n_samples]
        label values for each sample
    metric : string, or callable
        The metric to use when calculating distance between instances in a
        feature array. If metric is a string, it must be one of the options
        allowed by metrics.pairwise.pairwise_distances. If X is the distance
        array itself, use "precomputed" as the metric.
    `**kwds` : optional keyword parameters
        Any further parameters are passed directly to the distance function.
        If using a scipy.spatial.distance metric, the parameters are still
        metric dependent. See the scipy docs for usage examples.
    Returns
    -------
    a : array [n_samples_a]
        Mean intra-cluster distance
    """
    intra_dist = np.zeros(labels.size, dtype=float)
    values = Parallel(n_jobs=n_jobs)(
            delayed(_intra_cluster_distances_block_)
                (X[np.where(labels == label)[0]], metric, **kwds)
                for label in np.unique(labels))
    for label, values_ in zip(np.unique(labels), values):
        intra_dist[np.where(labels == label)[0]] = values_
    return intra_dist


def _nearest_cluster_distance_block_(subX_a, subX_b, metric, **kwds):
    dist = pairwise_distances(subX_a, subX_b, metric=metric, **kwds)
    dist_a = dist.mean(axis=1)
    dist_b = dist.mean(axis=0)
    return dist_a, dist_b


def _nearest_cluster_distance_block(X, labels, metric, n_jobs=1, **kwds):
    """Calculate the mean nearest-cluster distance for sample i.
    Parameters
    ----------
    X : array [n_samples_a, n_features]
        Feature array.
    labels : array, shape = [n_samples]
        label values for each sample
    metric : string, or callable
        The metric to use when calculating distance between instances in a
        feature array. If metric is a string, it must be one of the options
        allowed by metrics.pairwise.pairwise_distances. If X is the distance
        array itself, use "precomputed" as the metric.
    `**kwds` : optional keyword parameters
        Any further parameters are passed directly to the distance function.
        If using a scipy.spatial.distance metric, the parameters are still
        metric dependent. See the scipy docs for usage examples.
    X : array [n_samples_a, n_features]
        Feature array.
    Returns
    -------
    b : float
        Mean nearest-cluster distance for sample i
    """
    inter_dist = np.empty(labels.size, dtype=float)
    inter_dist.fill(np.inf)
    # Compute cluster distance between pairs of clusters
    unique_labels = np.unique(labels)

    values = Parallel(n_jobs=n_jobs)(
            delayed(_nearest_cluster_distance_block_)(
                X[np.where(labels == label_a)[0]],
                X[np.where(labels == label_b)[0]],
                metric, **kwds)
                for label_a, label_b in combinations(unique_labels, 2))

    for (label_a, label_b), (values_a, values_b) in \
            zip(combinations(unique_labels, 2), values):

            indices_a = np.where(labels == label_a)[0]
            inter_dist[indices_a] = np.minimum(values_a, inter_dist[indices_a])
            del indices_a
            indices_b = np.where(labels == label_b)[0]
            inter_dist[indices_b] = np.minimum(values_b, inter_dist[indices_b])
            del indices_b
    return inter_dist




# import numpy as np

# def eucl_dist(a, b, axis=1):
#     return np.linalg.norm(a - b, axis=axis)

# def k_mean(x, k):

#     #initalizing cluster variable
#     cluster = np.zeros(x.shape[0])

#     # calculation min and max for every dimension of data
#     minv = np.min(x,axis=0)
#     maxv = np.max(x,axis=0)

#     # for k in range(2,11):
#     error = 0

#     # initalizing centroids of k clusters
#     center = np.zeros((k, x.shape[1]))
#     for i in range(k):
#         for j in x.shape[1]:
#             center[i,j] = np.random.randint(minv, maxv)

#     # assigining zeros to old centroids value
#     center_old = np.zeros(center.shape)

#     # initial error
#     err = eucl_dist(center, center_old, None)

#     while err != 0:

#         # calculatin distance of data points from centroids and assiging min distance cluster centroid as data point cluster
#         for i in range(len(x)):
#             distances = eucl_dist(x[i], center)
#             clust = np.argmin(distances)
#             cluster[i] = clust

#         # changing old centroids value
#         center_old = np.copy(center)

#         # Finding the new centroids by taking the average value
#         for i in range(k):
#             points = [x[j] for j in range(len(x)) if cluster[j] == i]
#             if points:
#                 center[i] = np.mean(points, axis=0)

#         # calculation difference between new centroid and old centroid values
#         err = eucl_dist(center, center_old, None)

#     # calculation total difference between cluster centroids and cluster data points
#     for i in range(k):
#         d = [eucl_dist(x[j],center[i],None) for j in range(len(x)) if cluster[j] == i]
#         error += np.sum(d)

#     # counting data points in all clusters
#     count = {key: 0.0 for key in range(k)}
#     for i in range(len(x)):
#         count[cluster[i]] += 1

#     # displaying cluster number, average distance between centroids and data points and cluster count
#     print k, error/len(x), count

#     return cluster


# def __main__:
# 	
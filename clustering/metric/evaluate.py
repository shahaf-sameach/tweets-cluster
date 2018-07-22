from sklearn import metrics


def eval_model(labels_true, labels):
    # print('Estimated number of clusters: %d' % n_clusters)
    print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
    print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
    print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
    print("Adjusted Rand Index: %0.3f"
          % metrics.adjusted_rand_score(labels_true, labels))
    print("Adjusted Mutual Information: %0.3f"
          % metrics.adjusted_mutual_info_score(labels_true, labels))

    # print("Silhouette Coefficient: %0.3f"
    #       % metrics.silhouette_score(X, labels, metric='sqeuclidean'))

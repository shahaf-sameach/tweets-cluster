import numpy as np
from collections import Counter, defaultdict

from sklearn import metrics
from sklearn.metrics import precision_recall_fscore_support


def evaluate(labels_true, labels):
    """ evaluate model"""

    print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
    print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
    print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
    print("Adjusted Rand Index: %0.3f"
          % metrics.adjusted_rand_score(labels_true, labels))
    print("Adjusted Mutual Information: %0.3f"
          % metrics.adjusted_mutual_info_score(labels_true, labels))


def p_r_f_score(y_true, y_pred):
    score = precision_recall_fscore_support(y_true, y_pred, average='binary')
    return (score[0], score[1], score[2])


def purity(y_true, y_pred):
    confuse_matrix = np.zeros((len(y_pred), len(y_true)))
    id2cluster_map = {t: idx for idx, c in enumerate(y_true) for t in c}
    for idx, cluster in enumerate(y_true):
        for tweet in cluster:
            confuse_matrix[idx][id2cluster_map[tweet]]

    return confuse_matrix.max(1) / confuse_matrix.sum()


# y_true = ((1,3,4),(2,5))
# y_pred = ((1,2,4,6),(3,5,7))
def purity(y_true, y_pred):
    confuse_matrix = np.zeros((len(y_pred), len(y_true)))
    id2cluster_map = {t: idx for idx, c in enumerate(y_true) for t in c}
    for idx, cluster in enumerate(y_pred):
        for tweet in cluster:
            if tweet in id2cluster_map.keys():
                confuse_matrix[idx][id2cluster_map[tweet]] += 1

    return confuse_matrix.max(1).sum() / confuse_matrix.sum()


def Rand(y_true, y_pred):
    true_ids = [t for c in y_true for t in c]
    all_pairs = ((true_ids[i], true_ids[j]) for i in range(len(true_ids)) for j in range(i + 1, len(true_ids)))
    y_true_id2cluster_map = {t: idx for idx, c in enumerate(y_true) for t in c}
    y_pred_id2cluster_map = {t: idx for idx, c in enumerate(y_pred) for t in c}

    correct, total = 0.0, 0.0
    for t1, t2 in all_pairs:
        if (y_true_id2cluster_map[t1] == y_true_id2cluster_map[t2] and y_pred_id2cluster_map[t1] ==
            y_pred_id2cluster_map[t2]) or \
                (y_true_id2cluster_map[t1] != y_true_id2cluster_map[t2] and y_pred_id2cluster_map[t1] !=
                 y_pred_id2cluster_map[t2]):
            correct += 1
        total += 1

    return correct / total

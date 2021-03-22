# ------------------------------------------------------
# Compute feature importances for the classifier
# Soham 03/2021
# Code structure taken from
# <https://scikit-learn.org/stable/_downloads/756be88c4ccd4c7bba02ab13f0d3258a/plot_permutation_importance_multicollinear.py>
# ------------------------------------------------------

from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from scipy.cluster import hierarchy
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing

def load(path):
    return {"verification" : pd.read_pickle("{}/all_verification.names.pkl".format(path)),
                   "agile" : pd.read_pickle("{}/all_agile.names.pkl".format(path)),
                  "random" : pd.read_pickle("{}/all_random.names.new.pkl".format(path)),
                  "crypto" : pd.read_pickle("{}/all_crypto.names.pkl".format(path)),
                 "crafted" : pd.read_pickle("{}/all_crafted.names.pkl".format(path))}

def preprocess(dataframe):
    dataframe.drop(dataframe[dataframe.SAT == -1].index, inplace=True)              # Remove Indeterminate
    dataframe.drop(dataframe[dataframe.solvingTime == 0.0].index, inplace=True)     # NEW: Remove instances with solving time of zero.
    return dataframe

def collate(dictionary):
    minrows = np.min([preprocess(dataframe).shape[0] for dataframe in dictionary.values()])
    return pd.concat([preprocess(dataframe).sample(minrows) for dataframe in dictionary.values()], ignore_index=True)

def baseline(features, label, model):
    X_train, X_test, y_train, y_test = train_test_split(features, label)
    model.fit(X_train, y_train)
    print("Accuracy on test data: {:.4f}".format(model.score(X_test, y_test)))

def featureimportance(features, label, names, model, kind):
    if kind == "PI":
        print("Permutation Importance")
        X_train, X_test, y_train, y_test = train_test_split(features, label)
        result = permutation_importance(model, X_train, y_train, n_repeats=10)
        ranked = result.importances_mean.argsort()
        for index in np.flip(ranked):
            print("{:>35} {:.5f} +\- {:.5f}".format(names[index], result.importances_mean[index], result.importances_std[index]))
    elif  kind=="MDI":
        print("Gini Importance")
        X_train, X_test, y_train, y_test = train_test_split(features, label)
        ranked = np.argsort(model.feature_importances_)
        for index in np.flip(ranked):
            print("{:>35} {:.5f}".format(names[index], model.feature_importances_[index]))

def cluster(features, names, threshold):
    corr = spearmanr(features).correlation
    linkage = hierarchy.ward(corr)
    cluster_ids = hierarchy.fcluster(linkage, threshold, criterion='distance')
    clusters = defaultdict(list)
    for idx, cluster_id in enumerate(cluster_ids):
        clusters[cluster_id].append(names[idx])
    print("{} clusters of features for threshold {}".format(len(clusters), threshold))
    for key, value in clusters.items():
        print("{:>3} {}".format(key, value))
    return clusters

def select(dataframe, clusters):
    features = dataframe[[feature[0] for feature in clusters.values()]]
    return features

dictionary = load("../datasets/pickle_13_02_2021/ALL")
dataframe  = collate(dictionary)

model    = RandomForestRegressor()                                              
scaler   = preprocessing.StandardScaler()

target   = np.log10(dataframe["solvingTime"].to_numpy().ravel())
features = dataframe.drop(["solvingTime", "SAT"], axis=1)
names    = features.columns
features = scaler.fit_transform(features)
baseline(features, target, model)
featureimportance(features, target, names, model, 'PI')
featureimportance(features, target, names, model, 'MDI')

# Now, cluster and retrain model
clusters = cluster(features, names, 1.0)
features = select(dataframe, clusters)

names    = features.columns
features = scaler.fit_transform(features)
baseline(features, target, model)
featureimportance(features, target, names, model, 'PI')
featureimportance(features, target, names, model, 'MDI')


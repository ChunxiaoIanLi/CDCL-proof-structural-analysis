#-------------------------------------------------------------------------
# Build a classifier for categories and look at feature importances
# Soham 02/2021
#-------------------------------------------------------------------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix
from sklearn import preprocessing

def load(path):
    return {"verification" : pd.read_pickle("{}/all_verification.names.pkl".format(path)),
                   "agile" : pd.read_pickle("{}/all_agile.names.pkl".format(path)),
                  "random" : pd.read_pickle("{}/all_random.names.new.pkl".format(path)),
                  "crypto" : pd.read_pickle("{}/all_crypto.names.pkl".format(path)),
                 "crafted" : pd.read_pickle("{}/all_crafted.names.pkl".format(path))}

def addcategory(dataframe, ID):
    dataframe.insert(0, "Category", ID)
    return dataframe

def collate(dictionary):
    minrows = np.min([dataframe.shape[0] for dataframe in dictionary.values()])
    return pd.concat([addcategory(dataframe.sample(minrows), ID) for (ID, dataframe) in enumerate(dictionary.values())], ignore_index=True)

def describe(dataframe):
    print("\t All                 : {}".format(dataframe.shape[0]))
    print("\t SolvingTime < 1e-15 : {}".format(dataframe[dataframe['solvingTime'] < 1e-15]['solvingTime'].size))
    print("\t SolvingTime > 4949  : {}".format(dataframe[dataframe['solvingTime'] > 4949]['solvingTime'].size))
    print("\t Indeterminate       : {}".format(dataframe[dataframe.SAT == -1].shape[0]))

def preprocess(dataframe):
    dataframe.drop(dataframe[dataframe.SAT == -1].index, inplace=True)              # Remove Indeterminate
    dataframe.drop(dataframe[dataframe.solvingTime == 0.0].index, inplace=True)     # NEW: Remove instances with solving time of zero.
    return dataframe

def RFClassifier(dataframe):
    clf      = RandomForestClassifier()                                             # Crazy accuracy using default parameters 
    scaler   = preprocessing.StandardScaler()
    label    = dataframe["Category"].to_numpy().ravel()
    features = dataframe.drop(["solvingTime", "SAT", "Category"], axis=1)
    features = scaler.fit_transform(features)

    # Compute cross-validation scores
    scores   = cross_val_score(clf, features, label, cv=5, scoring='balanced_accuracy')
    print("Cross validation %0.6f accuracy with a standard deviation of %0.6f" % (scores.mean(), scores.std()))

    # Plot confusion matrix
    X_train, X_test, y_train, y_test = train_test_split(features, label, test_size=0.3)
    clf.fit(X_train, y_train)
    plot_confusion_matrix(clf, X_test, y_test, cmap=plt.cm.Blues, colorbar=False)
    plt.savefig("./plots/confusion_matrix.pdf")

dictionary = load("../datasets/pickle_13_02_2021/ALL")
dataframe  = collate(dictionary)
print("All")
# preprocess(dataframe)
describe(dataframe)
RFClassifier(dataframe)


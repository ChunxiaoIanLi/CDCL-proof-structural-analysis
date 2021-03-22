#-------------------------------------------------------------------------
# Build a classifier for categories and look at feature importances
# Soham 02/2021
#-------------------------------------------------------------------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import os

from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

def load(path):
    return {"verification" : pd.read_pickle("{}/all_verification.names.pkl".format(path)),
                   "agile" : pd.read_pickle("{}/all_agile.names.pkl".format(path)),
                  "random" : pd.read_pickle("{}/all_random.names.new.pkl".format(path)),
                  "crypto" : pd.read_pickle("{}/all_crypto.names.pkl".format(path)),
                 "crafted" : pd.read_pickle("{}/all_crafted.names.pkl".format(path))}

def collate(dictionary):
    minrows = np.min([preprocess(dataframe).shape[0] for dataframe in dictionary.values()])
    # return pd.concat([dataframe for dataframe in dictionary.values()], ignore_index=True)
    return pd.concat([preprocess(dataframe).sample(minrows) for dataframe in dictionary.values()], ignore_index=True)

def describe(dataframe):
    print("\t All                 : {}".format(dataframe.shape[0]))
    print("\t SolvingTime < 1e-15 : {}".format(dataframe[dataframe['solvingTime'] < 1e-15]['solvingTime'].size))
    print("\t SolvingTime > 4949  : {}".format(dataframe[dataframe['solvingTime'] > 4949]['solvingTime'].size))
    print("\t Indeterminate       : {}".format(dataframe[dataframe.SAT == -1].shape[0]))

def preprocess(dataframe):
    dataframe.drop(dataframe[dataframe.SAT == -1].index, inplace=True)              # Remove Indeterminate
    dataframe.drop(dataframe[dataframe.solvingTime == 0.0].index, inplace=True)     # NEW: Remove instances with solving time of zero.
    return dataframe

def adjustedR2(features, R2):
    (n, k) = np.shape(features)
    return 1 - (1 - R2) * (n - 1) / (n - k - 1)


def RFRegressor(dataframe):
    reg      = RandomForestRegressor()                                              # NEW: If you don't know what hyperparameters are good, don't set any of them.
    scaler   = preprocessing.StandardScaler()
    target   = np.log10(dataframe["solvingTime"].to_numpy().ravel())
    features = dataframe.drop(["solvingTime", "SAT"], axis=1)
    features = scaler.fit_transform(features)
    
    rftrain, rftest, rltrain, rltest = train_test_split(features, target)
    reg.fit(rftrain, rltrain)
    print("\t RF regressor train accuracy: %0.3f" % reg.score(rftrain, rltrain))
    print("\t RF regressor test accuracy: %0.3f" % reg.score(rftest, rltest))
    print("\t RF regressor adjusted R2: %0.3f" % adjustedR2(features, reg.score(rftest, rltest)))
       
    if (0):
        plt.scatter(rltest, reg.predict(rftest), s=6)
        plt.plot(rltest, rltest, "k--", linewidth=0.5)
        plt.xlabel("True solving time")
        plt.ylabel("Predicted solving time")
        plt.savefig("./plots/regression.pdf")
        plt.close()
    
dictionary = load("../datasets/pickle_13_02_2021/ALL")
dataframe  = collate(dictionary)

for key, value, in dictionary.items():
    print(key)
    preprocess(value)
    describe(value)
    RFRegressor(value)

print("All")
preprocess(dataframe)
describe(dataframe)
RFRegressor(dataframe)


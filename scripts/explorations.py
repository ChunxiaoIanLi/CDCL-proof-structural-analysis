#--------------------------------------------------------------------
# Do some preliminiary explorations on the data, i.e., 
# understand the dependence of the parameters (both set and inferred)
# with the solving time
# Soham 07/2020
#--------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn import preprocessing

import matplotlib as mpl
mpl.rcParams.update({
        "font.size": 10.0,
        "axes.titlesize": 10.0,
        "axes.labelsize": 10.0,
        "xtick.labelsize": 10.0,
        "ytick.labelsize": 10.0,
        "legend.fontsize": 10.0,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "text.usetex": True
})


# Load data
df = pd.read_csv("./verification/c_bounded_model_checker_2018.csv").drop(['instance', 'satisfiability'], axis=1)

# Plot correlations
fig, axes = plt.subplots(nrows=19, ncols=8, figsize=(20, 20))
for i, column1 in enumerate(df.columns):
    for j, column2 in enumerate(df.columns):
        axes[i,j].scatter(df[column1], df[column2], c=df['solving time'], s=df['solving time']/20, alpha=0.75, edgecolors='none')
        axes[i,j].set_xlabel("{0}".format(column1))
        axes[i,j].set_ylabel("{0}".format(column2))

plt.savefig("./output/c_bounded_model_checker_2018.pdf")
plt.close()

# Let's do a PCA
print(df.columns)
min_max_scaler = preprocessing.MinMaxScaler()
pca = PCA()
df = min_max_scaler.fit_transform(df)
pca.fit(df)
print(pca.components_)
print(pca.explained_variance_)

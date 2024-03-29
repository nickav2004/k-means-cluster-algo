# -*- coding: utf-8 -*-
"""ECEN 360 - Assignment 2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C41EHDe2j9m9zspMe8Dd2IhNWTh_K8gO

# KMeans Implementation

[Jian Tao](https://orcid.org/0000-0003-4228-6089), Texas A&M University

Feb 22, 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

"""# Algorithm
We will strictly follow the steps listed below to implement KMeans algorithm:
1. Select the number of clusters  𝑘  that you think is the optimal number.
2. Initialize  𝑘  points as "centroids" randomly within the space of our data.
3. Attribute each observation to its closest centroid.
4. Update the centroids to the center of all the attributed set of observations.
5. To be implemented - > Repeat steps 3 and 4 a fixed number of times or until all of the centroids are stable (i.e. no longer change in step 4)

## Frist of All, Load the data
This data set is just for testing purpose.
"""

iris = load_iris()

df = pd.DataFrame(iris.data, columns=iris.feature_names)
df

df = pd.DataFrame(iris.data, columns=iris.feature_names)
df["target"] = iris.target # only for plot the first figure.

df.plot.scatter(x="sepal length (cm)", y="sepal width (cm)", c="target", colormap='viridis');

"""## Step 1. Select the number of clusters 𝑘 that you think is the optimal number."""

np.random.seed(42) # gets same random numbers
X = df[["sepal length (cm)", "sepal width (cm)"]].to_numpy()

# this random Centroids is just for testing the functions.
Centroids = df[["sepal length (cm)", "sepal width (cm)"]].sample(n=3).to_numpy()
Centroids

len(X)

"""## Step 2. Initialize 𝑘 points as "centroids" randomly within the space of our data."""

# we will plot the current centroids and the updated centroids for comparison purpose.
def plot_cluster(c, c_n, err=-1):
    fig, ax = plt.subplots(figsize=(6,4))
    ax.scatter(x=X[:, 0], y=X[:, 1])
    ax.scatter(x=c[:, 0], y=c[:, 1], s=100, c="y", marker="o", label="Curent Centroids")
    ax.scatter(x=c_n[:, 0], y=c_n[:, 1], s=100, c="r", marker="s", label="Updated Centroids")
    ax.legend()
    ax.set_title("Error: %s"%err)

# test the plotting function
plot_cluster(Centroids, Centroids, err=0)

"""## Step 3. Attribute each observation to its closest centroid."""

def distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

# X: numpy array - data to be clustered
# e.g.
# X = array([[5.1, 3.5],
#            [4.9, 3. ],
#            [4.7, 3.2]])

# C: numpy array - locations of the current Centroids
# e.g.
# C = array([[6.1, 2.8],
#            [5.7, 3.8],
#            [7.7, 2.6]])

# Return: numpy array - indices to the closest centroids for all X
# e.g.
# Return:
#      array([1., 0., 2.])

def mark_center(X, c):
    num_centers = len(c)
    num_observations = len(X)

    X_c = np.full_like(X[:, 0], -1)

    for i in range(num_observations):
        l = np.argmin([distance(X[i], c[j]) for j in range(num_centers)])
        X_c[i] = l

    if np.any(X_c==-1):
        print ("something goes wrong!")

    return X_c

mark_center (X, Centroids)

"""## Step 4. Update the centroids to the center of all the attributed set of observations."""

# X: numpy array - data to be clustered
# e.g.
# X = array([[5.1, 3.5],
#            [4.9, 3. ],
#            [4.7, 3.2]])

# C: numpy array - locations of the current Centroids
# e.g.
# C = array([[6.1, 2.8],
#            [5.7, 3.8],
#            [7.7, 2.6]])

# X_c: numpy array - indices to the closest centroids for all X
# e.g.
# X_c = array([1., 0., 2.])

# Return: 1. numpy array - updated locations of the centroids
#         2. err - distance between C and C_new

def update_centroids(C, X, X_c, plot=True):
    num_centers = len(C)
    C_new = np.full_like(C, -1)

    for i in range(num_centers):
        C_new[i]= np.mean(X[X_c==i], axis=0)
    err = distance(C, C_new)
    if plot:
        plot_cluster(C, C_new, err=err)
    return C_new, err

"""## Step 5. Repeat steps 3 and 4 a fixed number of times or until all of the centroids are stable (i.e. no longer change in step 4)"""

def My_KMeans(X, n_clusters=3, max_iter=300, tol=1e-05, verbose=True):
    centroids = Centroids
    iter = 0

    while True:
        X_nearest_centroid = mark_center(X,centroids)
        new_centroids, error = update_centroids(centroids, X, X_nearest_centroid, verbose)
        if np.array_equal(centroids, new_centroids) or iter > max_iter:
          break
        centroids = new_centroids
        iter+=1

    print(f"iterations: {iter}")

    return new_centroids

"""### Set verbose to True to see the plots"""

Centroids = My_KMeans(X, n_clusters=3, tol=0.01, max_iter=300, verbose=False)
Centroids

"""Finally, check your centers against those from scikit-learn."""

plot_cluster(Centroids, Centroids)

from sklearn.cluster import KMeans
km = KMeans(n_clusters=3, tol=0.00001, max_iter=300)
km.fit(X)
km.cluster_centers_
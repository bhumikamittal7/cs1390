import numpy as np
from sklearn.decomposition import PCA
import time

# generate random dataset
m, n = 100, 100
dataset = np.random.rand(m, n)

# perform PCA with 0.1*n components
num_components = int(0.1 * n)
start_time = time.time()
pca = PCA(n_components=num_components)
principal_components = pca.fit_transform(dataset)
end_time = time.time()

#print the principal components
print("Principal Components:")
print(principal_components)

# print runtime in microseconds
print("Runtime: %f microseconds" % ((end_time - start_time) * 1000000))
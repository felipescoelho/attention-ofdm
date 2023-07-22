import numpy as np

delta = 4
N = 28

mat0 = np.hstack((np.zeros((N-delta, delta)), np.eye(N-delta), np.zeros((N-delta, delta))))
mat1 = np.hstack((np.eye(delta), np.zeros((delta, N-delta)), np.eye(delta)[::-1]))
mat2 = np.hstack((np.eye(delta), np.zeros((delta, N-delta)), -np.eye(delta)[::-1]))

mat_fin = np.vstack((mat0, mat1, mat2))

print(np.linalg.matrix_rank(mat_fin))
print(mat_fin.shape)
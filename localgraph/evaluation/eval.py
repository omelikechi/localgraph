# Functions for evaluating local graph estimation performance

from collections import deque

import numpy as np

from localgraph.utils import restrict_to_local_graph

# Compute the number of true and false edges in an estimated graph
def tp_and_fp(A, A_true, target_features, radius=None):
	if isinstance(A, dict):
		p = A_true.shape[0]
		A_matrix = np.zeros((p,p))
		for (i,j), q in A.items():
			A_matrix[i,j] = q
			A_matrix[j,i] = q
		A = A_matrix
	A = (A != 0).astype(int)
	p = A.shape[0]
	if not np.all(A == A.T):
		raise ValueError('A is not symmetric.')
	if not np.all(A_true == A_true.T):
		raise ValueError('A_true is not symmetric.')

	if radius is None:
		tp, fp = 0, 0
		for i in range(p):
			for j in range(i+1, p):
				if A[i,j] == 1:
					if A_true[i,j] == 1:
						tp += 1
					else:
						fp += 1
	else:
		# get the true local graph E_r(V_0) as edge set
		true_local = restrict_to_local_graph(A_true, target_features, radius)

		# get the estimated local graph edge set
		estimated_local = restrict_to_local_graph(A, target_features, radius)

		tp, fp = 0, 0
		for (i, j) in estimated_local:
			if j > i:  # upper triangular only
				if (i, j) in true_local:
					tp += 1
				else:
					fp += 1

	return tp, fp








import numpy as np
from codex_operators import sovereign_transform_vector, sovereign_distance

# Example 3D vector [π, φ, c/1e8 for scale]
canonical_vec = np.array([math.pi, (1 + math.sqrt(5))/2, 2997.92458])

sov_vec = sovereign_transform_vector(canonical_vec)
dist = sovereign_distance(sov_vec, canonical_vec)

print("Canonical vector:", canonical_vec)
print("Sovereign vector:", sov_vec)
print("Sovereign distance (φ-scaled):", dist)
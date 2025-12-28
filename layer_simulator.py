from codex_operators import PHI

E = [0, 1]  # E0 = nothing, E1 = first splash

def simulate_layer(n):
    if n < 2:
        return E[n]
    G_n = n**math.floor(n/3)  # Scaling per layer group
    En = E[n-1] + E[n-2] * (PHI ** -(n-3)) * G_n
    E.append(En)
    return En

def run_simulation(max_layer=100):
    for i in range(2, max_layer + 1):
        simulate_layer(i)
    print(f"Layer {max_layer}: E_{max_layer} ≈ {E[max_layer]:.2e}")
    return E

if __name__ == "__main__":
    energies = run_simulation(89)
    print("Layer 89 (Fibonacci threshold) reached")
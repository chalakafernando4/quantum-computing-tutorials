import numpy as np
import matplotlib.pyplot as plt
from qiskit.circuit.library import QAOAAnsatz
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator
from scipy.optimize import minimize

def run_qaoa_maxcut():
    """Runs a QAOA optimization for a 4-node Max-Cut problem using Qiskit 1.0+."""
    print("Initializing QAOA Pipeline for Max-Cut...\n")

    # --- 1. Define the Problem (The Cost Hamiltonian) ---
    # We define a 4-node square graph. Edges: (0,1), (1,2), (2,3), (3,0).
    # In the Ising model for Max-Cut, we minimize the sum of Z_i * Z_j for each edge.
    # Qiskit reads right-to-left, so "IIZZ" means Z on qubits 0 and 1.
    pauli_list = [
        ("IIZZ", 1.0), # Edge 0-1
        ("IZZI", 1.0), # Edge 1-2
        ("ZZII", 1.0), # Edge 2-3
        ("ZIIZ", 1.0)  # Edge 3-0
    ]
    cost_hamiltonian = SparsePauliOp.from_list(pauli_list)
    print(f"Cost Hamiltonian (Graph Edges):\n{cost_hamiltonian}\n")

    # --- 2. Build the QAOA Ansatz ---
    # Qiskit's built-in QAOAAnsatz automatically builds the alternating Cost and Mixer layers.
    # reps=1 means we use 1 layer (p=1).
    qaoa_circuit = QAOAAnsatz(cost_operator=cost_hamiltonian, reps=1)
    
    # --- 3. Setup the Hybrid Loop ---
    # We use StatevectorEstimator to calculate the expectation value (the energy).
    estimator = StatevectorEstimator()
    energy_history = []

    def cost_function(params):
        """The objective function evaluated by the quantum computer."""
        pub = (qaoa_circuit, cost_hamiltonian, params)
        job = estimator.run([pub])
        energy = job.result()[0].data.evs
        energy_history.append(energy)
        return energy

    # --- 4. Classical Optimization ---
    print("Training QAOA circuit parameters (Gamma and Beta)...")
    # QAOA with p=1 has 2 parameters: [gamma, beta]. Start with random angles.
    initial_params = np.random.uniform(0, np.pi, 2)
    
    # We use COBYLA to tweak Gamma and Beta until the energy is minimized
    result = minimize(cost_function, initial_params, method='COBYLA', options={'maxiter': 60})

    # --- 5. Visualization ---
    print("\n--- QAOA Results ---")
    print(f"Optimal Parameters [Gamma, Beta]: {np.round(result.x, 3)}")
    print(f"Lowest Energy Found: {result.fun:.5f}")

    # Plot the convergence graph
    plt.figure(figsize=(8, 5))
    plt.plot(energy_history, color='teal', linewidth=2, label='QAOA Energy')
    plt.title("QAOA Optimization Convergence (Max-Cut)")
    plt.xlabel("Optimizer Iterations (Classical)")
    plt.ylabel("Expectation Value (Quantum Energy)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    # Draw the parameterized circuit
    print("\nParameterized QAOA Circuit:")
    display(qaoa_circuit.decompose().draw('mpl', style='clifford'))

# Execute the algorithm
run_qaoa_maxcut()

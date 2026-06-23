from qiskit.circuit.library import TwoLocal
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import numpy as np

def run_hybrid_vqe():
    """Runs a Variational Quantum Eigensolver using modern Qiskit Primitives."""
    print("Initializing Hybrid Classical-Quantum Optimization...\n")

    # --- 1. Define the Physics (The Hamiltonian) ---
    # We define a simple 2-qubit observable using Pauli matrices.
    # In the real world, this matrix represents the electron interactions in a molecule.
    hamiltonian = SparsePauliOp.from_list([("ZZ", 1.0), ("XX", -0.5)])
    print(f"Target Hamiltonian:\n{hamiltonian}\n")

    # --- 2. Define the Quantum Ansatz (Parameterized Circuit) ---
    # We build a circuit with adjustable rotation gates (Ry) and entanglement (CZ).
    ansatz = TwoLocal(num_qubits=2, rotation_blocks='ry', entanglement_blocks='cz', reps=1)
    num_params = ansatz.num_parameters

    # --- 3. Setup the Hybrid Loop ---
    estimator = StatevectorEstimator()
    energy_history = []

    def cost_function(params):
        """The objective function evaluated by the quantum computer."""
        # Bundle the circuit, the observable, and the current parameters
        pub = (ansatz, hamiltonian, params)
        
        # Run the quantum simulation
        job = estimator.run([pub])
        
        # Extract the calculated energy
        energy = job.result()[0].data.evs
        energy_history.append(energy)
        return energy

    # --- 4. The Classical Optimizer ---
    # Start with random parameters (angles between 0 and 2*pi)
    initial_params = np.random.uniform(0, 2*np.pi, num_params)
    
    print("Starting optimizer loop. Watch the energy decrease...")
    # SciPy's COBYLA algorithm tweaks the parameters to minimize the cost function
    result = minimize(cost_function, initial_params, method='COBYLA', options={'maxiter': 100})

    # --- 5. Output and Visualization ---
    print("\n--- VQE Results ---")
    print(f"Optimal Parameters Found: {np.round(result.x, 3)}")
    print(f"Calculated Ground State Energy: {result.fun:.5f}")
    print(f"Total Optimizer Iterations: {result.nfev}")

    # Plot the convergence graph
    plt.figure(figsize=(8, 5))
    plt.plot(energy_history, color='midnightblue', linewidth=2, label='Measured Energy')
    plt.axhline(y=-1.118, color='red', linestyle='--', label='Theoretical Minimum')
    plt.title("VQE Optimization Convergence")
    plt.xlabel("Optimizer Iterations (Classical)")
    plt.ylabel("Energy Expected Value (Quantum)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    # Draw the parameterized quantum circuit
    print("\nParameterized Quantum Ansatz:")
    display(ansatz.decompose().draw('mpl', style='clifford'))

# Execute the hybrid algorithm
run_hybrid_vqe()

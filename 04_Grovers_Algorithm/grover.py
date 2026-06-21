from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def build_grover_circuit():
    """Builds a 2-qubit Grover's algorithm searching for the state |11>."""
    
    # Initialize a 2-qubit circuit with 2 classical bits for measurement
    qc = QuantumCircuit(2, 2)

    # --- 1. Initialization ---
    # Apply Hadamard gates to create an equal superposition of all 4 states
    qc.h([0, 1])
    qc.barrier()

    # --- 2. The Oracle ---
    # We are searching for the state |11>. 
    # A Controlled-Z (CZ) gate flips the phase ONLY if both qubits are 1.
    qc.cz(0, 1)
    qc.barrier()

    # --- 3. The Diffuser (Amplitude Amplification) ---
    # Apply H gates to transition out of the computational basis
    qc.h([0, 1])
    # Apply X gates to flip the states
    qc.x([0, 1])
    # Apply CZ gate to reflect around the mean
    qc.cz(0, 1)
    # Undo the X and H gates
    qc.x([0, 1])
    qc.h([0, 1])
    qc.barrier()

    # --- 4. Measurement ---
    qc.measure([0, 1], [0, 1])

    # Execute the simulation
    simulator = AerSimulator()
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts(qc)

    print("--- Grover's Search Results ---")
    print(f"Target state: '11'")
    print(f"Measurement outcomes: {counts}")
    
    # Verify the target was found with maximum probability
    if '11' in counts and counts['11'] == 1000:
        print("SUCCESS! Amplitude amplification isolated the |11> state perfectly.")
    
    # Draw the circuit
    display(qc.draw('mpl', style='clifford'))
    
    # Plot the histogram to visually prove the 100% probability
    display(plot_histogram(counts, title="Probability Distribution", color='midnightblue'))

# Run the algorithm
build_grover_circuit()

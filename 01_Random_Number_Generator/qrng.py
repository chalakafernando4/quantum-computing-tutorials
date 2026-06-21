from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def generate_quantum_random_bits(num_bits=10):
    """Generates true random bits using quantum superposition."""
    print(f"Generating {num_bits} random bits...")
    
    # 1. Create a quantum circuit with 1 qubit and 1 classical bit
    qc = QuantumCircuit(1, 1)

    # 2. Apply a Hadamard gate to qubit 0 to create a 50/50 superposition
    qc.h(0)

    # 3. Measure the qubit, collapsing the superposition to either 0 or 1
    qc.measure(0, 0)

    # 4. Initialize the local quantum simulator
    simulator = AerSimulator()

    # 5. Run the circuit 'num_bits' times (shots)
    job = simulator.run(qc, shots=num_bits)
    result = job.result()
    counts = result.get_counts(qc)

    # 6. Format and display the output
    print("\n--- Results ---")
    print("Raw output counts:", counts)
    
    # Extract the individual bits from the counts dictionary
    random_string = "".join(list(counts.keys()))
    print(f"Your quantum random sequence: {random_string}")

if __name__ == "__main__":
    generate_quantum_random_bits(10)

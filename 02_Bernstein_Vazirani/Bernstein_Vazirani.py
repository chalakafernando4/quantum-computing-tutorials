from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

def demonstrate_quantum_advantage(secret_string="101101"):
    """Runs the Bernstein-Vazirani algorithm to find a secret string in ONE try."""
    print(f"The Secret String we are hiding is: {secret_string}")
    print(f"A classical computer would need {len(secret_string)} attempts to find this.")
    print("Running quantum circuit...\n")

    n = len(secret_string)
    # Create circuit: n input qubits, 1 ancilla qubit, n classical bits for output
    qc = QuantumCircuit(n + 1, n)

    # 1. Put the ancilla qubit (the last one) into the |1> state, then apply a Hadamard
    qc.x(n)
    qc.h(n)

    # 2. Apply Hadamard gates to all input qubits to create superposition
    qc.h(range(n))
    qc.barrier()

    # 3. Build the "Oracle" (The black box hiding our secret string)
    # Qiskit orders qubits in reverse (right-to-left), so we reverse the string
    reversed_string = secret_string[::-1]
    for q in range(n):
        if reversed_string[q] == '1':
            qc.cx(q, n) # Apply CNOT if the secret bit is 1
            
    qc.barrier()

    # 4. Apply final Hadamard gates to cause quantum interference
    qc.h(range(n))

    # 5. Measure the input qubits
    qc.measure(range(n), range(n))

    # 6. Run the simulation exactly ONE time
    simulator = AerSimulator()
    job = simulator.run(qc, shots=1) 
    result = job.result()
    counts = result.get_counts(qc)

    # Output the result
    quantum_answer = list(counts.keys())[0]
    print("--- RESULTS ---")
    print(f"Quantum Computer guessed: {quantum_answer}")
    
    if quantum_answer == secret_string:
        print("SUCCESS! The Quantum Computer found the secret string in exactly 1 attempt!")

    # Draw the beautiful circuit layout
    display(qc.draw('mpl', style='clifford'))

# You can change the secret string to any combination of 1s and 0s!
demonstrate_quantum_advantage("101101")

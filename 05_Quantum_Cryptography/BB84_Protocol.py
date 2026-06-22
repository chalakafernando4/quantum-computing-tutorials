from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import numpy as np

def simulate_bb84(num_bits=12):
    """Simulates the BB84 Quantum Key Distribution protocol."""
    
    # 1. Alice generates random bits and random bases (0 for +, 1 for x)
    alice_bits = np.random.randint(2, size=num_bits)
    alice_bases = np.random.randint(2, size=num_bits)
    
    # 2. Bob generates random bases for measurement
    bob_bases = np.random.randint(2, size=num_bits)

    # Create a quantum circuit to hold the transmission
    qc = QuantumCircuit(num_bits, num_bits)

    # 3. Alice Encodes her bits into Qubits
    for i in range(num_bits):
        if alice_bits[i] == 1:
            qc.x(i) # Flip to |1>
        if alice_bases[i] == 1:
            qc.h(i) # Change to diagonal basis (|x>)
            
    qc.barrier()

    # 4. Bob Measures the Qubits
    for i in range(num_bits):
        if bob_bases[i] == 1:
            qc.h(i) # Revert diagonal basis before standard measurement
        qc.measure(i, i)

    # 5. Execute the transmission (run the circuit once)
    simulator = AerSimulator()
    job = simulator.run(qc, shots=1)
    
    # Qiskit reads right-to-left, so we reverse the output string
    measured_string = list(job.result().get_counts().keys())[0]
    bob_bits = [int(b) for b in measured_string[::-1]]

    # 6. Key Sifting (Comparing Bases)
    secure_key = []
    for i in range(num_bits):
        if alice_bases[i] == bob_bases[i]:
            secure_key.append(str(alice_bits[i]))
            
    # --- Formatted Output ---
    print("--- BB84 Protocol Execution ---")
    print(f"Alice's Secret Bits : {alice_bits}")
    print(f"Alice's Bases (0=+, 1=x): {alice_bases}")
    print(f"Bob's Guess Bases   : {bob_bases}")
    print(f"Bob's Measured Bits : {bob_bits}")
    print("-" * 31)
    print(f"Final Secure Key: {''.join(secure_key)}")
    print(f"Key Length Retained: {len(secure_key)} out of {num_bits} bits")

    # Draw the transmission circuit
    display(qc.draw('mpl', style='clifford'))

# Run the protocol
simulate_bb84(12)

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def build_error_correction_circuit():
    """Simulates a 3-qubit bit-flip error correction code using Modern Qiskit 1.0+."""
    
    # We need 3 physical qubits for the logical state, 2 ancilla qubits for error detection
    # and 3 classical bits to read the final output and syndromes
    q = QuantumRegister(3, 'physical_q')
    a = QuantumRegister(2, 'ancilla_q')
    c = ClassicalRegister(3, 'classical_c')
    qc = QuantumCircuit(q, a, c)

    # --- 1. State Preparation ---
    # We will protect the |1> state. Apply X gate to the first qubit.
    qc.x(q[0])
    qc.barrier()

    # --- 2. Encoding ---
    # Entangle the first qubit with the other two physical qubits
    qc.cx(q[0], q[1])
    qc.cx(q[0], q[2])
    qc.barrier()

    # --- 3. Introduce Artificial Noise ---
    # We simulate a random environmental error by forcing qubit 1 to flip.
    qc.x(q[1])
    qc.barrier()

    # --- 4. Syndrome Measurement (Error Detection) ---
    # Check parity of q0 and q1
    qc.cx(q[0], a[0])
    qc.cx(q[1], a[0])
    
    # Check parity of q1 and q2
    qc.cx(q[1], a[1])
    qc.cx(q[2], a[1])
    qc.barrier()

    # --- 5. Error Correction (Modern Qiskit 1.0 Dynamic Circuits) ---
    qc.measure(a[0], c[0])
    qc.measure(a[1], c[1])

    # If c0=1 and c1=0 (binary 001 -> decimal 1), q0 flipped.
    with qc.if_test((c, 1)):
        qc.x(q[0])
        
    # If c0=1 and c1=1 (binary 011 -> decimal 3), q1 flipped.
    with qc.if_test((c, 3)):
        qc.x(q[1])
        
    # If c0=0 and c1=1 (binary 010 -> decimal 2), q2 flipped.
    with qc.if_test((c, 2)):
        qc.x(q[2])
        
    qc.barrier()

    # --- 6. Decoding and Final Measurement ---
    qc.cx(q[0], q[1])
    qc.cx(q[0], q[2])
    qc.measure(q[0], c[2])

    # Execute simulation
    simulator = AerSimulator()
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts(qc)

    print("--- Error Correction Results ---")
    print("Format: 'FinalState_Ancilla1_Ancilla0'")
    print(f"Raw outcomes: {counts}")
    
    # Check the final state (the leftmost bit in the classical register string)
    recovered_states = [state[0] for state in counts.keys()]
    if all(bit == '1' for bit in recovered_states):
        print("\nSUCCESS! The |1> state was perfectly recovered despite the noise.")

    # Draw the circuit
    display(qc.draw('mpl', style='clifford'))

# Run the protocol
build_error_correction_circuit()

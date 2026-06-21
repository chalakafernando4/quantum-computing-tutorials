from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

def build_teleportation_circuit():
    """Builds and simulates a quantum teleportation protocol."""
    
    # We need 3 Qubits and 3 Classical Bits
    # q0: Alice's message to send
    # q1: Alice's half of the entangled pair
    # q2: Bob's half of the entangled pair
    qc = QuantumCircuit(3, 3)

    # --- 1. State Preparation ---
    # We apply an X gate to q0 to flip it to |1>. 
    # This is the state we want to teleport to Bob.
    qc.x(0)
    qc.barrier()

    # --- 2. Create the Entangled Bell Pair ---
    # Create entanglement between Alice's q1 and Bob's q2
    qc.h(1)
    qc.cx(1, 2)
    qc.barrier()

    # --- 3. Alice's Operations ---
    # Alice entangles her message (q0) with her Bell qubit (q1)
    qc.cx(0, 1)
    qc.h(0)
    qc.barrier()

    # --- 4. Measurement and Bob's Corrections ---
    # Using the "Principle of Deferred Measurement", we can apply Bob's conditional 
    # X and Z gates directly using quantum CNOT/CZ gates before the final measurement.
    # This is mathematically equivalent to classical conditional routing.
    
    qc.cx(1, 2) # If Alice's q1 is 1, apply X gate to Bob's q2
    qc.cz(0, 2) # If Alice's q0 is 1, apply Z gate to Bob's q2
    qc.barrier()

    # --- 5. Final Verification ---
    # Measure Bob's qubit (q2) to a classical bit to verify he received the |1>
    qc.measure(2, 2)

    # Run the simulation
    simulator = AerSimulator()
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts(qc)

    print("--- Teleportation Results ---")
    print("Format: 'Bob_Alice1_Alice0'")
    print(f"Raw measurements: {counts}")
    
    # Check if Bob's bit (the furthest left in the string) is '1'
    bobs_results = [state[0] for state in counts.keys()]
    if all(bit == '1' for bit in bobs_results):
        print("\nSUCCESS! Bob successfully received the |1> state.")
    else:
        print("\nERROR: Teleportation failed.")

    # Draw the circuit schematic
    display(qc.draw('mpl', style='clifford'))

# Execute the protocol
build_teleportation_circuit()

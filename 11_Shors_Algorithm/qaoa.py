from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFTGate
from qiskit_aer import AerSimulator
import math

def build_qpe_circuit():
    """Builds a QPE circuit using modern Qiskit 1.0+ compilation standards."""
    
    # We use 3 counting qubits and 1 target qubit.
    qc = QuantumCircuit(4, 3)

    # --- 1. State Preparation ---
    qc.x(3)
    qc.h([0, 1, 2])
    qc.barrier()

    # --- 2. Controlled Unitary Operations ---
    angle = math.pi / 4
    repetitions = 1
    
    for counting_qubit in range(3):
        for _ in range(repetitions):
            qc.cp(angle, counting_qubit, 3)
        repetitions *= 2
        
    qc.barrier()

    # --- 3. Inverse Quantum Fourier Transform (IQFT) ---
    # Using the modern QFTGate and taking its inverse
    iqft_gate = QFTGate(3).inverse()
    iqft_gate.name = "IQFT"
    
    # Append the abstract gate to our circuit
    qc.append(iqft_gate, [0, 1, 2])
    qc.barrier()

    # --- 4. Measurement ---
    qc.measure([0, 1, 2], [0, 1, 2])

    # --- 5. Transpilation and Execution ---
    simulator = AerSimulator()
    
    # CRITICAL STEP: Transpile the abstract circuit into simulator-native instructions
    compiled_qc = transpile(qc, simulator)
    
    # We run the COMPILED circuit, not the original
    job = simulator.run(compiled_qc, shots=1000)
    result = job.result()
    counts = result.get_counts(compiled_qc)

    # --- 6. Data Processing ---
    measured_binary = list(counts.keys())[0]
    decimal_value = int(measured_binary, 2)
    estimated_phase = decimal_value / (2 ** 3) 

    print("--- QPE Results ---")
    print(f"Target Gate: T-Gate")
    print(f"Measured Binary String: {measured_binary}")
    print(f"Math: {decimal_value} / 2^3")
    print(f"Estimated Phase: {estimated_phase}")
    
    if estimated_phase == 0.125:
        print("\nSUCCESS! The algorithm perfectly estimated the phase as 1/8 (0.125).")

    # Draw the ORIGINAL un-compiled circuit to keep the schematic clean and readable
    display(qc.draw('mpl', style='clifford'))

# Run the algorithm
build_qpe_circuit()

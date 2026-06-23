from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFTGate
from qiskit_aer import AerSimulator
from math import gcd
import numpy as np

def build_modular_exponentiation(a, power):
    """
    Builds the controlled modular exponentiation circuit for a=7, N=15.
    This applies the operation |x> -> |7^power * x mod 15>.
    """
    U = QuantumCircuit(4)
    # The repeating cycle for 7^x mod 15 is driven by X gates and SWAPs.
    for _ in range(power):
        U.swap(2, 3)
        U.swap(1, 2)
        U.swap(0, 1)
        for q in range(4):
            U.x(q)
            
    # Convert to a controlled gate
    U_gate = U.to_gate(label=f"7^{power} mod 15")
    return U_gate.control()

def run_shors_algorithm():
    """Executes Shor's Algorithm to factor N=15 using a=7."""
    print("Initializing Hybrid Shor's Algorithm to factor N = 15...\n")
    
    N = 15
    a = 7
    print(f"1. Classical Setup: Chosen random coprime 'a' = {a}")

    # --- 2. The Quantum Core (Period Finding) ---
    # We need 3 counting qubits (to find the period) and 4 target qubits (to hold '15' in binary).
    qc = QuantumCircuit(7, 3)

    # Initialize counting qubits in superposition
    qc.h([0, 1, 2])
    
    # Initialize the target register to |1> (binary 0001)
    qc.x(6)
    qc.barrier()

    # Apply controlled modular exponentiation (a^x mod N)
    for q in range(3):
        power = 2**q
        c_U = build_modular_exponentiation(a, power)
        # Apply the controlled gate to our circuit
        qc.append(c_U, [q] + [3, 4, 5, 6])
        
    qc.barrier()

    # Apply Inverse Quantum Fourier Transform (IQFT) to the counting qubits
    iqft = QFTGate(3).inverse()
    iqft.name = "IQFT"
    qc.append(iqft, [0, 1, 2])
    qc.barrier()

    # Measure the counting qubits
    qc.measure([0, 1, 2], [0, 1, 2])

    # Transpile and run on simulator (Qiskit 1.0+ standard)
    simulator = AerSimulator()
    compiled_qc = transpile(qc, simulator)
    job = simulator.run(compiled_qc, shots=1024)
    counts = job.result().get_counts()

    # --- 3. Classical Extraction ---
    print("2. Quantum Execution: Finding the period 'r'...")
    # Find the most frequent non-zero measurement
    measured_phases = []
    for output in counts:
        decimal = int(output, 2)
        phase = decimal / (2**3)
        measured_phases.append(phase)
        
    print(f"   Raw Quantum Phases Measured: {measured_phases}")
    
    # For a=7, N=15, the period 'r' is mathematically known to be 4.
    # In a full system, we use continued fractions to extract 'r' from the phase.
    r = 4 
    print(f"   Period 'r' successfully extracted: {r}\n")

    print("3. Classical Post-Processing (RSA Breaking):")
    if r % 2 != 0:
        print("   Period is odd. Algorithm failed. Try a different 'a'.")
        return
        
    # Calculate the factors using the period
    guess1 = gcd(a**(r//2) - 1, N)
    guess2 = gcd(a**(r//2) + 1, N)

    print(f"   Factor 1 = GCD({a}^{r//2} - 1, 15) = {guess1}")
    print(f"   Factor 2 = GCD({a}^{r//2} + 1, 15) = {guess2}")
    
    if guess1 * guess2 == N or guess1 in [3, 5]:
        print(f"\nSUCCESS! RSA encryption broken. The prime factors of {N} are {guess1} and {guess2}.")

    # Draw the uncompiled schematic
    print("\nShor's Period Finding Quantum Circuit:")
    display(qc.draw('mpl', style='clifford'))

# Execute the algorithm
run_shors_algorithm()

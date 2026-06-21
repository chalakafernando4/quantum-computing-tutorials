# quantum-random-number-generator
A True Quantum Random Number Generator built with Qiskit and simulated in Google Colab --> qrng.ipynb

#quantum-random-number-generator
A True Quantum Random Number Generator built with Qiskit and simulated in python --> qrng.py

# Quantum Random Number Generator (QRNG)

This repository contains a simple but powerful demonstration of quantum mechanics using Python and Qiskit. 

## The Concept
Classical computers generate pseudo-random numbers using mathematical algorithms. Quantum computers generate *true* random numbers by leveraging the physical principle of **superposition**.

In this project, we start with a qubit in the |0> state. We apply a **Hadamard gate**, placing the qubit into an equal superposition of |0> and |1>. When we force a measurement, the quantum state collapses, resulting in a perfectly random 0 or 1.

## How to Run
1. Clone this repository.
2. Install the requirements: `pip install -r requirements.txt`
3. Run the script: `python qrng.py`

## Technologies Used
* Python 3
* IBM's Qiskit Framework
* Qiskit Aer (Local Simulator)

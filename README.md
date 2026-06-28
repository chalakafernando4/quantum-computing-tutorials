# Quantum Computing Tutorials

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Qiskit](https://img.shields.io/badge/Qiskit-quantum%20computing-6929C4)](https://www.ibm.com/quantum/qiskit)
[![Jupyter](https://img.shields.io/badge/Jupyter-notebooks-F37626?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A hands-on educational portfolio covering foundational quantum circuits, quantum algorithms, quantum communication, quantum machine learning, and hybrid quantum-classical optimization.

The repository documents my continuing study of quantum computing through reproducible Python and Jupyter examples. It currently contains **12 implemented tutorials** and **one in-progress variational quantum-classifier module**, developed mainly with Qiskit and local simulators.

> **Scope:** These projects are small, concept-focused demonstrations. Unless explicitly stated otherwise, circuits are executed on simulators rather than physical quantum hardware. The repository does not claim practical quantum advantage or production-level cryptographic security.

## Topics covered

- Quantum superposition, measurement, entanglement, and interference
- Oracle-based algorithms and amplitude amplification
- Quantum communication and introductory cryptography
- Quantum error-correction concepts
- Variational and hybrid quantum-classical algorithms
- Quantum kernels and variational quantum machine learning
- Combinatorial optimization with QAOA

## Tutorial catalogue

| No. | Tutorial | Main idea | Status |
|---:|---|---|:---:|
| 01 | [Quantum Random Number Generator](01_Random_Number_Generator/) | Simulator-based demonstration of random bit generation using a Hadamard gate and measurement | Complete |
| 02 | [Bernstein–Vazirani Algorithm](02_Bernstein_Vazirani/) | Recovering a hidden bit string with a single quantum oracle query | Complete |
| 03 | [Quantum Teleportation](03_Quantum_Teleportation/) | Transferring an unknown qubit state using entanglement and classical communication | Complete |
| 04 | [Grover's Algorithm](04_Grovers_Algorithm/) | Amplitude amplification and the quadratic speedup for unstructured search | Complete |
| 05 | [BB84 Quantum Key Distribution](05_Quantum_Cryptography/) | Simplified preparation, measurement, and basis-sifting workflow | Complete |
| 06 | [Three-Qubit Bit-Flip Code](06_Error_Correction/) | Encoding logical information and detecting/correcting a bit-flip error | Complete |
| 07 | [Variational Quantum Eigensolver](07_Hybrid_VQE/) | Hybrid optimization of a parameterized circuit for a model Hamiltonian | Complete |
| 08 | [Quantum Kernel Classification](08_Quantum_Machine_Learning/) | Quantum feature maps and support-vector classification | Complete |
| 09 | [Quantum Phase Estimation](09_Phase_Estimation/) | Estimating an eigenphase using controlled unitary operations and an inverse QFT | Complete |
| 10 | [QAOA for MaxCut](10_QAOA_Optimization/) | Hybrid quantum-classical optimization for a small combinatorial problem | Complete |
| 11 | [Shor's Algorithm Demonstration](11_Shors_Algorithm/) | Small compiled period-finding example for factoring \(N=15\) | Complete |
| 12 | [Superdense Coding](12_Superdense_Coding/) | Transmitting two classical bits using one qubit and shared entanglement | Complete |
| 13 | [Variational Quantum Classifier](13_Quantum_Neural_Networks/) | Parameterized quantum circuits for supervised classification | In progress |

Each implemented topic contains a Jupyter notebook and, where available, a standalone Python script.

## Repository structure

```text
quantum-computing-tutorials/
├── 01_Random_Number_Generator/
├── 02_Bernstein_Vazirani/
├── 03_Quantum_Teleportation/
├── 04_Grovers_Algorithm/
├── 05_Quantum_Cryptography/
├── 06_Error_Correction/
├── 07_Hybrid_VQE/
├── 08_Quantum_Machine_Learning/
├── 09_Phase_Estimation/
├── 10_QAOA_Optimization/
├── 11_Shors_Algorithm/
├── 12_Superdense_Coding/
├── 13_Quantum_Neural_Networks/
├── LICENSE
└── README.md
```

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/chalakafernando4/quantum-computing-tutorials.git
cd quantum-computing-tutorials
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

### 3. Install the main dependencies

```bash
python -m pip install --upgrade pip
pip install qiskit qiskit-aer qiskit-machine-learning numpy scipy scikit-learn matplotlib pylatexenc jupyter
```

Some folders also contain local requirement files. A pinned repository-wide environment file is planned so that all tutorials can be reproduced with the same tested package versions.

### 4. Launch Jupyter

```bash
jupyter lab
```

Open any tutorial folder and run its notebook from top to bottom.

## Example workflow

Most tutorials follow the same learning sequence:

1. Introduce the physical or computational problem.
2. Explain the quantum principle or algorithm.
3. Construct the circuit or parameterized ansatz.
4. Execute the circuit with a simulator or statevector primitive.
5. Visualize and interpret the result.
6. Discuss assumptions and limitations.




## Background and motivation

 My interest in quantum computing developed further through the **ADEQUATE Advanced End-to-End Quantum Computing Technical Course**, a **Quantum Machine Learning workshop**, and the **QSilver programme organized by QPoland/QWorld**.

This repository connects that training with practical implementation and supports my developing research interests in:

- variational quantum algorithms;
- quantum optimization;
- hybrid quantum-classical computing;
- quantum machine learning for scientific problems.

## Author

**Chalaka Fernando**  
Temporary Assistant Lecturer in Physics  
University of Ruhuna, Sri Lanka

- GitHub: [@chalakafernando4](https://github.com/chalakafernando4)
- Portfolio: [chalakafernando4.github.io](https://chalakafernando4.github.io/)
- LinkedIn: [chalaka-fernando](https://www.linkedin.com/in/chalaka-fernando/)

## Acknowledgements

The tutorials draw on standard quantum-computing literature and the public documentation of Qiskit and related open-source libraries. My learning has also been supported by training activities from QURECA, QPoland, and QWorld. These notebooks are my own educational implementations and are not official course materials from those organizations.

## License

This repository is released under the [MIT License](LICENSE).

Contributions, corrections, and constructive feedback are welcome.

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

from qiskit.circuit.library import ZZFeatureMap
from qiskit_machine_learning.kernels import FidelityQuantumKernel

def run_quantum_machine_learning():
    """Builds and trains a Quantum Support Vector Machine (QSVM)."""
    print("Initializing Quantum Machine Learning Pipeline...\n")

    # --- 1. Generate Non-Linear Classical Data ---
    # We create a dataset of circles within circles. A standard linear ML model would fail here.
    X, y = make_circles(n_samples=100, noise=0.1, factor=0.3, random_state=42)
    
    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- 2. The Quantum Feature Map ---
    # We use a ZZFeatureMap to encode our 2D classical data into a 2-qubit quantum state.
    # This maps the data into a high-dimensional Hilbert space.
    feature_map = ZZFeatureMap(feature_dimension=2, reps=2, entanglement='linear')
    
    # --- 3. Build the Quantum Kernel ---
    # The kernel evaluates the "distance" (fidelity) between data points in the quantum space.
    qkernel = FidelityQuantumKernel(feature_map=feature_map)

    # --- 4. Train the Hybrid Model ---
    print("Training Hybrid Quantum-Classical SVM...")
    print("Encoding classical data into quantum states (this may take a moment)...")
    
    # We pass the quantum kernel evaluation function into a standard scikit-learn SVM
    qsvm = SVC(kernel=qkernel.evaluate)
    qsvm.fit(X_train, y_train)

    # --- 5. Evaluate Accuracy ---
    score = qsvm.score(X_test, y_test)
    print(f"\nSUCCESS! QSVM Classification Accuracy: {score * 100:.2f}%\n")

    # --- 6. Visualization: Decision Boundary ---
    # Create a mesh grid to plot the boundaries the quantum model learned
    h = 0.1  # step size in the mesh
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    
    # Predict the grid using the trained Quantum model
    grid_points = np.c_[xx.ravel(), yy.ravel()]
    Z = qsvm.predict(grid_points)
    Z = Z.reshape(xx.shape)

    # Plotting
    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z, alpha=0.4, cmap=plt.cm.coolwarm)
    plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, edgecolors='k', cmap=plt.cm.coolwarm, label="Training Data")
    plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, marker='x', s=60, cmap=plt.cm.coolwarm, label="Test Data")
    plt.title("QSVM Decision Boundary (Quantum Kernel)")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.legend()
    plt.show()

    # Draw the Quantum Feature Map circuit
    print("\nQuantum Feature Map Circuit (Data Encoding):")
    display(feature_map.decompose().draw('mpl', style='clifford'))

# Execute the QML pipeline
run_quantum_machine_learning()

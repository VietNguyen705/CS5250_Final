"""
Grover's Algorithm - CS 3650 Final
Searches a 3-qubit space (8 states) for the marked state |101>.
Classical search: avg 4 lookups. Grover: 1 iteration finds it with high probability.
"""

import math
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

N_QUBITS = 3
MARKED = "101"  # state we are searching for (read right-to-left in Qiskit: q2 q1 q0)


def oracle(qc: QuantumCircuit, marked: str) -> None:
    """Flip the phase of the marked basis state."""
    # Flip qubits that should be 0 in the marked state so the marked state becomes |111>
    for i, bit in enumerate(reversed(marked)):
        if bit == "0":
            qc.x(i)
    # Multi-controlled Z on |111>
    qc.h(N_QUBITS - 1)
    qc.mcx(list(range(N_QUBITS - 1)), N_QUBITS - 1)
    qc.h(N_QUBITS - 1)
    # Undo the X gates
    for i, bit in enumerate(reversed(marked)):
        if bit == "0":
            qc.x(i)


def diffuser(qc: QuantumCircuit) -> None:
    """Inversion about the mean."""
    for q in range(N_QUBITS):
        qc.h(q)
        qc.x(q)
    qc.h(N_QUBITS - 1)
    qc.mcx(list(range(N_QUBITS - 1)), N_QUBITS - 1)
    qc.h(N_QUBITS - 1)
    for q in range(N_QUBITS):
        qc.x(q)
        qc.h(q)


def build_grover(marked: str) -> QuantumCircuit:
    qc = QuantumCircuit(N_QUBITS, N_QUBITS)
    # Uniform superposition
    for q in range(N_QUBITS):
        qc.h(q)
    # Optimal iteration count: ~ pi/4 * sqrt(N/M)
    iterations = round((math.pi / 4) * math.sqrt(2 ** N_QUBITS))
    for _ in range(iterations):
        oracle(qc, marked)
        diffuser(qc)
    qc.measure(range(N_QUBITS), range(N_QUBITS))
    return qc


def main() -> None:
    qc = build_grover(MARKED)
    print(qc.draw(output="text"))

    sim = AerSimulator()
    tqc = transpile(qc, sim)
    result = sim.run(tqc, shots=1024).result()
    counts = result.get_counts()
    print("\nMeasurement counts:")
    for state, n in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  |{state}>: {n}")
    print(f"\nMarked state: |{MARKED}>")
    print(f"Probability of finding it: {counts.get(MARKED, 0) / 1024:.2%}")

    plot_histogram(counts)
    plt.savefig("results.png", bbox_inches="tight")
    print("\nHistogram saved to results.png")


if __name__ == "__main__":
    main()

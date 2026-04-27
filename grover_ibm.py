"""
Run Grover's algorithm on real IBM Quantum hardware.
Requires an IBM Quantum account: https://quantum.ibm.com (free tier available).

Setup:
    pip install qiskit-ibm-runtime
    # Save your token once:
    # from qiskit_ibm_runtime import QiskitRuntimeService
    # QiskitRuntimeService.save_account(channel="ibm_quantum", token="YOUR_TOKEN")
"""

from qiskit import transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

from grover import build_grover, MARKED


def main() -> None:
    service = QiskitRuntimeService()
    backend = service.least_busy(operational=True, simulator=False)
    print(f"Using backend: {backend.name}")

    qc = build_grover(MARKED)
    tqc = transpile(qc, backend, optimization_level=3)

    sampler = Sampler(backend)
    job = sampler.run([tqc], shots=1024)
    print(f"Job submitted: {job.job_id()}")

    result = job.result()
    counts = result[0].data.c.get_counts()
    print("\nCounts:", counts)
    print(f"Marked |{MARKED}> measured: {counts.get(MARKED, 0)} / 1024")


if __name__ == "__main__":
    main()

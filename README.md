# CS 5250 Final — Grover's Algorithm

Quantum search using Grover's algorithm on a 3-qubit space (8 possible states).
The oracle marks the state `|101>`; one Grover iteration amplifies its amplitude
so measurement returns `101` with very high probability.

## Why Grover?
- Classical search of N items: O(N) lookups (avg N/2)
- Grover's algorithm: O(√N) — quadratic speedup

For N = 8, optimal iterations = round(π/4 · √8) ≈ 2.

## Files
- `grover.py` — full algorithm, runs on local Aer simulator
- `grover_ibm.py` — same circuit on real IBM Quantum hardware
- `results.png` — measurement histogram (generated)

## Run
```bash
pip install -r requirements.txt
python grover.py
```

Expected output: `|101>` measured ~95%+ of the time, all other states near zero.

## Run on real quantum hardware
1. Make a free account at https://quantum.ibm.com
2. Copy your API token from the dashboard
3. Save it once:
   ```python
   from qiskit_ibm_runtime import QiskitRuntimeService
   QiskitRuntimeService.save_account(channel="ibm_quantum", token="YOUR_TOKEN")
   ```
4. `python grover_ibm.py`

## How it works
1. **Superposition** — Hadamard on all qubits → equal amplitude over all 8 states
2. **Oracle** — flips the phase of `|101>` (uses X gates + multi-controlled Z)
3. **Diffuser** — reflects all amplitudes about the mean, amplifying the marked one
4. Repeat oracle+diffuser ~√N times, then measure

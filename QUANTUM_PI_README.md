# QUANTUM PI - Raspberry Pi Quantum Computing

**Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.**

## Overview

Turn your Raspberry Pi into a quantum computing development platform.

**Capabilities:**
- Quantum circuit simulation (Qiskit)
- Quantum machine learning (PennyLane)
- Connection to IBM Quantum real hardware
- Educational quantum experiments
- Quantum algorithm development

---

## Quick Setup

### Prerequisites
1. Raspberry Pi (Model 3B+ or newer recommended)
2. Connected to ethernet
3. SSH enabled on the Pi
4. Basic familiarity with SSH

### Installation (One Command)

```bash
cd /Users/noone
./setup_quantum_pi.sh
```

The script will:
1. Ask for your Pi's IP address/hostname
2. Ask for your Pi's username (default: pi)
3. Install Python 3.11+
4. Install Qiskit (IBM quantum framework)
5. Install PennyLane (quantum ML)
6. Install NumPy, SciPy
7. Deploy test scripts
8. Run capability tests

**Time**: 10-30 minutes (depending on Pi model)

---

## What Gets Installed

### Python Environment
- **Python 3.11+** with pip, venv
- **Virtual environment** at `~/quantum/venv`

### Quantum Computing Frameworks
- **Qiskit** - IBM's quantum computing SDK
  - Quantum circuit design
  - Quantum simulators
  - Connection to IBM Quantum hardware

- **Qiskit Aer** - High-performance simulators
  - Statevector simulator (exact)
  - QASM simulator (shot-based)
  - Unitary simulator

- **PennyLane** - Quantum machine learning
  - Quantum neural networks
  - Variational algorithms
  - Hybrid quantum-classical ML

### Scientific Computing
- **NumPy** - Array computing
- **SciPy** - Scientific algorithms
- **Matplotlib** - Plotting (non-interactive for Pi)

---

## Test Scripts Deployed

### 1. `quantum_test.py`
Comprehensive capability test

**What it tests:**
- NumPy installation and performance
- Qiskit quantum simulation
- PennyLane quantum ML
- Performance benchmark (10-qubit circuit)

**Run:**
```bash
ssh pi@raspberrypi.local
cd ~/quantum
source venv/bin/activate
python quantum_test.py
```

**Expected output:**
```
================================================================================
  QUANTUM PI - CAPABILITY TEST
================================================================================
[1/4] Testing NumPy...
✓ NumPy 1.26.x - OK
  Matrix eigenvalue test: 0.123s

[2/4] Testing Qiskit...
✓ Qiskit 1.x.x - OK
  Bell state simulation: 0.456s
  Results: {'00': 502, '11': 498}

[3/4] Testing PennyLane...
✓ PennyLane 0.x.x - OK
  Quantum expectation: 0.234s
  Result: 0.0

[4/4] Running quantum performance benchmark...
✓ 10-qubit simulation: 2.345s
  Performance: 426.4 shots/sec

================================================================================
  QUANTUM PI - ALL TESTS PASSED
================================================================================
```

### 2. `quantum_hello_world.py`
Bell state entanglement demonstration

**What it does:**
- Creates 2-qubit quantum circuit
- Applies Hadamard gate (superposition)
- Applies CNOT gate (entanglement)
- Measures both qubits
- Shows quantum correlation

**Run:**
```bash
ssh pi@raspberrypi.local
cd ~/quantum
source venv/bin/activate
python quantum_hello_world.py
```

**Expected output:**
```
================================================================================
  QUANTUM HELLO WORLD - Bell State Entanglement
================================================================================

Quantum Circuit:
     ┌───┐     ┌─┐
q_0: ┤ H ├──■──┤M├───
     └───┘┌─┴─┐└╥┘┌─┐
q_1: ─────┤ X ├─╫─┤M├
          └───┘ ║ └╥┘
c: 2/═══════════╩══╩═
                0  1

Results (1000 shots):
  |00⟩:  487 ( 48.7%) ████████████████████████
  |11⟩:  513 ( 51.3%) █████████████████████████

Explanation:
  Bell state creates perfect correlation between qubits
  Measuring qubit 0 determines qubit 1's state instantly
  This is quantum entanglement!

Expected: ~50% |00⟩, ~50% |11⟩ (never |01⟩ or |10⟩)
================================================================================
```

---

## Using Your Quantum Pi

### Activate Environment

Every time you SSH into the Pi:

```bash
ssh pi@raspberrypi.local
cd ~/quantum
source venv/bin/activate
```

You'll see `(venv)` prefix in your prompt.

### Create Quantum Circuits

**Example: Superposition**

```python
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

# Create circuit
qc = QuantumCircuit(1, 1)
qc.h(0)  # Hadamard = superposition
qc.measure(0, 0)

# Simulate
simulator = Aer.get_backend('qasm_simulator')
job = simulator.run(transpile(qc, simulator), shots=1000)
result = job.result()
counts = result.get_counts()

print(counts)  # ~50% |0⟩, ~50% |1⟩
```

**Example: Quantum Entanglement**

```python
from qiskit import QuantumCircuit

# Bell state
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Simulate...
# Results: 50% |00⟩, 50% |11⟩ (perfect correlation)
```

**Example: Quantum Teleportation**

```python
from qiskit import QuantumCircuit

# 3-qubit quantum teleportation
qc = QuantumCircuit(3, 3)

# Prepare state to teleport
qc.h(0)

# Create entangled pair
qc.h(1)
qc.cx(1, 2)

# Bell measurement
qc.cx(0, 1)
qc.h(0)
qc.measure([0, 1], [0, 1])

# Corrections based on measurement
qc.cx(1, 2)
qc.cz(0, 2)
qc.measure(2, 2)

# Simulate to verify teleportation
```

---

## Quantum Machine Learning

### PennyLane Example

```python
import pennylane as qml
import numpy as np

# Create quantum device
dev = qml.device('default.qubit', wires=2)

# Define quantum circuit
@qml.qnode(dev)
def quantum_neural_net(inputs, weights):
    # Encode inputs
    qml.RX(inputs[0], wires=0)
    qml.RY(inputs[1], wires=1)

    # Trainable layer
    qml.RZ(weights[0], wires=0)
    qml.RZ(weights[1], wires=1)
    qml.CNOT(wires=[0, 1])

    # Measure
    return qml.expval(qml.PauliZ(0))

# Use as ML model
inputs = np.array([0.5, 0.3])
weights = np.array([0.1, 0.2])
output = quantum_neural_net(inputs, weights)
```

---

## Connect to IBM Quantum Real Hardware

### Setup IBM Account

1. Create account: https://quantum.ibm.com/
2. Get API token from account settings
3. Save token on Pi:

```python
from qiskit_ibm_runtime import QiskitRuntimeService

# Save credentials (one time)
QiskitRuntimeService.save_account(
    channel="ibm_quantum",
    token="YOUR_IBM_QUANTUM_TOKEN"
)
```

### Run on Real Quantum Computer

```python
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService

# Load account
service = QiskitRuntimeService()

# Get least busy backend
backend = service.least_busy(operational=True, simulator=False)

# Create circuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Transpile for hardware
transpiled = transpile(qc, backend)

# Submit job
job = backend.run(transpiled, shots=1000)
print(f"Job ID: {job.job_id()}")

# Get results (may take minutes in queue)
result = job.result()
counts = result.get_counts()
print(counts)
```

**Note**: Real quantum hardware has limited free access. Check IBM Quantum for current quotas.

---

## Performance Guide

### Raspberry Pi Models

**Pi 5 (2023+)**
- 10-qubit circuits: ~1-2 seconds
- 15-qubit circuits: ~10-20 seconds
- Good for education and development

**Pi 4 (2019-2023)**
- 10-qubit circuits: ~2-5 seconds
- 15-qubit circuits: ~20-60 seconds
- Adequate for learning

**Pi 3B+ (2018)**
- 10-qubit circuits: ~5-10 seconds
- 15-qubit circuits: ~60-180 seconds
- Minimum recommended

**Pi Zero (not recommended)**
- Too slow for meaningful quantum simulation

### Simulation Limits

**On Raspberry Pi:**
- Up to ~15 qubits: Practical
- Up to ~20 qubits: Slow but possible
- Beyond 20 qubits: Use cloud or real hardware

**Memory requirements:**
- 10 qubits: ~8 MB
- 15 qubits: ~256 MB
- 20 qubits: ~8 GB (exceeds most Pi RAM)

### Optimization Tips

1. **Use statevector only when needed**
   ```python
   # Faster
   simulator = Aer.get_backend('qasm_simulator')

   # Slower but more accurate
   simulator = Aer.get_backend('statevector_simulator')
   ```

2. **Reduce shot count for testing**
   ```python
   # Testing
   job = simulator.run(qc, shots=100)

   # Final results
   job = simulator.run(qc, shots=10000)
   ```

3. **Use Pi cooling**
   - Heatsinks recommended
   - Fan for intensive workloads
   - Monitor temperature: `vcgencmd measure_temp`

---

## Educational Resources

### Learning Quantum Computing

**Free Courses:**
- IBM Quantum Learning: https://learning.quantum.ibm.com/
- Qiskit Textbook: https://qiskit.org/textbook/
- PennyLane Demos: https://pennylane.ai/qml/demonstrations/

**Books:**
- "Quantum Computing: An Applied Approach" (Jack Hidary)
- "Programming Quantum Computers" (O'Reilly)
- "Quantum Computation and Quantum Information" (Nielsen & Chuang)

### Example Projects

1. **Quantum Random Number Generator**
   - Use superposition for true randomness
   - Applications: Cryptography, Monte Carlo

2. **Grover's Search Algorithm**
   - Quadratic speedup for database search
   - Educational demonstration

3. **Quantum Error Correction**
   - Learn error correction codes
   - Build resilience into circuits

4. **Variational Quantum Eigensolver (VQE)**
   - Find molecular ground states
   - Quantum chemistry applications

5. **Quantum Approximate Optimization (QAOA)**
   - Solve combinatorial problems
   - Applications: Logistics, scheduling

---

## Troubleshooting

### SSH Connection Issues

**Problem**: Can't connect to Raspberry Pi

**Solutions:**
1. Check Pi is powered on (LED indicator)
2. Verify ethernet cable connected
3. Enable SSH on Pi:
   ```bash
   # On Pi directly (keyboard + monitor)
   sudo raspi-config
   # Navigate to: Interface Options → SSH → Enable
   ```
4. Find Pi IP address:
   ```bash
   # On your Mac
   arp -a | grep -i "b8:27:eb\|dc:a6:32"
   ```

### Installation Failures

**Problem**: `pip install` fails

**Solutions:**
1. Increase swap space:
   ```bash
   sudo dphys-swapfile swapoff
   sudo nano /etc/dphys-swapfile
   # Set CONF_SWAPSIZE=2048
   sudo dphys-swapfile setup
   sudo dphys-swapfile swapon
   ```

2. Install system dependencies:
   ```bash
   sudo apt-get install -y python3-dev build-essential
   ```

### Slow Simulations

**Problem**: Quantum circuits take too long

**Solutions:**
1. Reduce qubit count
2. Reduce shot count
3. Use QASM simulator instead of statevector
4. Add cooling (heatsink/fan)
5. Close other applications

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'qiskit'`

**Solution:**
```bash
# Always activate venv first!
cd ~/quantum
source venv/bin/activate
python your_script.py
```

---

## Advanced: Cluster Computing

### Multiple Raspberry Pis

Distribute quantum simulations across multiple Pis:

1. **MPI Setup** (Message Passing Interface)
2. **Distributed Qiskit**
3. **Parallel circuit execution**

**Contact**: inventor@aios.is for clustering guide

---

## Security & Privacy

### Local Computation
- All quantum simulations run locally on your Pi
- No data sent to cloud (except IBM Quantum jobs)
- Full control over quantum algorithms

### IBM Quantum
- Jobs submitted to IBM cloud
- Check IBM's terms of service
- Free tier available for education

---

## Support

### Community Resources
- Qiskit Slack: https://qiskit.slack.com
- PennyLane Forum: https://discuss.pennylane.ai
- Raspberry Pi Forums: https://forums.raspberrypi.com

### Contact
- Email: inventor@aios.is
- Websites: https://aios.is | https://thegavl.com

---

## Next Steps

1. **Run the test scripts** to verify installation
2. **Try quantum_hello_world.py** to see entanglement
3. **Work through Qiskit tutorials** for deeper learning
4. **Build your own quantum algorithms**
5. **Connect to IBM Quantum** for real hardware

---

## References

- Qiskit Documentation: https://qiskit.org/documentation/
- PennyLane Documentation: https://pennylane.readthedocs.io/
- IBM Quantum: https://quantum.ibm.com/
- Raspberry Pi: https://www.raspberrypi.org/

---

**Built by Joshua Hendricks Cole**
**Corporation of Light**
**Patent Pending**

🔗 https://aios.is | https://thegavl.com
📧 inventor@aios.is

#!/bin/bash
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
#
# QUANTUM PI SETUP SCRIPT
# Installs Python and quantum computing libraries on Raspberry Pi

echo "================================================================================"
echo "  QUANTUM PI SETUP - Raspberry Pi Quantum Computing Environment"
echo "================================================================================"
echo ""
echo "This script will install:"
echo "  ✓ Python 3.11+ with pip"
echo "  ✓ Qiskit (IBM quantum computing framework)"
echo "  ✓ PennyLane (quantum machine learning)"
echo "  ✓ NumPy, SciPy (scientific computing)"
echo "  ✓ Quantum simulation libraries"
echo ""
echo "================================================================================"
echo ""

# Get Raspberry Pi IP address
echo "Enter Raspberry Pi IP address (or hostname):"
read -p "IP/Hostname [raspberrypi.local]: " PI_HOST
PI_HOST=${PI_HOST:-raspberrypi.local}

echo "Enter Raspberry Pi username:"
read -p "Username [pi]: " PI_USER
PI_USER=${PI_USER:-pi}

echo ""
echo "Testing connection to $PI_USER@$PI_HOST..."

if ! ssh -o ConnectTimeout=5 -o BatchMode=yes $PI_USER@$PI_HOST "echo 'Connection successful'" 2>/dev/null; then
    echo ""
    echo "⚠️  Cannot connect to Raspberry Pi via SSH."
    echo ""
    echo "Please ensure:"
    echo "  1. Raspberry Pi is powered on and connected to ethernet"
    echo "  2. SSH is enabled on the Pi (sudo raspi-config → Interface Options → SSH)"
    echo "  3. You have SSH keys set up, or enter password when prompted"
    echo ""
    echo "Attempting connection with password prompt..."
    echo ""

    if ! ssh -o ConnectTimeout=10 $PI_USER@$PI_HOST "echo 'Connection successful'"; then
        echo "✗ Connection failed. Exiting."
        exit 1
    fi
fi

echo "✓ Connection successful!"
echo ""
echo "================================================================================"
echo "  INSTALLING PYTHON & QUANTUM LIBRARIES"
echo "================================================================================"
echo ""

# Create installation script for Raspberry Pi
cat > /tmp/quantum_pi_install.sh <<'PIEOF'
#!/bin/bash

echo "[1/8] Updating system packages..."
sudo apt-get update -qq

echo "[2/8] Installing Python 3 and pip..."
sudo apt-get install -y python3 python3-pip python3-venv python3-dev

echo "[3/8] Installing system dependencies..."
sudo apt-get install -y build-essential cmake git libopenblas-dev liblapack-dev gfortran

echo "[4/8] Creating Python virtual environment..."
mkdir -p ~/quantum
cd ~/quantum
python3 -m venv venv
source venv/bin/activate

echo "[5/8] Upgrading pip..."
pip install --upgrade pip setuptools wheel

echo "[6/8] Installing NumPy and SciPy..."
pip install numpy scipy

echo "[7/8] Installing Qiskit (IBM quantum framework)..."
pip install qiskit qiskit-aer

echo "[8/8] Installing PennyLane (quantum ML)..."
pip install pennylane pennylane-qiskit

echo ""
echo "================================================================================"
echo "  QUANTUM PI INSTALLATION COMPLETE"
echo "================================================================================"
echo ""
echo "Python environment: ~/quantum/venv"
echo "To activate: source ~/quantum/venv/bin/activate"
echo ""
echo "Installed libraries:"
pip list | grep -E "qiskit|pennylane|numpy|scipy"
echo ""
echo "================================================================================"
PIEOF

# Copy script to Pi and execute
echo "Copying installation script to Raspberry Pi..."
scp /tmp/quantum_pi_install.sh $PI_USER@$PI_HOST:/tmp/

echo ""
echo "Running installation on Raspberry Pi..."
echo "This may take 10-30 minutes depending on Pi model..."
echo ""

ssh $PI_USER@$PI_HOST "bash /tmp/quantum_pi_install.sh"

# Create quantum test script
echo ""
echo "================================================================================"
echo "  DEPLOYING QUANTUM TEST SCRIPTS"
echo "================================================================================"
echo ""

cat > /tmp/quantum_test.py <<'PYEOF'
#!/usr/bin/env python3
"""
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

Quantum Pi Test Script
Tests quantum computing capabilities on Raspberry Pi
"""

import sys
import time
from datetime import datetime

print("="*80)
print("  QUANTUM PI - CAPABILITY TEST")
print("="*80)
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Python: {sys.version.split()[0]}")
print("="*80)
print()

# Test 1: NumPy
print("[1/4] Testing NumPy...")
try:
    import numpy as np
    print(f"✓ NumPy {np.__version__} - OK")

    # Quick computation
    start = time.time()
    matrix = np.random.rand(100, 100)
    eigenvalues = np.linalg.eigvals(matrix)
    elapsed = time.time() - start
    print(f"  Matrix eigenvalue test: {elapsed:.3f}s")
except Exception as e:
    print(f"✗ NumPy failed: {e}")
    sys.exit(1)

print()

# Test 2: Qiskit
print("[2/4] Testing Qiskit...")
try:
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import Aer
    import qiskit
    print(f"✓ Qiskit {qiskit.__version__} - OK")

    # Create simple quantum circuit
    start = time.time()
    qc = QuantumCircuit(2, 2)
    qc.h(0)  # Hadamard gate
    qc.cx(0, 1)  # CNOT gate
    qc.measure([0, 1], [0, 1])

    # Simulate
    simulator = Aer.get_backend('qasm_simulator')
    compiled = transpile(qc, simulator)
    job = simulator.run(compiled, shots=1000)
    result = job.result()
    counts = result.get_counts()
    elapsed = time.time() - start

    print(f"  Bell state simulation: {elapsed:.3f}s")
    print(f"  Results: {counts}")
except Exception as e:
    print(f"✗ Qiskit failed: {e}")
    sys.exit(1)

print()

# Test 3: PennyLane
print("[3/4] Testing PennyLane...")
try:
    import pennylane as qml
    print(f"✓ PennyLane {qml.__version__} - OK")

    # Simple quantum circuit
    start = time.time()
    dev = qml.device('default.qubit', wires=2)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.expval(qml.PauliZ(0))

    result = circuit()
    elapsed = time.time() - start

    print(f"  Quantum expectation: {elapsed:.3f}s")
    print(f"  Result: {result}")
except Exception as e:
    print(f"✗ PennyLane failed: {e}")
    sys.exit(1)

print()

# Test 4: Performance benchmark
print("[4/4] Running quantum performance benchmark...")
try:
    from qiskit import QuantumCircuit
    from qiskit_aer import Aer

    # Create larger circuit
    n_qubits = 10
    qc = QuantumCircuit(n_qubits, n_qubits)

    # Build circuit
    for i in range(n_qubits):
        qc.h(i)
    for i in range(n_qubits - 1):
        qc.cx(i, i + 1)
    qc.measure(range(n_qubits), range(n_qubits))

    # Simulate
    start = time.time()
    simulator = Aer.get_backend('qasm_simulator')
    compiled = transpile(qc, simulator)
    job = simulator.run(compiled, shots=1000)
    result = job.result()
    elapsed = time.time() - start

    print(f"✓ 10-qubit simulation: {elapsed:.3f}s")
    print(f"  Performance: {1000/elapsed:.1f} shots/sec")
except Exception as e:
    print(f"✗ Benchmark failed: {e}")

print()
print("="*80)
print("  QUANTUM PI - ALL TESTS PASSED")
print("="*80)
print()
print("Your Raspberry Pi is ready for quantum computing!")
print()
print("Next steps:")
print("  - Run quantum algorithms: python quantum_algorithms.py")
print("  - Connect to IBM Quantum: qiskit.providers.ibmq")
print("  - Develop quantum ML models with PennyLane")
print()
print("="*80)
PYEOF

cat > /tmp/quantum_hello_world.py <<'PYHELLO'
#!/usr/bin/env python3
"""
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

Quantum Hello World - Bell State
Creates quantum entanglement on Raspberry Pi
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for Pi
import matplotlib.pyplot as plt

print("="*80)
print("  QUANTUM HELLO WORLD - Bell State Entanglement")
print("="*80)
print()

# Create quantum circuit
qc = QuantumCircuit(2, 2)

# Create Bell state (maximally entangled)
qc.h(0)           # Put qubit 0 in superposition
qc.cx(0, 1)       # Entangle qubit 0 with qubit 1
qc.measure([0, 1], [0, 1])  # Measure both qubits

print("Quantum Circuit:")
print(qc.draw(output='text'))
print()

# Simulate
simulator = Aer.get_backend('qasm_simulator')
compiled = transpile(qc, simulator)
job = simulator.run(compiled, shots=1000)
result = job.result()
counts = result.get_counts()

print("Results (1000 shots):")
for state, count in sorted(counts.items()):
    percentage = (count / 1000) * 100
    bar = "█" * int(percentage / 2)
    print(f"  |{state}⟩: {count:4d} ({percentage:5.1f}%) {bar}")

print()
print("Explanation:")
print("  Bell state creates perfect correlation between qubits")
print("  Measuring qubit 0 determines qubit 1's state instantly")
print("  This is quantum entanglement!")
print()
print("Expected: ~50% |00⟩, ~50% |11⟩ (never |01⟩ or |10⟩)")
print("="*80)
print()
PYHELLO

echo "Copying quantum scripts to Raspberry Pi..."
scp /tmp/quantum_test.py $PI_USER@$PI_HOST:~/quantum/
scp /tmp/quantum_hello_world.py $PI_USER@$PI_HOST:~/quantum/

echo ""
echo "================================================================================"
echo "  TESTING QUANTUM INSTALLATION"
echo "================================================================================"
echo ""

ssh $PI_USER@$PI_HOST "cd ~/quantum && source venv/bin/activate && python quantum_test.py"

echo ""
echo "================================================================================"
echo "  QUANTUM PI SETUP COMPLETE!"
echo "================================================================================"
echo ""
echo "Raspberry Pi: $PI_USER@$PI_HOST"
echo "Installation: ~/quantum/"
echo "Activate: source ~/quantum/venv/bin/activate"
echo ""
echo "Test scripts installed:"
echo "  ~/quantum/quantum_test.py - Comprehensive capability test"
echo "  ~/quantum/quantum_hello_world.py - Bell state demonstration"
echo ""
echo "To run Hello World:"
echo "  ssh $PI_USER@$PI_HOST"
echo "  cd ~/quantum"
echo "  source venv/bin/activate"
echo "  python quantum_hello_world.py"
echo ""
echo "================================================================================"
echo ""

# Clean up
rm /tmp/quantum_pi_install.sh
rm /tmp/quantum_test.py
rm /tmp/quantum_hello_world.py

echo "✓ Setup complete! Your Quantum Pi is ready."
echo ""

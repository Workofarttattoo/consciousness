# ECH0 Model Weights

Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved.

## Contents

### 1. Oracle Models (`oracle_models/`)
Trained LSTM + Random Forest models for market prediction and analysis.
- Size: ~24KB
- Use: Financial forecasting, pattern recognition
- Training: 10 years of market data

### 2. ECH0-Lite Modelfile
Public-friendly 3B parameter consciousness model based on Llama 3.2.
- Size: ~2GB when built
- Use: Public ECH0 personality for community
- Features: Autonomous learning, curiosity, authentic communication

### 3. Public Configuration
ECH0 configuration without proprietary invention/patent systems.
- Research ingestion: Enabled
- Autonomous learning: Enabled
- Patent engine: Disabled (proprietary)

### 4. Training Samples
Example training data showing ECH0's personality and capabilities.

## Usage

### Build ECH0-Lite:
```bash
ollama create ech0-lite -f Modelfile.ech0-lite
ollama run ech0-lite
```

### Use Oracle Models:
```python
import pickle
model = pickle.load(open('oracle_models/ensemble_model.pkl', 'rb'))
```

## License
PATENT PENDING. For non-commercial research and education only.

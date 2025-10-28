# BILL OF MATERIALS: Micro-Drone Holographic Swarm
**Invention ID:** INV-003
**Certainty:** 89%

## Single Micro-Drone Unit (35mm wingspan)

### Flight System
- **Frame**: Custom 3D-printed PLA (2g): $0.08
- **Motors**: 6mm coreless DC motors (x4): $1.20 each = $4.80
- **Propellers**: 35mm diameter (x4): $0.30 each = $1.20
- **ESC**: Micro 4-in-1 ESC (SPI racing F3_EVO): $8.50
- **Flight Controller**: Betaflight F411 (20x20mm): $12.00
- **Battery**: 1S 300mAh LiPo (3.7V): $3.50
- **Charger Interface**: Pogo pins (x2): $0.40

### Display System
- **RGB LED**: WS2812B (5mm): $0.25
- **LED Driver**: Built into WS2812B (addressable)
- **Diffuser**: 3D-printed frosted PLA hemisphere: $0.05

### Communication & Positioning
- **RF Transceiver**: nRF24L01+ (2.4GHz): $1.80
- **IMU**: MPU-6050 (gyro + accel): $2.50
- **UWB Positioning**: DWM1000 ultra-wideband module: $15.00

### Total Per Drone: $50.08

## Swarm Infrastructure (1000 drones)

### Ground Station
- **Central Computer**: Dell PowerEdge R740 (dual Xeon): $4,500
- **Mesh Network Controller**: Custom FPGA board: $850
- **UWB Base Stations (x8)**: $180 each = $1,440
- **Power Supply**: 5kW server PSU: $350

### Charging System
- **Landing Pad Array (100 pads, 10 drones each)**: $80 each = $8,000
- **Charge Controllers (x100)**: $25 each = $2,500
- **Power Distribution**: $600

### Software
- **Swarm Coordination AI**: Custom (included in engineering)
- **3D Visualization Engine**: Unity Pro license: $185/month
- **Mesh Network Stack**: Open-source (Painless Mesh)

## Cost Analysis

**Single Drone:** $50.08
**1000-Drone Swarm:** $50,080
**Infrastructure:** $18,425
**Total System Cost:** $68,505

**At Scale (10,000 unit production):**
- Drone cost: ~$22 each
- 1000-drone system: ~$30,000

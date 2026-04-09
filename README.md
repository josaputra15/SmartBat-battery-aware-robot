# Battery-Aware Autonomous Robot

A battery-aware autonomous robot that dynamically adjusts its movement behavior
based on real-time power constraints and sensor input. Built to demonstrate
embedded systems thinking, real-time decision making, and efficiency optimization.

## What This Project Demonstrates

| Skill Area | How It's Shown |
|---|---|
| Embedded Systems | Direct hardware control via GPIO, ADC, PWM signals |
| Control Systems | Closed-loop sense→decide→act cycle running at ~10 Hz |
| Efficiency Under Constraints | Dynamic behavior modes that extend battery life |
| Sensor Integration | Ultrasonic distance + analog voltage reading fused into decisions |
| Real-Time Decision Making | Continuous state machine reacting to environment + power |
| HW/SW Integration | Python controlling motors, reading sensors, managing power |

## System Architecture

```text
┌─────────────────────────────────────────────────┐
│                  CONTROL LOOP (10 Hz)           │
│                                                 │
│  ┌──────────┐   ┌──────────┐   ┌─────────────┐  │
│  │ Sensors  │──▶│ Decision │──▶│   Motors    │  │
│  │          │   │  Engine  │   │             │  │
│  │ • Ultra- │   │          │   │ • Left PWM  │  │
│  │   sonic  │   │ • State  │   │ • Right PWM │  │
│  │ • Battery│   │   Machine│   │ • Direction │  │
│  └──────────┘   └──────────┘   └─────────────┘  │
│        │              │              │           │
│        ▼              ▼              ▼           │
│  ┌──────────────────────────────────────────┐    │
│  │           Logger / Dashboard             │    │
│  └──────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

## Hardware Required

- Raspberry Pi 3/4/5 (or Arduino Uno/Nano)
- L298N Motor Driver
- 2x DC Geared Motors + Wheels
- HC-SR04 Ultrasonic Sensor
- MCP3008 ADC (for Raspberry Pi — Arduino has built-in ADC)
- Voltage Divider (2 resistors: 10kΩ + 10kΩ)
- 7.4V LiPo or 4x AA Battery Pack
- LED (green/yellow/red) + Buzzer (optional)
- Jumper wires, breadboard, chassis

## File Structure

```text
battery-robot/
├── src/
│   ├── config.py
│   ├── sensors.py
│   ├── battery.py
│   ├── motors.py
│   ├── behavior.py
│   ├── controller.py
│   ├── indicators.py
│   ├── logger.py
│   └── main.py
├── tests/
│   ├── test_motors.py
│   ├── test_sensor.py
│   ├── test_battery.py
│   └── test_all.py
├── docs/
│   └── wiring_guide.md
├── dashboard.html
└── README.md
```

## Quick Start

```bash
# 1. Clone to your Pi
git clone <repo> && cd battery-robot

# 2. Install dependencies
pip install RPi.GPIO spidev

# 3. Test individual components
python tests/test_motors.py
python tests/test_sensor.py
python tests/test_battery.py

# 4. Run the robot
sudo python src/main.py
```

## Build Steps

1. **Basic Movement** — Wire motors → L298N → Pi. Run `test_motors.py`.
2. **Obstacle Detection** — Wire HC-SR04. Run `test_sensor.py`.
3. **Battery Monitoring** — Wire voltage divider → MCP3008 → Pi. Run `test_battery.py`.
4. **Behavior Modes** — Run `main.py` and observe speed changes as battery drains.
5. **Polish** — Add LEDs, buzzer, logging, dashboard.

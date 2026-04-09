# Hardware Assembly & Wiring Guide

## Parts List

| Part | Approx Cost | Where to Buy |
|---|---|---|
| Raspberry Pi 3B+/4/5 | $35-55 | Amazon, Adafruit, CanaKit |
| L298N Motor Driver | $6 | Amazon (search "L298N") |
| 2x DC Geared Motors + Wheels | $10 | Amazon (search "TT motor robot") |
| HC-SR04 Ultrasonic Sensor | $3 | Amazon |
| MCP3008 ADC | $4 | Adafruit, Amazon |
| 7.4V LiPo Battery (2S) | $12 | Amazon (or 4x AA holder: $3) |
| 10kOhm Resistors x2 | $1 | Any electronics shop |
| LEDs (red/yellow/green) + 220Ohm resistors | $2 | Amazon |
| Buzzer (active, 5V) | $2 | Amazon |
| Breadboard + Jumper Wires | $8 | Amazon |
| Robot Chassis (2WD) | $12 | Amazon (search "2WD robot chassis") |
| **Total** | **~$95** | |

**Budget option:** Use 4x AA batteries instead of LiPo ($3 vs $12), skip LEDs/buzzer ($4 saved). Minimum cost: ~$75.

---

## Step 1: Mount Motors to Chassis

1. Attach the two DC motors to the chassis using the included screws.
2. Press-fit the wheels onto the motor shafts.
3. Attach the caster wheel to the front of the chassis.
4. Mount the Raspberry Pi and breadboard on top using standoffs or double-sided tape.

```text
        FRONT (caster wheel)
        ┌──────────────────┐
        │    [HC-SR04]     │
        │                  │
        │  [Breadboard]    │
        │  [Raspberry Pi]  │
        │                  │
   [Motor L]          [Motor R]
        └──────────────────┘
           REAR (drive wheels)
```

---

## Step 2: Wire the Motor Driver (L298N)

The L298N is the bridge between your Pi (3.3V logic) and your motors (6-12V power).

### Power connections:

```text
Battery (+) ──────▶ L298N "12V" terminal
Battery (-) ──────▶ L298N "GND" terminal
L298N "GND" ──────▶ Raspberry Pi GND (MUST share ground)
L298N "5V"  ──────▶ (can power Pi if jumper is ON - or leave disconnected)
```

### Motor connections:

```text
L298N OUT1 ──────▶ Left Motor wire 1
L298N OUT2 ──────▶ Left Motor wire 2
L298N OUT3 ──────▶ Right Motor wire 1
L298N OUT4 ──────▶ Right Motor wire 2
```

### Logic connections (L298N -> Raspberry Pi):

```text
L298N ENA  ──────▶ Pi GPIO 18  (PWM for left motor speed)
L298N IN1  ──────▶ Pi GPIO 23  (left motor direction)
L298N IN2  ──────▶ Pi GPIO 24  (left motor direction)
L298N ENB  ──────▶ Pi GPIO 13  (PWM for right motor speed)
L298N IN3  ──────▶ Pi GPIO 5   (right motor direction)
L298N IN4  ──────▶ Pi GPIO 6   (right motor direction)
```

**IMPORTANT:** Remove the jumpers on ENA and ENB pins on the L298N board. Those jumpers lock speed to 100% - we need PWM control.

---

## Step 3: Wire the Ultrasonic Sensor (HC-SR04)

The HC-SR04 operates at 5V but the Pi's GPIO is 3.3V. The TRIG pin is safe (3.3V is enough to trigger). The ECHO pin needs a voltage divider to avoid damaging the Pi.

```text
HC-SR04 VCC  ──────▶ Pi 5V pin
HC-SR04 GND  ──────▶ Pi GND
HC-SR04 TRIG ──────▶ Pi GPIO 17

HC-SR04 ECHO ──┬──▶ 1kΩ resistor ──▶ Pi GPIO 27
               └──▶ 2kΩ resistor ──▶ GND
```

This creates a voltage divider: 5V × (2k / (1k + 2k)) = 3.3V -> safe for Pi.

**Mounting:** Attach the sensor to the front of the chassis facing forward, using hot glue or a small bracket.

---

## Step 4: Wire the MCP3008 ADC (for Battery Monitoring)

The Raspberry Pi has no analog pins. The MCP3008 is a 10-bit ADC that talks over SPI.

### MCP3008 Pin Layout (chip has a notch/dot on pin 1 side):

```text
         ┌───── notch ─────┐
  CH0  1 │ ●               │ 16  VDD (3.3V)
  CH1  2 │                 │ 15  VREF (3.3V)
  CH2  3 │                 │ 14  AGND (GND)
  CH3  4 │    MCP3008      │ 13  CLK (Pi SCLK)
  CH4  5 │                 │ 12  DOUT (Pi MISO)
  CH5  6 │                 │ 11  DIN (Pi MOSI)
  CH6  7 │                 │ 10  CS (Pi CE0)
  CH7  8 │                 │  9  DGND (GND)
         └─────────────────┘
```

### Wiring:

```text
MCP3008 Pin 16 (VDD)  ──────▶ Pi 3.3V
MCP3008 Pin 15 (VREF) ──────▶ Pi 3.3V
MCP3008 Pin 14 (AGND) ──────▶ Pi GND
MCP3008 Pin 13 (CLK)  ──────▶ Pi GPIO 11 (SCLK)
MCP3008 Pin 12 (DOUT) ──────▶ Pi GPIO 9  (MISO)
MCP3008 Pin 11 (DIN)  ──────▶ Pi GPIO 10 (MOSI)
MCP3008 Pin 10 (CS)   ──────▶ Pi GPIO 8  (CE0)
MCP3008 Pin 9  (DGND) ──────▶ Pi GND
```

### Enable SPI on the Pi:

```bash
sudo raspi-config
# -> Interface Options -> SPI -> Enable
```

---

## Step 5: Wire the Voltage Divider (Battery -> ADC)

**Why:** The battery outputs up to 8.4V. The MCP3008 can only read 0-3.3V.
A voltage divider scales it down.

```text
Battery (+) ──▶ [10kΩ R1] ──┬──▶ MCP3008 CH0 (Pin 1)
                             │
                         [10kΩ R2]
                             │
Battery (-) ─────────────────┴──▶ GND
```

With R1=R2=10kΩ: V_out = V_battery / 2
- 8.4V battery -> 4.2V at ADC (still too high for 3.3V reference!)

**Better option:** Use R1=20kΩ, R2=10kΩ for a 3:1 ratio:
- 8.4V -> 2.8V at ADC ✅ safe
- Update `DIVIDER_RATIO = 3.0` in config.py

**Alternative if using 4x AA (6V max):** 10kΩ + 10kΩ is fine:
- 6V -> 3.0V at ADC ✅ safe
- Keep `DIVIDER_RATIO = 2.0` in config.py

---

## Step 6: Wire LEDs and Buzzer (Optional)

```text
Pi GPIO 16 ──▶ [220Ω] ──▶ Green LED (+) ──▶ GND    (HIGH battery)
Pi GPIO 20 ──▶ [220Ω] ──▶ Yellow LED (+) ──▶ GND   (MEDIUM battery)
Pi GPIO 21 ──▶ [220Ω] ──▶ Red LED (+) ──▶ GND      (LOW battery)
Pi GPIO 12 ──▶ Buzzer (+) ──▶ GND                   (CRITICAL alert)
```

LED longer leg = positive (anode). Shorter leg = negative (cathode, goes to GND).

---

## Complete Wiring Summary

```text
Raspberry Pi GPIO (BCM)        Connected To
──────────────────────────      ────────────────────────
GPIO 18 (PWM0)                  L298N ENA (left speed)
GPIO 23                         L298N IN1 (left dir)
GPIO 24                         L298N IN2 (left dir)
GPIO 13 (PWM1)                  L298N ENB (right speed)
GPIO 5                          L298N IN3 (right dir)
GPIO 6                          L298N IN4 (right dir)
GPIO 17                         HC-SR04 TRIG
GPIO 27                         HC-SR04 ECHO (via divider)
GPIO 11 (SCLK)                  MCP3008 CLK
GPIO 9  (MISO)                  MCP3008 DOUT
GPIO 10 (MOSI)                  MCP3008 DIN
GPIO 8  (CE0)                   MCP3008 CS
GPIO 16                         Green LED (via 220Ω)
GPIO 20                         Yellow LED (via 220Ω)
GPIO 21                         Red LED (via 220Ω)
GPIO 12                         Buzzer
5V                              HC-SR04 VCC
3.3V                            MCP3008 VDD + VREF
GND                             Shared ground (all components)
```

---

## Step 7: Software Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python dependencies
pip install RPi.GPIO spidev

# Enable SPI
sudo raspi-config   # -> Interface Options -> SPI -> Enable

# Clone your project
cd ~ && git clone <your-repo-url>
cd battery-robot

# Edit config.py to set SIMULATION_MODE = False
nano src/config.py

# Test components one at a time
python tests/test_motors.py    # Wheels should spin
python tests/test_sensor.py    # Should show distance readings
python tests/test_battery.py   # Should show voltage

# Run the robot
sudo python src/main.py
```

---

## Troubleshooting

**Motors don't spin:**
- Check battery is charged and connected to L298N 12V terminal.
- Verify ENA/ENB jumpers are REMOVED.
- Swap IN1/IN2 wires if a motor spins the wrong direction.

**Sensor reads -1 constantly:**
- Check TRIG and ECHO wires aren't swapped.
- Verify the ECHO voltage divider is wired correctly.
- Make sure there's no obstacle within 2 cm of the sensor.

**Battery reads 0V:**
- Check SPI is enabled: `ls /dev/spidev*` should show `spidev0.0`.
- Verify MCP3008 chip orientation (notch = pin 1 side).
- Check voltage divider resistors are connected correctly.

**"Permission denied" on GPIO:**
- Run with `sudo`: `sudo python src/main.py`
- Or add your user to the gpio group: `sudo usermod -aG gpio $USER`

# Wiring Guide (Raspberry Pi + L298N + HC-SR04 + MCP3008)

## Safety First

- Disconnect battery power while wiring.
- Confirm shared ground between battery, motor driver, Pi, and sensors.
- Never feed battery voltage directly into Pi GPIO pins.

## Motor Driver (L298N)

- `MOTOR_A_EN` -> ENA
- `MOTOR_A_IN1` -> IN1
- `MOTOR_A_IN2` -> IN2
- `MOTOR_B_EN` -> ENB
- `MOTOR_B_IN1` -> IN3
- `MOTOR_B_IN2` -> IN4
- L298N `12V`/`VIN` -> Battery+
- L298N `GND` -> Battery- and Pi GND

## Ultrasonic Sensor (HC-SR04)

- VCC -> 5V
- GND -> GND
- TRIG -> `ULTRASONIC_TRIG`
- ECHO -> `ULTRASONIC_ECHO` (use a divider/level shifter to 3.3V for Pi)

## MCP3008 (SPI ADC)

- VDD, VREF -> 3.3V
- AGND, DGND -> GND
- CLK -> SCLK (GPIO11)
- DOUT -> MISO (GPIO9)
- DIN -> MOSI (GPIO10)
- CS/SHDN -> CE0 (GPIO8)
- CH0 -> midpoint of battery divider

## Battery Divider

- Battery+ -> R1 -> ADC CH0 -> R2 -> GND
- Divider ratio must keep CH0 <= 3.3V at max battery voltage.
- Update `DIVIDER_RATIO` in `src/config.py` to match actual resistor values.

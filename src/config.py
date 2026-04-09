"""config.py — All hardware pins, thresholds, and tuning constants."""

# GPIO Pin Assignments (BCM numbering)
MOTOR_A_EN = 18
MOTOR_A_IN1 = 23
MOTOR_A_IN2 = 24

MOTOR_B_EN = 13
MOTOR_B_IN1 = 5
MOTOR_B_IN2 = 6

ULTRASONIC_TRIG = 17
ULTRASONIC_ECHO = 27

LED_GREEN = 16
LED_YELLOW = 20
LED_RED = 21

BUZZER_PIN = 12

# SPI / ADC Configuration (MCP3008)
SPI_BUS = 0
SPI_DEVICE = 0
SPI_SPEED = 1_000_000
ADC_CHANNEL = 0

# Voltage Divider Calibration
DIVIDER_RATIO = 2.0
ADC_VREF = 3.3
ADC_RESOLUTION = 1024

# Battery Thresholds (volts)
BATTERY_HIGH = 7.4
BATTERY_MEDIUM = 7.0
BATTERY_LOW = 6.6
BATTERY_CRITICAL = 6.2

# Behavior Mode Parameters
BEHAVIOR = {
    "HIGH": {
        "speed": 85,
        "turn_speed": 70,
        "obstacle_threshold_cm": 25,
        "turn_duration": 0.4,
        "description": "Fast & aggressive",
    },
    "MEDIUM": {
        "speed": 60,
        "turn_speed": 50,
        "obstacle_threshold_cm": 35,
        "turn_duration": 0.5,
        "description": "Moderate & cautious",
    },
    "LOW": {
        "speed": 35,
        "turn_speed": 30,
        "obstacle_threshold_cm": 45,
        "turn_duration": 0.6,
        "description": "Slow & efficient",
    },
    "CRITICAL": {
        "speed": 0,
        "turn_speed": 0,
        "obstacle_threshold_cm": 50,
        "turn_duration": 0,
        "description": "Full stop — conserve power",
    },
}

LOOP_HZ = 10
LOOP_PERIOD = 1.0 / LOOP_HZ
BATTERY_SMOOTHING_WINDOW = 10

LOG_FILE = "robot_log.csv"
LOG_ENABLED = True

SIMULATION_MODE = True

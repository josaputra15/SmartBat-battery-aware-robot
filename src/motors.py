"""motors.py — DC motor control via L298N motor driver."""

import config

try:
    if config.SIMULATION_MODE:
        raise ImportError("Simulation mode")
    import RPi.GPIO as GPIO

    _HW_AVAILABLE = True
except ImportError:
    _HW_AVAILABLE = False


class MotorDriver:
    """Controls two DC motors through an L298N H-bridge."""

    def __init__(self):
        self._current_speed = 0
        self._pwm_a = None
        self._pwm_b = None

        if _HW_AVAILABLE:
            GPIO.setmode(GPIO.BCM)
            for pin in (config.MOTOR_A_EN, config.MOTOR_A_IN1, config.MOTOR_A_IN2):
                GPIO.setup(pin, GPIO.OUT)
            for pin in (config.MOTOR_B_EN, config.MOTOR_B_IN1, config.MOTOR_B_IN2):
                GPIO.setup(pin, GPIO.OUT)

            self._pwm_a = GPIO.PWM(config.MOTOR_A_EN, 1000)
            self._pwm_b = GPIO.PWM(config.MOTOR_B_EN, 1000)
            self._pwm_a.start(0)
            self._pwm_b.start(0)

    def forward(self, speed: int):
        speed = self._clamp(speed)
        self._current_speed = speed
        self._set_motor_a("forward", speed)
        self._set_motor_b("forward", speed)
        self._log(f"FORWARD speed={speed}")

    def backward(self, speed: int):
        speed = self._clamp(speed)
        self._current_speed = speed
        self._set_motor_a("backward", speed)
        self._set_motor_b("backward", speed)
        self._log(f"BACKWARD speed={speed}")

    def turn_left(self, speed: int):
        speed = self._clamp(speed)
        self._set_motor_a("backward", speed)
        self._set_motor_b("forward", speed)
        self._log(f"TURN LEFT speed={speed}")

    def turn_right(self, speed: int):
        speed = self._clamp(speed)
        self._set_motor_a("forward", speed)
        self._set_motor_b("backward", speed)
        self._log(f"TURN RIGHT speed={speed}")

    def stop(self):
        self._current_speed = 0
        self._set_motor_a("stop", 0)
        self._set_motor_b("stop", 0)
        self._log("STOP")

    @property
    def current_speed(self) -> int:
        return self._current_speed

    def _set_motor_a(self, direction: str, speed: int):
        if _HW_AVAILABLE:
            if direction == "forward":
                GPIO.output(config.MOTOR_A_IN1, GPIO.HIGH)
                GPIO.output(config.MOTOR_A_IN2, GPIO.LOW)
            elif direction == "backward":
                GPIO.output(config.MOTOR_A_IN1, GPIO.LOW)
                GPIO.output(config.MOTOR_A_IN2, GPIO.HIGH)
            else:
                GPIO.output(config.MOTOR_A_IN1, GPIO.LOW)
                GPIO.output(config.MOTOR_A_IN2, GPIO.LOW)
            self._pwm_a.ChangeDutyCycle(speed)

    def _set_motor_b(self, direction: str, speed: int):
        if _HW_AVAILABLE:
            if direction == "forward":
                GPIO.output(config.MOTOR_B_IN1, GPIO.HIGH)
                GPIO.output(config.MOTOR_B_IN2, GPIO.LOW)
            elif direction == "backward":
                GPIO.output(config.MOTOR_B_IN1, GPIO.LOW)
                GPIO.output(config.MOTOR_B_IN2, GPIO.HIGH)
            else:
                GPIO.output(config.MOTOR_B_IN1, GPIO.LOW)
                GPIO.output(config.MOTOR_B_IN2, GPIO.LOW)
            self._pwm_b.ChangeDutyCycle(speed)

    @staticmethod
    def _clamp(speed: int) -> int:
        return max(0, min(100, int(speed)))

    @staticmethod
    def _log(msg: str):
        if config.SIMULATION_MODE:
            print(f"  [MOTORS] {msg}")

    def cleanup(self):
        self.stop()
        if _HW_AVAILABLE:
            self._pwm_a.stop()
            self._pwm_b.stop()
            GPIO.cleanup(
                [
                    config.MOTOR_A_EN,
                    config.MOTOR_A_IN1,
                    config.MOTOR_A_IN2,
                    config.MOTOR_B_EN,
                    config.MOTOR_B_IN1,
                    config.MOTOR_B_IN2,
                ]
            )

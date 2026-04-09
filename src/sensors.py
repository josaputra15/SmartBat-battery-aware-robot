"""sensors.py — Ultrasonic distance sensor (HC-SR04)."""

import time
import config

try:
    if config.SIMULATION_MODE:
        raise ImportError("Simulation mode")
    import RPi.GPIO as GPIO

    _HW_AVAILABLE = True
except ImportError:
    _HW_AVAILABLE = False


class UltrasonicSensor:
    """Reads distance in centimeters from an HC-SR04 sensor."""

    SPEED_OF_SOUND_CM_PER_S = 34300

    def __init__(self, trig_pin=None, echo_pin=None):
        self.trig = trig_pin or config.ULTRASONIC_TRIG
        self.echo = echo_pin or config.ULTRASONIC_ECHO
        self._sim_distance = 100.0
        self._sim_direction = -1

        if _HW_AVAILABLE:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.trig, GPIO.OUT)
            GPIO.setup(self.echo, GPIO.IN)
            GPIO.output(self.trig, False)
            time.sleep(0.05)

    def read_distance_cm(self) -> float:
        if not _HW_AVAILABLE:
            return self._simulate()
        return self._read_hardware()

    def _read_hardware(self) -> float:
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        timeout = time.time() + 0.04
        pulse_start = time.time()
        while GPIO.input(self.echo) == 0:
            pulse_start = time.time()
            if pulse_start > timeout:
                return -1

        pulse_end = time.time()
        while GPIO.input(self.echo) == 1:
            pulse_end = time.time()
            if pulse_end > timeout:
                return -1

        pulse_duration = pulse_end - pulse_start
        distance = (pulse_duration * self.SPEED_OF_SOUND_CM_PER_S) / 2.0

        if distance < 2 or distance > 400:
            return -1

        return round(distance, 1)

    def _simulate(self) -> float:
        self._sim_distance += self._sim_direction * 3.0
        if self._sim_distance <= 10:
            self._sim_direction = 1
        elif self._sim_distance >= 120:
            self._sim_direction = -1
        return round(self._sim_distance, 1)

    def cleanup(self):
        if _HW_AVAILABLE:
            GPIO.cleanup([self.trig, self.echo])

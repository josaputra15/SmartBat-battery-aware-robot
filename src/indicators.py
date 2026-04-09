"""indicators.py — LED and buzzer feedback for battery state."""

import config

try:
    if config.SIMULATION_MODE:
        raise ImportError("Simulation mode")
    import RPi.GPIO as GPIO

    _HW_AVAILABLE = True
except ImportError:
    _HW_AVAILABLE = False


class Indicators:
    """Manages LED and buzzer output based on robot state."""

    def __init__(self):
        self._buzzer_active = False

        if _HW_AVAILABLE:
            GPIO.setmode(GPIO.BCM)
            for pin in (config.LED_GREEN, config.LED_YELLOW, config.LED_RED):
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.LOW)
            GPIO.setup(config.BUZZER_PIN, GPIO.OUT)
            GPIO.output(config.BUZZER_PIN, GPIO.LOW)

    def update(self, state: str):
        self._all_off()

        if state == "HIGH":
            self._set_led(config.LED_GREEN, True)
        elif state == "MEDIUM":
            self._set_led(config.LED_YELLOW, True)
        elif state == "LOW":
            self._set_led(config.LED_RED, True)
        elif state == "CRITICAL":
            self._set_led(config.LED_RED, True)
            self._buzz(True)

        if config.SIMULATION_MODE:
            symbols = {
                "HIGH": "GREEN",
                "MEDIUM": "YELLOW",
                "LOW": "RED",
                "CRITICAL": "RED+BUZZ",
            }
            print(f"  [INDICATOR] {symbols.get(state, 'OFF')} {state}")

    def _set_led(self, pin: int, on: bool):
        if _HW_AVAILABLE:
            GPIO.output(pin, GPIO.HIGH if on else GPIO.LOW)

    def _buzz(self, on: bool):
        self._buzzer_active = on
        if _HW_AVAILABLE:
            GPIO.output(config.BUZZER_PIN, GPIO.HIGH if on else GPIO.LOW)

    def _all_off(self):
        if _HW_AVAILABLE:
            for pin in (config.LED_GREEN, config.LED_YELLOW, config.LED_RED):
                GPIO.output(pin, GPIO.LOW)
            GPIO.output(config.BUZZER_PIN, GPIO.LOW)
        self._buzzer_active = False

    def cleanup(self):
        self._all_off()
        if _HW_AVAILABLE:
            GPIO.cleanup(
                [
                    config.LED_GREEN,
                    config.LED_YELLOW,
                    config.LED_RED,
                    config.BUZZER_PIN,
                ]
            )

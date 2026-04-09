"""controller.py — Main control loop."""

import time
import config
from sensors import UltrasonicSensor
from battery import BatteryMonitor
from motors import MotorDriver
from behavior import BehaviorEngine
from indicators import Indicators
from logger import DataLogger


class RobotController:
    """Orchestrates all subsystems in a real-time control loop."""

    def __init__(self):
        print("=" * 50)
        print("  BATTERY-AWARE AUTONOMOUS ROBOT")
        print("  Mode: " + ("SIMULATION" if config.SIMULATION_MODE else "HARDWARE"))
        print("=" * 50)

        self.sensor = UltrasonicSensor()
        self.battery = BatteryMonitor()
        self.motors = MotorDriver()
        self.behavior = BehaviorEngine()
        self.indicators = Indicators()
        self.logger = DataLogger()

        self._running = False
        self._loop_count = 0

    def run(self, max_iterations: int = None):
        self._running = True
        print("\n  Starting control loop...\n")

        try:
            while self._running:
                loop_start = time.time()
                self._loop_count += 1

                distance = self.sensor.read_distance_cm()
                voltage = self.battery.read_voltage()
                battery_state = self.battery.get_state(voltage)
                battery_pct = self.battery.get_percentage(voltage)

                state_changed = self.behavior.update_state(battery_state)
                action = self.behavior.decide_action(distance)

                self._execute(action)

                if state_changed:
                    self.indicators.update(battery_state)

                self.logger.log(
                    battery_v=voltage,
                    battery_pct=battery_pct,
                    battery_state=battery_state,
                    distance_cm=distance,
                    action=action["action"],
                    speed=action["speed"],
                    reason=action["reason"],
                )

                if self._loop_count % 5 == 0:
                    self._print_status(voltage, battery_pct, battery_state, distance, action)

                if self.behavior.is_critical:
                    print("\n  CRITICAL BATTERY - Robot stopped.")
                    print("  Waiting 5 seconds then shutting down...\n")
                    time.sleep(5)
                    break

                if max_iterations and self._loop_count >= max_iterations:
                    break

                elapsed = time.time() - loop_start
                sleep_time = config.LOOP_PERIOD - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)

        except KeyboardInterrupt:
            print("\n\n  Ctrl+C - Shutting down gracefully...\n")

        finally:
            self.shutdown()

    def _execute(self, action: dict):
        cmd = action["action"]
        speed = action["speed"]
        duration = action.get("turn_duration", 0)

        if cmd == "forward":
            self.motors.forward(speed)
        elif cmd == "turn_left":
            self.motors.turn_left(speed)
            if duration > 0:
                time.sleep(duration)
        elif cmd == "turn_right":
            self.motors.turn_right(speed)
            if duration > 0:
                time.sleep(duration)
        elif cmd == "stop":
            self.motors.stop()

    def _print_status(self, voltage, pct, state, distance, action):
        pct_clamped = max(0, min(100, pct))
        filled = min(20, pct_clamped // 5)
        bar = "#" * filled + "-" * (20 - filled)
        print(
            f"  [{self._loop_count:>5}] "
            f"Batt: {voltage:.2f}V ({pct_clamped}%) [{bar}] {state:>8} | "
            f"Dist: {distance:>6.1f} cm | "
            f"Action: {action['action']:>12} @ {action['speed']}%"
        )

    def shutdown(self):
        print("  Cleaning up...")
        self._running = False
        self.motors.cleanup()
        self.sensor.cleanup()
        self.battery.cleanup()
        self.indicators.cleanup()
        self.logger.close()
        print("  Shutdown complete.\n")

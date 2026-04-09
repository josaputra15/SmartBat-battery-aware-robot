"""
test_sensor.py — Verify ultrasonic sensor readings.

What "working" looks like:
  - Readings update in real time
  - Moving your hand closer -> number decreases
  - Moving away -> number increases
  - Range: ~2 cm to ~400 cm

Run: python tests/test_sensor.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from sensors import UltrasonicSensor


print("=== Ultrasonic Sensor Test ===")
print("Place hand in front of sensor. Press Ctrl+C to stop.\n")

s = UltrasonicSensor()

try:
    for i in range(50):
        dist = s.read_distance_cm()
        bar = "█" * max(0, int(dist / 5)) if dist > 0 else "ERROR"
        print(f"  Reading {i + 1:>3}: {dist:>7.1f} cm  {bar}")
        time.sleep(0.2)
    print("\n✅ Sensor test complete.")

except KeyboardInterrupt:
    print("\nStopped.")

finally:
    s.cleanup()

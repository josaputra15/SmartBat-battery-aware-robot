"""
test_motors.py — Verify motor wiring and direction.

What "working" looks like:
  - Both wheels spin forward for 2 seconds
  - Both wheels spin backward for 2 seconds
  - Robot pivots left, then right
  - Motors stop

Run: python tests/test_motors.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from motors import MotorDriver


print("=== Motor Test ===\n")
m = MotorDriver()

try:
    print("Forward (speed 50) for 2s...")
    m.forward(50)
    time.sleep(2)

    print("Backward (speed 50) for 2s...")
    m.backward(50)
    time.sleep(2)

    print("Turn left (speed 40) for 1s...")
    m.turn_left(40)
    time.sleep(1)

    print("Turn right (speed 40) for 1s...")
    m.turn_right(40)
    time.sleep(1)

    print("Stop.")
    m.stop()
    print("\n✅ Motor test complete. If wheels moved correctly, wiring is good!")

except Exception as e:
    print(f"\n❌ Error: {e}")

finally:
    m.cleanup()

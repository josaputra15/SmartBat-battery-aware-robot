"""
test_battery.py — Verify battery voltage readings and state classification.

What "working" looks like:
  - Voltage reads between 6.0V and 8.4V for a 2S LiPo
  - State changes as voltage drops
  - Percentage roughly matches expected charge

Run: python tests/test_battery.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from battery import BatteryMonitor


print("=== Battery Monitor Test ===\n")

b = BatteryMonitor()

try:
    for i in range(30):
        v = b.read_voltage()
        state = b.get_state(v)
        pct = b.get_percentage(v)
        bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
        print(f"  Reading {i + 1:>3}: {v:.2f}V  [{bar}] {pct:>3}%  State: {state}")
        time.sleep(0.3)

    print("\n✅ Battery test complete.")

except KeyboardInterrupt:
    print("\nStopped.")

finally:
    b.cleanup()

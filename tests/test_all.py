"""
test_all.py — Quick integration test (runs 30 loop iterations in simulation).

What "working" looks like:
  - Robot starts in HIGH mode at fast speed
  - Battery slowly drains -> transitions to MEDIUM -> LOW -> CRITICAL
  - Obstacle avoidance triggers turns when distance drops
  - Robot stops at CRITICAL
  - CSV log file is created

Run: python tests/test_all.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import config

config.SIMULATION_MODE = True
config.LOG_FILE = "test_log.csv"

from controller import RobotController


print("=== Integration Test (30 iterations) ===\n")

robot = RobotController()
robot.run(max_iterations=30)

if os.path.exists(config.LOG_FILE):
    with open(config.LOG_FILE, encoding="utf-8") as f:
        lines = f.readlines()
    print(f"\n✅ Log file created: {len(lines) - 1} data rows recorded.")
    os.remove(config.LOG_FILE)
else:
    print("\n⚠️  No log file created.")

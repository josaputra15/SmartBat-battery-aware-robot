"""main.py — Entry point for the Battery-Aware Autonomous Robot."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controller import RobotController


def main():
    robot = RobotController()
    robot.run()


if __name__ == "__main__":
    main()

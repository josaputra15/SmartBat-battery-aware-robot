"""behavior.py — State machine that maps battery level to robot behavior."""

import random
import config


class BehaviorEngine:
    """Decides robot actions based on battery state and sensor input."""

    def __init__(self):
        self.current_state = "HIGH"
        self.previous_state = "HIGH"
        self._turn_preference = "left"

    def update_state(self, battery_state: str) -> bool:
        self.previous_state = self.current_state
        self.current_state = battery_state
        changed = self.current_state != self.previous_state

        if changed:
            desc = config.BEHAVIOR[self.current_state]["description"]
            print(
                f"  [BEHAVIOR] State changed: {self.previous_state} -> "
                f"{self.current_state} ({desc})"
            )

        return changed

    def decide_action(self, distance_cm: float) -> dict:
        params = config.BEHAVIOR[self.current_state]

        if self.current_state == "CRITICAL":
            return {
                "action": "stop",
                "speed": 0,
                "turn_duration": 0,
                "reason": "Battery critical - shutting down to preserve cells",
            }

        if 0 < distance_cm < params["obstacle_threshold_cm"]:
            direction = self._pick_turn_direction()
            return {
                "action": f"turn_{direction}",
                "speed": params["turn_speed"],
                "turn_duration": params["turn_duration"],
                "reason": (
                    f"Obstacle at {distance_cm:.0f} cm "
                    f"(threshold: {params['obstacle_threshold_cm']} cm)"
                ),
            }

        if distance_cm < 0:
            return {
                "action": f"turn_{self._pick_turn_direction()}",
                "speed": params["turn_speed"],
                "turn_duration": params["turn_duration"] * 1.5,
                "reason": "Sensor error - turning to be safe",
            }

        return {
            "action": "forward",
            "speed": params["speed"],
            "turn_duration": 0,
            "reason": f"Path clear ({distance_cm:.0f} cm ahead)",
        }

    def _pick_turn_direction(self) -> str:
        if random.random() < 0.7:
            self._turn_preference = (
                "right" if self._turn_preference == "left" else "left"
            )
        else:
            self._turn_preference = random.choice(["left", "right"])
        return self._turn_preference

    @property
    def is_critical(self) -> bool:
        return self.current_state == "CRITICAL"

    @property
    def state_description(self) -> str:
        return config.BEHAVIOR[self.current_state]["description"]

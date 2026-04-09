"""
battery.py — Battery voltage monitoring via MCP3008 ADC.

Why we need an ADC:
  The Raspberry Pi has NO analog input pins. Battery voltage is an analog
  signal, so we use an MCP3008 (10-bit SPI ADC) to convert it to digital.

Why we need a voltage divider:
  A 2S LiPo outputs up to 8.4V. The MCP3008 can only handle 0–3.3V.
  A 10kΩ / 10kΩ divider cuts the voltage in half: 8.4V → 4.2V... still
  too high. In practice, use 10kΩ + 20kΩ for a 3:1 ratio, or adjust
  DIVIDER_RATIO in config.py. The default 2:1 assumes a lower-voltage pack
  or a matched divider.

Reading flow:
  Battery → Voltage Divider → MCP3008 Ch0 → SPI → Raspberry Pi
"""

import time
from collections import deque
import config

try:
    if config.SIMULATION_MODE:
        raise ImportError("Simulation mode")
    import spidev

    _HW_AVAILABLE = True
except ImportError:
    _HW_AVAILABLE = False


class BatteryMonitor:
    """Reads battery voltage and classifies into power states."""

    STATES = ("HIGH", "MEDIUM", "LOW", "CRITICAL")

    def __init__(self):
        self._readings = deque(maxlen=config.BATTERY_SMOOTHING_WINDOW)
        self._sim_voltage = 8.2  # start near full
        self._sim_drain = 0.08  # volts lost per read in simulation (fast for demo)

        if _HW_AVAILABLE:
            self.spi = spidev.SpiDev()
            self.spi.open(config.SPI_BUS, config.SPI_DEVICE)
            self.spi.max_speed_hz = config.SPI_SPEED

    # ── Public API ───────────────────────────────

    def read_voltage(self) -> float:
        """Return smoothed battery voltage in volts."""
        raw = self._read_raw() if _HW_AVAILABLE else self._simulate_raw()
        voltage = self._raw_to_voltage(raw)
        self._readings.append(voltage)
        return round(self._smoothed(), 2)

    def get_state(self, voltage: float = None) -> str:
        """Classify voltage into HIGH / MEDIUM / LOW / CRITICAL."""
        if voltage is None:
            voltage = self.read_voltage()

        if voltage >= config.BATTERY_HIGH:
            return "HIGH"
        elif voltage >= config.BATTERY_MEDIUM:
            return "MEDIUM"
        elif voltage >= config.BATTERY_LOW:
            return "LOW"
        else:
            return "CRITICAL"

    def get_percentage(self, voltage: float = None) -> int:
        """Rough estimate: map voltage range to 0–100%."""
        if voltage is None:
            voltage = self.read_voltage()
        full = 8.4
        empty = config.BATTERY_CRITICAL
        pct = (voltage - empty) / (full - empty) * 100
        return max(0, min(100, int(pct)))

    # ── Internal ─────────────────────────────────

    def _read_raw(self) -> int:
        """Read raw 10-bit value from MCP3008 via SPI."""
        channel = config.ADC_CHANNEL
        # MCP3008 SPI protocol: start bit, single-ended, channel, then read
        cmd = [1, (8 + channel) << 4, 0]
        result = self.spi.xfer2(cmd)
        value = ((result[1] & 3) << 8) | result[2]
        return value

    def _simulate_raw(self) -> int:
        """Fake ADC value that slowly drains, then resets (simulates charge)."""
        self._sim_voltage -= self._sim_drain
        if self._sim_voltage < 5.8:
            self._sim_voltage = 8.4  # "recharge"

        # Reverse the voltage → raw conversion
        v_at_adc = self._sim_voltage / config.DIVIDER_RATIO
        raw = int((v_at_adc / config.ADC_VREF) * config.ADC_RESOLUTION)
        return max(0, min(1023, raw))

    def _raw_to_voltage(self, raw: int) -> float:
        """Convert raw ADC reading to actual battery voltage."""
        v_at_adc = (raw / config.ADC_RESOLUTION) * config.ADC_VREF
        v_battery = v_at_adc * config.DIVIDER_RATIO
        return v_battery

    def _smoothed(self) -> float:
        """Return the average of recent readings to filter noise."""
        if not self._readings:
            return 0.0
        return sum(self._readings) / len(self._readings)

    def cleanup(self):
        if _HW_AVAILABLE:
            self.spi.close()

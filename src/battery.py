"""battery.py — Battery voltage monitoring via MCP3008 ADC."""

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
        self._sim_voltage = 8.2
        self._sim_drain = 0.08

        if _HW_AVAILABLE:
            self.spi = spidev.SpiDev()
            self.spi.open(config.SPI_BUS, config.SPI_DEVICE)
            self.spi.max_speed_hz = config.SPI_SPEED

    def read_voltage(self) -> float:
        if _HW_AVAILABLE:
            raw = self._read_raw()
            voltage = self._raw_to_voltage(raw)
        else:
            voltage = self._simulate_voltage()
        self._readings.append(voltage)
        return round(self._smoothed(), 2)

    def get_state(self, voltage: float = None) -> str:
        if voltage is None:
            voltage = self.read_voltage()

        if voltage >= config.BATTERY_HIGH:
            return "HIGH"
        if voltage >= config.BATTERY_MEDIUM:
            return "MEDIUM"
        if voltage >= config.BATTERY_LOW:
            return "LOW"
        return "CRITICAL"

    def get_percentage(self, voltage: float = None) -> int:
        if voltage is None:
            voltage = self.read_voltage()
        full = 8.4
        empty = config.BATTERY_CRITICAL
        pct = (voltage - empty) / (full - empty) * 100
        return max(0, min(100, int(pct)))

    def _read_raw(self) -> int:
        channel = config.ADC_CHANNEL
        cmd = [1, (8 + channel) << 4, 0]
        result = self.spi.xfer2(cmd)
        value = ((result[1] & 3) << 8) | result[2]
        return value

    def _simulate_voltage(self) -> float:
        self._sim_voltage -= self._sim_drain
        if self._sim_voltage < 5.8:
            self._sim_voltage = 8.4
        return self._sim_voltage

    def _raw_to_voltage(self, raw: int) -> float:
        v_at_adc = (raw / config.ADC_RESOLUTION) * config.ADC_VREF
        v_battery = v_at_adc * config.DIVIDER_RATIO
        return v_battery

    def _smoothed(self) -> float:
        if not self._readings:
            return 0.0
        return sum(self._readings) / len(self._readings)

    def cleanup(self):
        if _HW_AVAILABLE:
            self.spi.close()

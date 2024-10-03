"""Platform for sensor integration."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

# from .heatpump_engine import heatpump_engine
from .heatpump_engine import my_heatpump_engine


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    add_entities([HeatpumpSensor1()])
    add_entities([HeatpumpSensor2()])
    add_entities([HeatpumpSensor3()])
    add_entities([HeatpumpSensor4()])
    add_entities([HeatpumpSensor5()])
    add_entities([HeatpumpSensor6()])


#    my_heatpump_engine.host = str(config["ser2net-host"])
#    my_heatpump_engine.port = int(config["ser2net-port"])


class HeatpumpSensor1(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self):
        """Init sensor."""
        self.eng = my_heatpump_engine

    _attr_name = "luxtronik1 Outdoor temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self.eng.poll_for_stats("baba-cafe", 4322)
        self._attr_native_value = self.eng.outdoor_temp


class HeatpumpSensor2(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self):
        """Init sensor."""
        self.eng = my_heatpump_engine

    _attr_name = "luxtronik1 heating circuit flow temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant .
        """
        self.eng.poll_for_stats("baba-cafe", 4322)
        self._attr_native_value = self.eng.heating_circuit_flow_temp


class HeatpumpSensor3(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self):
        """Init sensor."""
        self.eng = my_heatpump_engine

    _attr_name = "luxtronik1 heating circuit return flow temperature (actual)"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self.eng.poll_for_stats("baba-cafe", 4322)
        self._attr_native_value = self.eng.heating_circuit_return_flow_temp_actual


class HeatpumpSensor4(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self):
        """Init sensor."""
        self.eng = my_heatpump_engine

    _attr_name = "luxtronik1 heating circuit return flow temperature (setpoint)"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self.eng.poll_for_stats("baba-cafe", 4322)
        self._attr_native_value = self.eng.heating_circuit_return_flow_temp_setpoint


class HeatpumpSensor5(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self):
        """Init sensor."""
        self.eng = my_heatpump_engine

    _attr_name = "luxtronik1 hot water temperature (actual)"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self.eng.poll_for_stats("baba-cafe", 4322)
        self._attr_native_value = self.eng.domestic_hot_water_temp_actual


class HeatpumpSensor6(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self):
        """Init sensor."""
        self.eng = my_heatpump_engine

    _attr_name = "luxtronik1 hot water temperature (setpoint)"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self.eng.poll_for_stats("baba-cafe", 4322)
        self._attr_native_value = self.eng.domestic_hot_water_temp_setpoint

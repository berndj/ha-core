"""Luxtronik v1 heatpump sensor integration."""

DOMAIN = "lux_heatpump"


async def async_setup(hass, config):
    """Integration setup."""

    hass.states.async_set("lux_heatpump.connection", "up")

    # Return boolean to indicate that initialization was successful.
    return True

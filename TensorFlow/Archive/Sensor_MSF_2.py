
from micropython import const

import adafruit_bus_device.i2c_device as i2c_device

from periphery import I2C

# Internal constants:
_VCNL4010_I2CADDR_DEFAULT   = const(0x13)
_VCNL4010_COMMAND           = const(0x80)
_VCNL4010_PRODUCTID         = const(0x81)
_VCNL4010_PROXRATE          = const(0x82)
_VCNL4010_IRLED             = const(0x83)
_VCNL4010_AMBIENTPARAMETER  = const(0x84)
_VCNL4010_AMBIENTDATA       = const(0x85)
_VCNL4010_PROXIMITYDATA     = const(0x87)
_VCNL4010_INTCONTROL        = const(0x89)
_VCNL4010_PROXINITYADJUST   = const(0x8A)
_VCNL4010_INTSTAT           = const(0x8E)
_VCNL4010_MODTIMING         = const(0x8F)
_VCNL4010_MEASUREAMBIENT    = const(0x10)
_VCNL4010_MEASUREPROXIMITY  = const(0x08)
_VCNL4010_AMBIENTREADY      = const(0x40)
_VCNL4010_PROXIMITYREADY    = const(0x20)
_VCNL4010_AMBIENT_LUX_SCALE = 0.25  # Lux value per 16-bit result value.

# User-facing constants:
FREQUENCY_3M125    = 3
FREQUENCY_1M5625   = 2
FREQUENCY_781K25   = 1
FREQUENCY_390K625  = 0


class VCNL4010:
    """Vishay VCNL4010 proximity and ambient light sensor."""

    _BUFFER = bytearray(3)

    def __init__(self, address=_VCNL4010_I2CADDR_DEFAULT):
        self._device = I2C('/dev/i2c-1')
        self.led_current = 20
        self.frequency = FREQUENCY_390K625

    def _read_u8(self, address):
        # Read an 8-bit unsigned value from the specified 8-bit address.
        with self._device as i2c:
            self._BUFFER[0] = address & 0xFF
            # i2c.write_then_readinto(self._BUFFER, self._BUFFER, out_end=1, in_start=1)
        return self._BUFFER[1]


























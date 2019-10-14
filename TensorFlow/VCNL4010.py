
from micropython import const

import adafruit_bus_device.i2c_device as i2c_device

from periphery import I2C

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_VCNL4010.git"


# pylint: disable=bad-whitespace
# Internal constants (converted to decimal):
_VCNL4010_I2CADDR_DEFAULT   = const(0x13)
_VCNL4010_COMMAND           = const(128)
_VCNL4010_PRODUCTID         = const(129)
_VCNL4010_PROXRATE          = const(130)
_VCNL4010_IRLED             = const(131)
_VCNL4010_AMBIENTPARAMETER  = const(132)
_VCNL4010_AMBIENTDATA       = const(133)
_VCNL4010_PROXIMITYDATA     = const(134)
_VCNL4010_INTCONTROL        = const(135)
_VCNL4010_PROXINITYADJUST   = const(138)
_VCNL4010_INTSTAT           = const(142)
_VCNL4010_MODTIMING         = const(143)
_VCNL4010_MEASUREAMBIENT    = const(16)
_VCNL4010_MEASUREPROXIMITY  = const(8)
_VCNL4010_AMBIENTREADY      = const(64)
_VCNL4010_PROXIMITYREADY    = const(32)
_VCNL4010_AMBIENT_LUX_SCALE = 0.25  # Lux value per 16-bit result value.

# User-facing constants:
FREQUENCY_3M125    = 3
FREQUENCY_1M5625   = 2
FREQUENCY_781K25   = 1
FREQUENCY_390K625  = 0
# pylint: enable=bad-whitespace

# Disable pylint's name warning as it causes too much noise.  Suffixes like
# BE (big-endian) or mA (milli-amps) don't confirm to its conventions--by
# design (clarity of code and explicit units).  Disable this globally to prevent
# littering the code with pylint disable and enable and making it less readable.
# pylint: disable=invalid-name


class VCNL4010:
    """Vishay VCNL4010 proximity and ambient light sensor."""

    def __init__(self):
        self._device = I2C('/dev/i2c-1')
        self.led_current = 20
        self.frequency = FREQUENCY_390K625
        self._write_u8(_VCNL4010_INTCONTROL, 8)

    def _read_u8(self, address):
        # Read an 8-bit unsigned value from the specified 8-bit address.
        with self._device as i2c:
            msgs = [I2C.Message(address), I2C.Message([0x00], read = True)]
            self.transfer(0x13, msgs)
        return msgs[1].data[0]

    def _write_u8(self, address, val):
        # Write an 8-bit unsigned value to the specified 8-bit address.
        with self._device as i2c:
            msgs = [I2C.Message(address), I2C.Message([val])]
            self.transfer(0x13, msgs)

    @property
    def proximity(self):
        """The detected proximity of an object in front of the sensor.  This
        is a unit-less unsigned 16-bit value (0-65535) INVERSELY proportional
        to the distance of an object in front of the sensor (up to a max of
        ~200mm).  For example a value of 10 is an object farther away than a
        value of 1000.  Note there is no conversion from this value to absolute
        distance possible, you can only make relative comparisons.
        """
        # Clear interrupt.
        status = self._read_u8(_VCNL4010_INTSTAT)
        status &= ~0x80
        self._write_u8(_VCNL4010_INTSTAT, status)
        # Grab a proximity measurement.
        self._write_u8(_VCNL4010_COMMAND, _VCNL4010_MEASUREPROXIMITY)
        # Wait for result, then read and return the 16-bit value.
        while True:
            result = self._read_u8(_VCNL4010_COMMAND)
            if result & _VCNL4010_PROXIMITYREADY:
                return self._read_u8(_VCNL4010_PROXIMITYDATA)
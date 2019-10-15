from micropython import const
from smbus2 import SMBus



# Disable pylint's name warning as it causes too much noise.  Suffixes like
# BE (big-endian) or mA (milli-amps) don't confirm to its conventions--by
# design (clarity of code and explicit units).  Disable this globally to prevent
# littering the code with pylint disable and enable and making it less readable.
# pylint: disable=invalid-name

class PressureSensor:
    """Vishay VCNL4010 proximity and ambient light sensor."""

    def __init__(self):
        self._device = SMBus(1)

    def _read_u8(self, address):
        # Read an 8-bit unsigned value from the specified 8-bit address.
        with SMBus(1) as self._device:
            read = self._device.read_byte_data(_VCNL4010_I2CADDR_DEFAULT, address)
        return read

    def _write_u8(self, address, val):
        # Write an 8-bit unsigned value to the specified 8-bit address.
        with SMBus(1) as self._device:
            self._device.write_byte_data(_VCNL4010_I2CADDR_DEFAULT, address, val)

    def _read_u16BE(self, address):
        with SMBus(1) as self._device:
            read_block = self._device.read_i2c_block_data(_VCNL4010_I2CADDR_DEFAULT, address, 2)
        return (read_block[0] << 8) | read_block[1]

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
                return self._read_u16BE(_VCNL4010_PROXIMITYDATA)

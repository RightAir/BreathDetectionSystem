
def readinto(self, buf, **kwargs):
        """
        Read into ``buf`` from the device. The number of bytes read will be the
        length of ``buf``.
        If ``start`` or ``end`` is provided, then the buffer will be sliced
        as if ``buf[start:end]``. This will not cause an allocation like
        ``buf[start:end]`` will so it saves memory.
        :param bytearray buffer: buffer to write into
        :param int start: Index to start writing at
        :param int end: Index to write up to but not include
        """
        self.i2c.readfrom_into(self.device_address, buf, **kwargs)

def write(self, buf, **kwargs):
        """
        Write the bytes from ``buffer`` to the device. Transmits a stop bit if
        ``stop`` is set.
        If ``start`` or ``end`` is provided, then the buffer will be sliced
        as if ``buffer[start:end]``. This will not cause an allocation like
        ``buffer[start:end]`` will so it saves memory.
        :param bytearray buffer: buffer containing the bytes to write
        :param int start: Index to start writing from
        :param int end: Index to read up to but not include
        :param bool stop: If true, output an I2C stop condition after the buffer is written
        """
        self.i2c.writeto(self.device_address, buf, **kwargs)


def write_then_readinto(self, out_buffer, in_buffer, *, out_start = 0, out_end = None, in_start = 0, in_end = None, stop = False):
    """
        Write the bytes from ``out_buffer`` to the device, then immediately
        reads into ``in_buffer`` from the device. The number of bytes read
        will be the length of ``in_buffer``.
        If ``out_start`` or ``out_end`` is provided, then the output buffer
        will be sliced as if ``out_buffer[out_start:out_end]``. This will
        not cause an allocation like ``buffer[out_start:out_end]`` will so
        it saves memory.
        If ``in_start`` or ``in_end`` is provided, then the input buffer
        will be sliced as if ``in_buffer[in_start:in_end]``. This will not
        cause an allocation like ``in_buffer[in_start:in_end]`` will so
        it saves memory.
    """

    if out_end is None:

        out_end = len(out_buffer)
        if in_end is None:
            in_end = len(in_buffer)

            if stop:
                raise ValueError("Stop must be False. Use writeto instead.")
                if hasattr(self.i2c, 'writeto_then_readfrom'):

        self.i2c.writeto_then_readfrom(self.device_address, out_buffer, in_buffer,
        out_start=out_start, out_end=out_end,
        in_start=in_start, in_end=in_end)

    else:
        self.write(out_buffer, start=out_start, end=out_end, stop=False)
        self.readinto(in_buffer, start=in_start, end=in_end)

# Example of write then read into

_BUFFER = bytearray(3)

    def _read_u8(self, address):
        # Read an 8-bit unsigned value from the specified 8-bit address.
        with self._device as i2c:
            # Set buffer [0] to the address of the register
            self._BUFFER[0] = address & 0xFF
            # Writes the out buffer than reads in in buffer
            i2c.write_then_readinto(self._BUFFER, self._BUFFER, out_end=1, in_start=1)
        return self._BUFFER[1]

"""
Notes
    Write the bytes from out buffer to the device
    Read in buffer from the device
"""

# EXAMPLE OF SMBUS APPLICATION

from smbus2 import SMBus, ic_msg

# Single transaction writing two bytes then read two at address 80
# Attempted to recreate writ then read with both result registers
write = i2c_msg.write(0x13, [0x87, 0x88])
read = i2c_msg.read(0x13, 2)
with SMBus(1) as bus:
    bus.i2c_rdwr(write, read)

with SMBus(1) as bus:
    bus.write_byte_data(0x13, 0x87, self._BUFFER)








from register import *

# Stream Command Contexts
WRITE_INTERNAL = 1
WRITE_EXTERNAL = 3
READ_INTERNAL = 2
READ_EXTERNAL = 4


class StreamContext():
    def __init__(self):
        self.clear_rw_context()

    def addr(self, value):
        return value & 0x3FFF

    def is_read(self, value):
        if ((value & 0x8000) > 0):
            return True
        else:
            return False

    def is_write(self, value):
        if ((value & 0x8000) > 0):
            return False
        else:
            return True

    def is_internal(self, value):
        if ((value & 0x4000) > 0):
            return True
        else:
            return False

    def is_external(self, value):
        if ((value & 0x4000) > 0):
            return False
        else:
            return True

    def set_dma_size(self, size):
        self.rw_size = size

    def set_port_size(self, size):
        self.rw_size = size

    def set_port_address(self, address):
        self.portaddress = address

    # Called whenever we finish processing a command
    def reset_context(self):
        self.stack = []
        self.context = None

    # Called whenever we finish processing an RW operation
    def clear_rw_context(self):
        self.reset_context()
        self.portaddress = None
        self.rw_size = 0

    def print_values(self, values):
        print("0x00 0x02 0x04 0x06 0x08 0x0A 0x0C 0x0E")
        print("---- ---- ---- ---- ---- ---- ---- ----")

        col = 0
        for value in values:
            if (col == 8):
                col = 0
                print
                ""
            print
            "%04x" % (value),
            col += 1

        print
        "\n"

    def feed(self, value_out, value_in):

        # Command sets the context
        if (not self.context):
            if (self.is_internal(value_out)):
                if (self.is_read(value_out)):
                    self.context = READ_INTERNAL
                elif (self.is_write(value_out)):
                    self.context = WRITE_INTERNAL
                else:
                    raise Exception("Command neither read nor write")
            elif (self.is_external(value_out)):
                if (self.is_read(value_out)):
                    self.context = READ_EXTERNAL
                elif (self.is_write(value_out)):
                    self.context = WRITE_EXTERNAL
                else:
                    raise Exception("Command neither read nor write")
            else:
                raise Exception("Command neither internal nor external")

            # Push command and wait for next words
            self.stack.append(value_out)
            return

        # We have a context set, read the data
        if (self.context == WRITE_INTERNAL):
            self.stack.append(value_out)

            # Write register port
            if (self.addr(self.stack[0]) == 0xA00):
                if (self.rw_size == 1):
                    print
                    "rw_size == 1, skipping expected value"
                    self.clear_rw_context()
                    self.feed(value_out, value_in)

                    return
                else:
                    self.rw_size -= 2

                # Write is done
                if (self.rw_size == 0):
                    print("WRITE_INTERNAL_PORT()")
                    self.print_values(self.stack[1:])
                    self.clear_rw_context()
                return

            print("WRITE_INTERNAL(%04x,%04x)" % (self.addr(self.stack[0]), self.stack[1]))
            print
            get_reg(self.addr(self.stack[0]), self.stack[1])

            # Check for host control byte size
            if (self.addr(self.stack[0]) == 0x600):
                self.set_port_size(value_out & 0x1F)
            elif (self.addr(self.stack[0]) == 0x0700):
                self.set_port_address(value_out & 0x3FFF)
            # Check for DMA Size
            elif (self.addr(self.stack[0]) == 0x100):
                self.set_dma_size(value_out & 0xFFF)

            self.reset_context()

        elif (self.context == WRITE_EXTERNAL):
            self.stack.append(value_out)
            if (self.rw_size == 1):
                print
                "rw_size == 1, skipping expected value"
                self.clear_rw_context()
                self.feed(value_out, value_in)
                return
            else:
                self.rw_size -= 2
            # Write is done
            if (self.rw_size == 0):
                print("WRITE_EXTERNAL(%04x)" % self.addr(self.addr(self.stack[0])))
                self.print_values(self.stack[1:])
                self.clear_rw_context()
            return

        elif (self.context == READ_INTERNAL):
            self.stack.append(value_in)

            # Read register port
            if (self.addr(self.stack[0]) == 0x800):
                if (self.rw_size == 1):
                    print
                    "rw_size == 1, skipping expected value"
                    self.clear_rw_context()
                    self.feed(value_out, value_in)
                    return
                else:
                    self.rw_size -= 2
                # Read is done
                if (self.rw_size == 0):
                    print("READ_INTERNAL_PORT(%04x)" % (self.portaddress))
                    self.print_values(self.stack[1:])
                    self.clear_rw_context()
                return

            print("READ_INTERNAL (%04x) == %04x" % (self.addr(self.stack[0]), self.stack[1]))
            print
            get_reg(self.addr(self.stack[0]), self.stack[1])

            self.reset_context()

        elif (self.context == READ_EXTERNAL):
            self.stack.append(value_in)
            if (self.rw_size == 1):
                print
                "rw_size == 1, skipping expected value"
                self.clear_rw_context()
                self.feed(value_out, value_in)
                return
            else:
                self.rw_size -= 2
            # Read is done
            if (self.rw_size == 0):
                print("READ_EXTERNAL(%04x)" % (self.addr(self.stack[0])))
                self.print_values(self.stack[1:])
                self.clear_rw_context()
            return
        else:
            raise Exception("No State!")

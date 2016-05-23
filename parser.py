import sys

from streamcontext import StreamContext

data = open(sys.argv[1], 'r').read()

sc = StreamContext()

limit = -1

# Start with line 2 for CSV Export
for line in data.split("\n")[1:]:
    if (limit == 0):
        print("Processing limit reached.")
        sys.exit(0)
    if (len(line) == 0):
        break

    # CSV Columns
    fields = line.split(",")

    # Basic sanity check
    if (len(fields) < 4):
        continue

    # MOSI/MISO are the final 2 fields for SPI export on Saleae Logic
    str_mosi = fields[2]
    str_miso = fields[3]

    sc.feed(int(str_mosi, 16), int(str_miso, 16))
    limit -= 1

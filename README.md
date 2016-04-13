# QCA4002_SPI_Parser

Parser for QCA4002 SPI capture in CSV format. Supports Saleae Logic export by default but could be made to potentially support any other format.
Understands the context of the stream and can understand when an operation is a DMA operation or just a single transaction.

Recquires that 16 bit word size be set.

Syntax: python parser.py filename.csv

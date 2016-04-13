from math import pow

class Register(object):
  EXTERNAL = 0
  INTERNAL = 1
  READ = 1
  WRITE = 0
  NAME = "RegisterOperation"
  bits = {0: "RESERVED",1: "RESERVED",2: "RESERVED",3: "RESERVED",\
    4: "RESERVED",5: "RESERVED",6: "RESERVED",7: "RESERVED",\
    8: "RESERVED",9: "RESERVED",10: "RESERVED",11: "RESERVED",\
    12: "RESERVED",13: "RESERVED",14: "RESERVED",15: "RESERVED"}
  def __init__(self,value):
    self.value = value

  def get_bit(self,bit):
    if(self.value & int(pow(2,bit))):
      return 1
    else:
      return 0
    
  def __repr__(self):
    s = "%s" % self.NAME
    for i in range(0,16):
      try:
        s = "%s\n%s: %d" % (s,self.bits[i],self.get_bit(i))
      except KeyError:
        pass
    s = "%s\n" % s
    return s
    

class DMASize(Register):
  def __init__(self,value):
    super(DMASize,self).__init__(value)
    self.NAME = "DMA_SIZE"
    self.ADDRESS = 0x0100
  def __repr__(self):
    return "%s : %d\n" % (self.NAME,self.value)
    
class WriteBufferSpace(Register):
  def __init__(self,value):
    super(WriteBufferSpace,self).__init__(value)
    self.NAME = "WRBUF_SPC_AVA"
    self.ADDRESS = 0x0200
  def __repr__(self):
    return "%s : %d\n" % (self.NAME,self.value)      

class ReadBufferSpace(Register):
  def __init__(self,value):
    super(ReadBufferSpace,self).__init__(value)
    self.NAME = "RDBUF_BYTE_AVA"
    self.ADDRESS = 0x0300
  def __repr__(self):
    return "%s : %d\n" % (self.NAME,self.value)      
    
    
class SPIConfig(Register):
  def __init__(self,value):
    super(SPIConfig,self).__init__(value)
    self.bits = {0: "prefetch_mode",1: "16bit_mode",2: "Swap",3: "keep_awake_en",\
    4: "keep_awake_for_intr",7: "spi_io_enable",8: "spi2mbox_intr_en", 9: "miso_muxsel1",\
    9: "miso_muxsel2",11: "prefetch_priority1", 12: "prefetch_priority2",15: "spi_reset"}
    self.NAME = "SPI_CONFIG"
    self.ADDRESS = 0x0400

class SPIStatus(Register):
  def __init__(self,value):
    super(SPIStatus,self).__init__(value)
    self.bits = {0: "host_access_done",1: "rtc_state1",2: "rtc_state2",3: "rdbuf_error",\
    4: "wrbuf_error",5: "mbox_flow_ctrl"}
    self.NAME = "SPI_STATUS"
    self.ADDRESS = 0x0500
    
class HostCtrlByteSize(Register):
 
  def __init__(self,value):
    super(HostCtrlByteSize,self).__init__(value)
    self.bits = {6: "no_addr_increment"}
    self.NAME = "HOST_CTRL_BYTE_SIZE"
    self.ADDRESS = 0x0600
  def __repr__(self):
    s = super(HostCtrlByteSize,self).__repr__()
    s = "%sbyte_size: %d\n" % (s,self.value & 0x3F)
    return s
    
class HostCtrlRegisterConfigure(Register):
  
  def __init__(self,value):
    super(HostCtrlRegisterConfigure,self).__init__(value)
    self.bits = {15: "enable",14: "direction"}
    self.NAME = "HOST_CTRL_CONFIG"
    self.ADDRESS = 0x0700
  def __repr__(self):
    s = super(HostCtrlRegisterConfigure,self).__repr__()
    s = "%saddress: %x\n" % (s,self.value & 0x3FFF)
    return s
    
class InterruptCause(Register):
  def __init__(self,value):
    super(InterruptCause,self).__init__(value)
    self.bits = {0: "packet_available",1: "rdbuf_error",2: "wrbuf_error",3: "address_error",\
    4: "local_cpu _interrupt",5: "counter_interrupt",6: "cpu_on",7: "all_cpu_interrupt",\
    8: "host_ctrl_wr _done",9: "host_ctrl_rd _done",10: "wrbuf_below _watermark"}
    self.NAME = "INTR_CAUSE"
    self.ADDRESS = 0x0C00
    
class InterruptEnable(Register):
  def __init__(self,value):
    super(InterruptEnable,self).__init__(value)
    self.bits = {0: "packet_available",1: "rdbuf_error",2: "wrbuf_error",3: "address_error",\
    4: "local_cpu _interrupt",5: "counter_interrupt",6: "cpu_on",7: "all_cpu_interrupt",\
    8: "host_ctrl_wr _done",9: "host_ctrl_rd _done",10: "wrbuf_below _watermark"}
    self.NAME = "INTR_ENABLE"
    self.ADDRESS = 0x0D00
    
class WriteBufferWritePointer(Register):
  def __init__(self,value):
    super(WriteBufferWritePointer,self).__init__(value)
    self.NAME = "WRBUF_WRPTR"
    self.ADDRESS = 0x0E00    
  def __repr__(self):
    return "%s : %d\n" % (self.NAME,self.value & 0x7FF)    
    
class WriteBufferReadPointer(Register):
  def __init__(self,value):
    super(WriteBufferReadPointer,self).__init__(value)
    self.NAME = "WRBUF_RDPTR"
    self.ADDRESS = 0x0F00    
  def __repr__(self):
    return "%s : %d\n" % (self.NAME,self.value & 0x7FF)    
    
class ReadBufferWritePointer(Register):
  def __init__(self,value):
    super(ReadBufferWritePointer,self).__init__(value)
    self.NAME = "RDBUF_WRPTR"
    self.ADDRESS = 0x1000    
  def __repr__(self):
    return "%s : %d\n" % (self.NAME,self.value & 0xFFF)    
    
class ReadBufferReadPointer(Register):
  def __init__(self,value):
    super(ReadBufferReadPointer,self).__init__(value)
    self.NAME = "RDBUF_RDPTR"
    self.ADDRESS = 0x1100    
  def __repr__(self):
    return "%s : %d\n" % (self.NAME,self.value & 0xFFF)
    
class ReadBufferWatermark(Register):
  def __init__(self,value):
    super(ReadBufferWatermark,self).__init__(value)
    self.NAME = "RDBUF_WATERMARK"
    self.ADDRESS = 0x1200    
  def __repr__(self):
    return "%s : %d\n" % (self.NAME,self.value & 0x7FF)
    
class WriteBufferWatermark(Register):
  def __init__(self,value):
    super(WriteBufferWatermark,self).__init__(value)
    self.NAME = "WRBUF_WATERMARK"
    self.ADDRESS = 0x1300    
  def __repr__(self):
    return "%s : %d\n" % (self.NAME,self.value & 0x7FF)
    
class ReadBufferLookAhead1(Register):
  def __init__(self,value):
    super(ReadBufferLookAhead1,self).__init__(value)
    self.NAME = "RDBUF_LOOKAHEAD1"
    self.ADDRESS = 0x1400    
  def __repr__(self):
    return "%s : %d\n" % (self.NAME,self.value & 0x7FF)

class ReadBufferLookAhead2(Register):
  def __init__(self,value):
    super(ReadBufferLookAhead2,self).__init__(value)
    self.NAME = "RDBUF_LOOKAHEAD2"
    self.ADDRESS = 0x1500    
  def __repr__(self):
    return "%s : %d\n" % (self.NAME,self.value & 0x7FF)
    
def get_reg(addr,value):
  if(DMASize(value).ADDRESS == addr):
    return DMASize(value)
  elif(WriteBufferSpace(value).ADDRESS == addr):
    return WriteBufferSpace(value)
  elif(ReadBufferSpace(value).ADDRESS == addr):
    return ReadBufferSpace(value)
  elif(SPIConfig(value).ADDRESS == addr):
    return SPIConfig(value)
  elif(SPIStatus(value).ADDRESS == addr):
    return SPIStatus(value)
  elif(HostCtrlByteSize(value).ADDRESS == addr):
    return HostCtrlByteSize(value)
  elif(HostCtrlRegisterConfigure(value).ADDRESS == addr):
    return HostCtrlRegisterConfigure(value)
  elif(InterruptCause(value).ADDRESS == addr):
    return InterruptCause(value)
  elif(InterruptEnable(value).ADDRESS == addr):
    return InterruptEnable(value)
  elif(WriteBufferWritePointer(value).ADDRESS == addr):
    return WriteBufferWritePointer(value)
  elif(WriteBufferReadPointer(value).ADDRESS == addr):
    return WriteBufferReadPointer(value)
  elif(ReadBufferWritePointer(value).ADDRESS == addr):
    return ReadBufferWritePointer(value)
  elif(ReadBufferReadPointer(value).ADDRESS == addr):
    return ReadBufferReadPointer(value)
  elif(ReadBufferWatermark(value).ADDRESS == addr):
    return ReadBufferWatermark(value)
  elif(WriteBufferWatermark(value).ADDRESS == addr):
    return WriteBufferWatermark(value)
  elif(ReadBufferLookAhead1(value).ADDRESS == addr):
    return ReadBufferLookAhead1(value)
  elif(ReadBufferLookAhead2(value).ADDRESS == addr):
    return ReadBufferLookAhead2(value)
  else:
    return "No Object: %04x" % addr
 
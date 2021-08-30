from binary_reader import BinaryReader, BrStruct

class NavApproachArea(BrStruct):
  def __init__(self):
    pass
    
  def __br_read__(self, br: 'BinaryReader') -> None:
    br.read_uint32()
    br.read_uint32()
    br.read_uint8()
    br.read_uint32()
    br.read_uint8()
    pass
    
from binary_reader import BinaryReader, BrStruct

class NavSpotOrder(BrStruct):
  def __init__(self):
    pass
    
  def __br_read__(self, br: BinaryReader) -> None:
    self.id = br.read_uint32()
    self.t = br.read_uint8() / 255.0
    
from binary_reader import BinaryReader, BrStruct
from .vector import Vector

class NavHidingSpot(BrStruct):
  def __init__(self):
    self.pos = None
    pass
    
  def __br_read__(self, br: BinaryReader, version: int) -> None:
    if version == 1:
      self.pos = br.read_struct(Vector)
    else:
      self.id = br.read_uint32()
      self.pos = br.read_struct(Vector)
      self.flags = br.read_uint8()
    
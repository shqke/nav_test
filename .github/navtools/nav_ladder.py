from binary_reader import BinaryReader, BrStruct
from .vector import Vector
from .enums import NavDirType

class NavLadder(BrStruct):
  def __init__(self):
    pass
  
  def __br_read__(self, br: BinaryReader, version) -> None:
    self.id = br.read_uint32()
    self.width = br.read_float()
    self.top = br.read_struct(Vector)
    self.bottom = br.read_struct(Vector)
    self.length = br.read_float()
    self.dir = NavDirType(br.read_uint32())
    
    if version == 6:
      self.is_dangling = br.read_uint8() != 0
      
    self.top_forward_area = br.read_uint32()
    self.top_left_area = br.read_uint32()
    self.top_right_area = br.read_uint32()
    self.top_behind_area = br.read_uint32()
    self.bottom_area = br.read_uint32()
      
  def dump(self, f):
    f.write((
      f'NAV LADDER #{self.id}\n'
      f'--------\n'
      f'Top: {self.top}\n'
      f'Bottom: {self.bottom}\n'
      f'Dir: {self.dir.name}\n'
    ))
    
    f.write((
      f'\n'
    ))

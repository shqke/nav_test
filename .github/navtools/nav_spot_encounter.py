from binary_reader import BinaryReader, BrStruct
from .nav_spot_order import NavSpotOrder
from .vector import Vector

class NavSpotEncounter(BrStruct):
  def __init__(self):
    self._from = None
    self._to = None
    pass
    
  def __br_read__(self, br: BinaryReader, version) -> None:
    self.path = {}
    
    if version < 3:
      self.from_id = br.read_uint32()
      self.to_id = br.read_uint32()
      
      self.path['from'] = br.read_struct(Vector)
      self.path['to'] = br.read_struct(Vector)
      
      num_spots = br.read_uint8()
      for i in range(num_spots):
        br.read_float()
        br.read_float()
        br.read_float()
        br.read_float()
    else:
      self.from_id = br.read_uint32()
      self.from_dir = br.read_uint8()
      self.to_id = br.read_uint32()
      self.to_dir = br.read_uint8()
      
      num_spots = br.read_uint8()
      self.spots = br.read_struct(NavSpotOrder, num_spots)
      
    pass
    
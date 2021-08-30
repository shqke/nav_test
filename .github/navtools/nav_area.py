from binary_reader import BinaryReader, BrStruct, Whence
from .nav_spot_encounter import NavSpotEncounter
from .nav_approach_area import NavApproachArea
from .nav_hiding_spot import NavHidingSpot
from .vector import Vector
from .enums import NavDirType, LadderDirectionType, NavCornerType
from .util import Timer

class NavArea(BrStruct):
  def __init__(self):
    pass
  
  def __br_read__(self, br: BinaryReader, version, sub_version) -> None:
    self.id = br.read_uint32()
    
    if version <= 8:
      self.flags = br.read_uint8()
    elif version <= 12:
      self.flags = br.read_uint16()
    else:
      self.flags = br.read_uint32()
      
    self.nw_corner = br.read_struct(Vector)
    self.se_corner = br.read_struct(Vector)
    self.center = (self.nw_corner + self.se_corner) / 2
    
    self.ne_z = br.read_float()
    self.sw_z = br.read_float()
    
    self.connections = []
    for dir_type in NavDirType:
      areas = []
      num_areas = br.read_uint32()
      for _x in range(num_areas):
        other_area_id = br.read_uint32()
        areas.append(other_area_id)
        
      self.connections.append(areas)
      
    # Hiding spots
    num_hiding_spots = br.read_uint8()
    self.hiding_spots = br.read_struct(NavHidingSpot, num_hiding_spots, version)
      
    # Approach areas
    if version < 15:
      self.approach_areas = br.read_struct(NavApproachArea, br.read_uint8())
    
    # Encounter paths
    self.encounter_spots = br.read_struct(NavSpotEncounter, br.read_uint32(), version)
    
    if version < 5:
      return
      
    # Skip place data
    br.read_uint16()
    
    if version < 7:
      return
      
    # Ladder data
    self.ladders = []
    for dir in LadderDirectionType:
      num_connections = br.read_uint32()
      br.seek(num_connections * 4, Whence.CUR)
    # with Timer('ladder connections'):
      # for dir in LadderDirectionType:
        # for i in range(br.read_uint32()):
          # self.ladders.append(( dir, br.read_uint32() ))
      
    if version < 8:
      return
      
    # Earliest occupy times
    self.occupy_times = (br.read_float(), br.read_float())
    
    if version < 11:
      return
      
    self.light_intensity = []
    for type in NavCornerType:
      self.light_intensity.append(br.read_float())
      
    if version < 16:
      return
      
    # Custom data
    if sub_version == 0:
      return
      
    self.terror_spawn_attributes = br.read_uint32()
    
    if sub_version >= 2:
      if sub_version <= 9:
        br.read_uint32()
        br.read_uint32()
        
      if sub_version <= 12:
        br.read_uint32()
        
      if sub_version >= 8:
        self.fog_place_id = br.read_uint16()
        
    if sub_version <= 9:
      if self.terror_spawn_attributes & 8:
        br.read_int32()
        br.read_int32()
        br.read_float()
        br.read_float()
        br.read_int32()
        
      for i in range(br.read_uint8()):
        br.read_uint32()
      
    # Cached visibility information
    if sub_version >= 5:
      br.seek(br.read_uint32() * 5, Whence.CUR)
      # NOTE: Heavy!
      # for i in range(br.read_uint32()):
        # br.read_uint32()
        # br.read_uint8()
      
      # Read area from which we inherit visibility
      self.vis_inherit_from = br.read_uint32()
  
  def __repr__(self):
    return f'NavArea #{self.id}'
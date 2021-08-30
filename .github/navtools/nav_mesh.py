from binary_reader import BinaryReader
from .nav_area import NavArea
from .nav_ladder import NavLadder

class NavMesh(object):
  def load_custom_data_pre_area(self, rs: BinaryReader) -> None:
    self.custom_data = {}
    if self.sub_version <= 7:
      return
    
    if self.sub_version > 11:
      self.population_type = rs.read_str()
      self.fog_places = []
      
      for _x in range(rs.read_uint16()):
        rs.read_uint16() # string length
        self.fog_places.append(rs.read_str())
      if len(self.fog_places) > 0:
        print(self.fog_places)
        
  def load_custom_data(self, rs: BinaryReader) -> None:
    if self.sub_version <= 7:
      return
      
    self.max_view_distance = rs.read_float()
    
  def load_r(self, rs: BinaryReader):
    # Check magic number
    if rs.read_uint32() != 0xfeedface:
      raise Exception('Invalid magic number.')
    
    # Read version
    self.version = rs.read_uint32()
    if self.version < 5 or self.version > 16:
      raise Exception('Unsupported file version {0}.'.format(self.version))
      
    self.sub_version = 0
    # Read sub version
    if self.version >= 10:
      self.sub_version = rs.read_uint32()
      
    self.bsp_size = 0
    if self.version >= 4:
      self.bsp_size = rs.read_uint32()
    
    self.is_analyzed = False
    if self.version >= 14:
      self.is_analyzed = rs.read_uint8() != 0
      
    self.has_unnamed_areas = False
    self.places = []
    if self.version >= 5:
      for _x in range(rs.read_uint16()):
        rs.read_uint16() # string length
        self.places.append(rs.read_str())
        
      if self.version > 11:
        self.has_unnamed_areas = rs.read_uint8() != 0
      
    # Read custom pre area data
    self.load_custom_data_pre_area(rs)
    
    self.areas = {}
    for _x in range(rs.read_uint32()):
      area = rs.read_struct(NavArea, None, self.version, self.sub_version)
      self.areas[area.id] = area
    
    if len(self.areas) == 0:
      raise Exception('Areas count == 0.')
      
    # Read ladders
    if self.version >= 6:
      self.ladders = {}
      for _x in range(rs.read_uint32()):
        ladder = rs.read_struct(NavLadder, None, self.version)
        self.ladders[ladder.id] = ladder
          
    # Load class mesh info
    self.load_custom_data(rs)
    
  def load(self, f):
    rs = BinaryReader(f.read())
    self.load_r(rs)
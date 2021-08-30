from binary_reader import BinaryReader, BrStruct

class Vector(BrStruct):
  def __init__(self, x = 0.0, y = 0.0, z = 0.0):
    self.coords = (x, y, z)
    
  def __br_read__(self, br: BinaryReader) -> None:
    self.__init__( br.read_float(), br.read_float(), br.read_float() )
    
  @property
  def x( self ):
    return self.coords[0]
    
  @property
  def y( self ):
    return self.coords[1]
    
  @property
  def z( self ):
    return self.coords[2]
    
  def __add__(self, other):
    return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
    
  def __sub__(self, other):
    return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
  def __truediv__(self, other):
    return Vector(self.x / other, self.y / other, self.z / other)
    
  def __eq__(self, other):
    return self.coords == other.coords
    
  def __lt__(self, other):
    return self.coords < other.coords
  
  def __repr__(self):
    return f'{self.x:.6f} {self.y:.6f} {self.z:.6f}'
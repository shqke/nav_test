#!/usr/bin/env python
from navtools.nav_mesh import NavMesh
from argparse import ArgumentParser, FileType
import sys
import os
from enum import IntFlag
from navtools.enums import NavDirType, NavBaseAttribute, NavTerrorSpawnAttribute
from navtools.util import Timer

parser = ArgumentParser(description = 'Dumps navmesh data summary into a text file', epilog = 'More info: https://developer.valvesoftware.com/wiki/NAV')
parser.add_argument('input', nargs = '+', type = FileType('rb'), help = 'Source Engine navigation files to process')
parser.add_argument('-o', '--output-dir', help = 'Write output into specified directory, same directory that contains input file otherwise')
parser.add_argument('--stdout', action = 'store_true', help = 'Write into stdout')
# parser.add_argument('-v', '--verbose', action = 'store_true', help = 'Spew more information')
args = parser.parse_args()

def describe_flags(flags, base: IntFlag):
  return ' '.join(
    map(
      lambda attr: attr.name,
      filter(
        lambda attr: ( flags & attr.value ) != 0,
        base
      )
    )
  )
  
def describe_list(lst):
  return ' '.join(
    map(
      lambda item: str(item),
      lst
    )
  )

def describe_navladder(f, ladder):
  f.write((
    f'NAV LADDER #{ladder.id}\n'
    f'--------\n'
    f'Top: {ladder.top}\n'
    f'Bottom: {ladder.bottom}\n'
    f'Dir: {ladder.dir.name}\n'
    f'\n'
  ))

def describe_navarea(f, area):
  f.write((
    f'NAV AREA #{area.id}\n'
    f'--------\n'
    f'Center Position: {area.center}\n'
    f'Corner NW: {area.nw_corner}\n'
    f'Corner SE: {area.se_corner}\n'
    f'Corner Heights: NE [ {area.ne_z:.6f} ], SW [ {area.sw_z:.6f} ]\n'
    f'Base Attribute Flags: 0x{area.flags:08x} [ {describe_flags(area.flags, NavBaseAttribute)} ]\n'
  ))
  
  if hasattr(area, 'terror_spawn_attributes'):
    f.write((
      f'Terror Spawn Attribute Flags: 0x{area.terror_spawn_attributes:08x} [ {describe_flags(area.terror_spawn_attributes, NavTerrorSpawnAttribute)} ]\n'
    ))
  
  f.write((
    f'Connections:\n'
  ))
  
  for dir in NavDirType:
    f.write((
      f'\t{dir.name}: [ {describe_list(area.connections[dir])} ]\n'
    ))
    
  f.write((
    f'Ladder Data:\n'
  ))
  
  if len(area.ladders) != 0:
    for dir, id in area.ladders:
      f.write((
        f'\t{dir.name}: Ladder #{id}\n'
      ))
  else:
    f.write((
      f'\tNone\n'
    ))

  f.write((
    f'\n'
  ))

def describe_navmesh(f, mesh):
  f.write((
    f'Output file: {os.path.basename(f.name)}\n'
    f'Version: {mesh.version}\n'
    f'Sub-Version: {mesh.sub_version}\n'
    f'BSP File Size: {mesh.bsp_size} bytes\n'
  ))
  
  if hasattr(mesh, 'population_type'):
    f.write((
      f'Population Preset: {mesh.population_type}\n'
    ))
    
  if hasattr(mesh, 'max_view_distance'):
    f.write((
      f'Max View Distance: {mesh.max_view_distance}\n'
    ))
    
  for i, place in enumerate(mesh.places):
    f.write((
      f'Place #{i}: {place}\n'
    ))
    
  f.write((
    f'\n'
    f'===============================\n'
    f'           NAV AREAS           \n'
    f'===============================\n'
    f'\n'
  ))
  
  # Dump nav areas
  # Sort areas by coordinates in ascending order
  for area in sorted(mesh.areas.values(), key = lambda area: area.center):
    describe_navarea(f, area)
    
  f.write((
    f'===============================\n'
    f'Number of Nav Areas: {len(mesh.areas)}\n'
    f'\n'
  ))
  
  # Dump nav ladders
  f.write((
    f'\n'
    f'===============================\n'
    f'          NAV LADDERS          \n'
    f'===============================\n'
    f'\n'
  ))
  
  for ladder in sorted(mesh.ladders.values(), key = lambda ladder: ladder.top):
    describe_navladder(f, ladder)
  
  f.write((
    f'===============================\n'
    f'Number of Nav Ladders: {len(mesh.ladders)}\n'
    f'\n'
  ))

def dump_file(f):
  input_path = os.path.normpath(f.name)
  print(f'Reading from "{input_path}"')

  mesh = NavMesh()
  mesh.load(f)
  
  if args.stdout is True:
    describe_navmesh(sys.stdout, mesh)
    return

  if args.output_dir is None:
    output_dir = os.path.dirname(input_path)
  else:
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
  
  output_path = os.path.join(os.path.normpath(output_dir), os.path.basename(input_path) + '.txt')
  with open(output_path, 'w') as f:
    print(f'Saving output into "{output_path}"')
    describe_navmesh(f, mesh)

def main():
  with Timer('All input files'):
    for f in args.input:
      dump_file(f)
  
main()

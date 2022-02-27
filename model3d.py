#!/usr/bin/env python3
# 3d Model Loading
# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLU import *

import pygame.image
import os.path

__title__ = 'OBJ Loader'
__author__ = 'CoolCat467'
__version__ = '1.2.0'
__ver_major__ = 1
__ver_minor__ = 2
__ver_patch__ = 0

_DO_MIP_MAPS = True

class Material:
    "Material object, stores information about a material."
    texture_filename = None
    ambient = [0, 0, 0]
    diffuse = [0, 0, 0]
    specular = [0, 0, 0]
    shininess = 0.0
    transparency = 0.0
    
    texture_id = None
    
    def __init__(self, name=''):
        self.name = name
    
    def __repr__(self):
        return '<Material Object>'
    pass

class FaceGroup(object):
    """Face group object, stores information about indices, the material name, the type of face group, and the length of itself.
    
    Valid types:
        'tex'
        'notex'
        'line'
        'point'
    """
    def __init__(self, mat_name='', face_type=None):
        self.indices = []
        self.material_name = mat_name
        self.type = face_type
        self.len = 3
    
    def add_indice(self, indice):
        """Add an indice to self. Indice = [vertex index, texture index, normal index]"""
        self.indices.append(indice)
    
    def __repr__(self):
        return '<FaceGroup Object>'
    pass

def _amol(lst, **kwargs):
    "Math Operator acting appon All values of a List."
    data = list(lst)
    for operator in kwargs:
        target = kwargs[operator]
        for i in range(len(data)):
            if operator == 'a':#add
                data[i] += target
            if operator == 's':#subtract
                data[i] -= target
            if operator == 'm':#multiply
                data[i] *= target
            if operator == 'd':#divide
                data[i] /= target
            if operator == 'p':#power
                data[i] **= target
    return tuple(data)

class Model:
    "Base class for storing 3d models."
    def __init__(self, debug=False):
        self.vertices = []
        self.tex_coords = []
        self.normals = []
        
        self.materials = {}
        self.face_groups = []
        
        self.debug = bool(debug)
        self.name = '3D Object'
        
        # Display list id for quick rendering
        self.display_list_id = None
    
    def __repr__(self):
        return '<3D Model>'
    
    def add_vertex(self, x, y, z):
        "Add a new vertex at x, y, z. Returns new vertex's index."
        idx = len(self.vertices)
        self.vertices.append((x, y, z))
        return idx
    
    def add_tex_coord(self, x, y):
        "Add a new tex coordinate at x, y. Returns new coordinate's index."
        idx = len(self.tex_coords)
        self.tex_coords.append((x, y))
        return idx
    
    def add_normal(self, x, y, z):
        "Add a new normals at x, y, z. Returns new normals's index."
        idx = len(self.normals)
        self.normals.append((x, y, z))
        return idx
    
    def add_material(self, name):
        "Add a new material with <name> to list of materials."
        material = Material(name)
        self.materials[material.name] = material
    
    def add_face_group(self, name, indices):
        pass
    
    def process_textures(self, texture_path):
        "Process Textures from materials for OpenGL."
        if self.debug:
            print('Processing textures...')
        
        # Read all the textures used in the model
        for matname in self.materials:
            material = self.materials[matname]
            if self.debug:
                print(f'Processing material {matname}...')
            if material.texture_filename is None:
                texture_data = None
                width, height = (0, 0)
                
                if self.debug:
                    print(f'Material {matname} has no texture.')
                continue
            else:
                full_texture_filename = os.path.join(texture_path, material.texture_filename)
                
                texture_surface = pygame.image.load(full_texture_filename)
                texture_surface.lock()
##                texture_data = pygame.image.tostring(texture_surface, 'RGB', True)
                texture_data = pygame.image.tostring(texture_surface, 'RGBA', True)
                
                width, height = texture_surface.get_size()
                del texture_surface
                
                if self.debug:
                    print('Texture loading done, creating and binding texture id')
            
            # Create and bind a texture id
            # Generate a texture id
            material.texture_id = glGenTextures(1)
            
             # Tell OpenGL we will be using this texture id for texture opperations
            glBindTexture(GL_TEXTURE_2D, material.texture_id)
            
            if _DO_MIP_MAPS:
                glTexParameteri( GL_TEXTURE_2D,
                                 GL_TEXTURE_MAG_FILTER,
                                 GL_LINEAR )
                glTexParameteri( GL_TEXTURE_2D,
                                 GL_TEXTURE_MIN_FILTER,
                                 GL_LINEAR_MIPMAP_LINEAR )
            else:
                glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
                glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
            
            # Tell OpenGL that data is aligned to byte boundries
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            
            glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
##            glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
            
            if self.debug:
                print('Texture id binding done.')
##                if _DO_MIP_MAPS:
##                    
##                else:
##                    print('Initialized localy, skipping mip maps or the shell will crash.')
            if _DO_MIP_MAPS:
                # Upload texture and build mip-maps
                #width, height = texture_surface.get_rect().size
                if self.debug:
                    print('Generating mip maps...')
##                gluBuild2DMipmaps( GL_TEXTURE_2D,
##                                   3,#no alpha channel...
##                                   width,
##                                   height,
##                                   GL_RGB,#no alpha
##                                   GL_UNSIGNED_BYTE,
##                                   texture_data )
                gluBuild2DMipmaps( GL_TEXTURE_2D,
                                   4,# alpha channel...
                                   width,
                                   height,
                                   GL_RGBA,# alpha
                                   GL_UNSIGNED_BYTE,
                                   texture_data )
            else:
                if self.debug:
                    print('Uploading texture...')
                # Upload the image to OpenGL
                glTexImage2D( GL_TEXTURE_2D,
                              0,    # First mip-level
                              4,    # Bytes per pixel (4 if alpha channel)
                              width,
                              height,
                              0,    # Texture border boolian
                              GL_RGBA, #GL_RGBA if alpha channel
                              GL_UNSIGNED_BYTE,
                              texture_data )
        if self.debug:
            print('Done processing textures.')
    
    def vertexindices_to_facegroups(self, vertex_indices):
        "Convert a list of Vertex Indices into Face Groups"
        if self.debug:
            print('Converting Vertex Indices to Face Groups...')
        self.face_groups = []
        for i in range(len(vertex_indices)):#for each face
            vertex_indice = vertex_indices[i]
            face_group = FaceGroup('None')
            face_group.len = len(vertex_indice)
            if face_group.len == 4:
                for ii in range(len(vertex_indice)):
                    vi = vertex_indice[ii]
                    ti = 0
                    ni = i
                    face_group.indices.append([vi, ti, ni])
            elif face_group.len == 3:
                for ii in range(len(vertex_indice)):
                    vi = vertex_indice[ii]
                    ti = 0
                    ni = ii
                    face_group.indices.append([vi, ti, ni])
            self.face_groups.append(face_group)
        if self.debug:
            print('Done converting Vertex Indices to Face Groups.')
    
    def facegroups_to_indices(self):
        """Convert FaceGroups into a list of Vertex Indices, Texture Indices, and Normal Indices"""
        raise NotImplemented('This is not finnished. Do not use. It broken.')
        if self.debug:
            print('Converting Face Groups to Vertex Indices, Texture Indices, and Normal Indices...')
        vertex_indices = []
        texture_indices = []
        normal_indices = []
        for face_group in self.face_groups:
            vertex_indice = []
            texture_indice = []
            normal_indice = []
            #for ii in range(face_group.len):
            for vi, ti, ni in face_group.indices:
                # = indices
                vertex_indice.append(vi)
                texture_indice.append(ti)
                normal_indice.append(ni)
            vertex_indices.append(tuple(vertex_indice))
            texture_indices.append(tuple(texture_indice))
            normal_indices.append(tuple(normal_indice))
        if self.debug:
            print('Done converting Face Groups to Vertex Indices, Texture Indices, and Normal Indices.')
        return vertex_indices, texture_indices, normal_indices
    
    def draw(self):
        "Send commands to OpenGL to render self."
        for face_group in self.face_groups:
            textures = self.tex_coords and face_group.len >= 2
            normals = self.normals and face_group.len >= 1
            
            # Send the geometry to OpenGL
            geometryType = {1:GL_LINES, 3:GL_TRIANGLES, 4:GL_QUADS}[face_group.len]
            
            if face_group.len == 1 and face_group.type == 'point':
                geometryType = GL_POINTS
            
            material = self.materials[face_group.material_name]
            
            # Bind the texture for this face group
            glBindTexture(GL_TEXTURE_2D, material.texture_id)
            
            glBegin(geometryType)
            
            # Texture handling
            if textures:
                # Get the texture information for this material
                glMaterialfv(GL_FRONT, GL_AMBIENT,
                             (*material.ambient, material.transparency))
                glMaterialfv(GL_FRONT, GL_DIFFUSE,
                             (*material.diffuse, material.transparency))
                glMaterialfv(GL_FRONT, GL_SPECULAR,
                             (*material.specular, material.transparency))
                glMaterialfv(GL_FRONT, GL_SHININESS,
                             material.shininess)
            
            # Send commands to OpenGL
            for verticeIndex, textureIndex, normalIndex in face_group.indices:
                if textures:
                    glTexCoord2fv( self.tex_coords[textureIndex] )
                if normals:
                    glNormal3fv( self.normals[normalIndex] )
                glVertex3fv( self.vertices[verticeIndex] )
            glEnd()
    
    def generate_display_list(self):
        "If self.display_list_id is None, generate a new display list and set self.display_list_id to list id."
        if self.display_list_id is None:
            if self.debug:
                print('Generating display list...')
            # Generate a display list that renders the geometry
            self.display_list_id = glGenLists(1)
            glNewList(self.display_list_id, GL_COMPILE)
            self.draw()
            glEndList()
            if self.debug:
                print('Done generating display list.')
    
    def draw_quick(self):
        "Generate a display list if self.display_list_id is None, and either way call that display list."
        if self.display_list_id is None:
            if self.debug:
                print('draw_quick: No display list set, generating one.')
            self.generate_display_list()
        glCallList(self.display_list_id)
    
    def __del__(self):
        """Call self.free_resources."""
        # Called when the model is cleaned up by python
        self.free_resources()
    
    def free_resources(self):
        "Free resources; Delete gl lists, delete textures used, clear materials, and clear the geometry lists."
        # Delete the display list
        if self.display_list_id is not None:
            glDeleteLists(self.display_list_id, 1)
            self.display_list_id = None
        
        # Delete any textures we used
        for material_name in list(self.materials):
            material = self.materials[material_name]
            if material.texture_id is not None:
                glDeleteTextures(material.texture_id)
            del self.materials[material_name]
        
        # Clear all the materials
        self.materials.clear()
        
        # Clear the geometry lists
        del self.vertices[:]
        del self.tex_coords[:]
        del self.normals[:]
        del self.face_groups[:]
    pass

class ModelObj(Model):
    "Object for reading, writing, storing, and drawing wavefont 3D Models"
    def __repr__(self):
        return '<Wavefont Obj 3D Model>'
    
    def read_mtllib(self, mtl_filename):
        "Read a WaveFont Material Library file"
        if self.debug:
            print(f'Reading mtl file {mtl_filename}...')
        file_mtllib = open(mtl_filename, mode='r')
        
        cur_mat = None
        
        for line in file_mtllib:
            # Parse command and data from each line
            words = line.split()
            if len(words) > 0:
                command = words[0]
                data = words[1:]
            else:
                command = '#'
            
            if command[0] == '#': # Comment, so ignore line.
                continue
            
            elif command == 'newmtl': # New MaTeriaL
                self.add_material(data[0])
                cur_mat = data[0]
            
            elif not cur_mat is None:
                if command == 'map_Kd': # Diffuse 'K'olor texture map
                    self.materials[cur_mat].texture_filename = data[0]
                
                elif command == 'Ka': # Ambient Kolor
                    self.materials[cur_mat].ambient = [float(i) for i in (data[:3])]
                
                elif command == 'Kd': # Diffuse Kolor
                    self.materials[cur_mat].diffuse = [float(i) for i in (data[:3])]
                
                elif command == 'Ks': # Specular Kolor
                    self.materials[cur_mat].specular = [float(i) for i in (data[:3])]
                
                elif command in ('Ns', 'Ni'): # Shininess (specular exponent)
                    self.materials[cur_mat].shininess = float(data[0])
                
                elif command == 'd': # Dissolved; pretty much just alpha channel
                    self.materials[cur_mat].transparency = float(data[0])
                
                elif command == 'Tr': # Transparency; 1 - dissolved
                    self.materials[cur_mat].transparency = 1 - float(data[0])# makes it back into dissolved
                
                elif command == 'illum':
                    if self.debug:
                        print('"illum" commands are currently not supported.')
                
                elif self.debug:
                    print(f'Unrecognized material library command "{command}".')
            elif self.debug:
                print(f'No material defined/Unrecognized material lib command "{command}".')
        
        file_mtllib.close()
        
        if self.debug:
            print(f'Done reading mtl file {mtl_filename}.')
        model_path = os.path.split(mtl_filename)[0]
        self.process_textures(model_path)
    
    def read_obj(self, filename):
        "Read a WaveFont OBJ file"
        current_face_group = None
        
        if self.debug:
            print(f'Reading obj file {filename}...')
        file_in = open(filename, mode='r', encoding='utf-8')
        
        for line in file_in:
            # Parse command and data from each line
            words = line.split()
            command, data = words[0], words[1:]
            
            if command == '#':# Comment, so skip this line.
                continue
            
            if command == 'mtllib': # Material library
                # Find the file name of the texture
                model_path = os.path.split(filename)[0]
                mtllib_path = os.path.join(model_path, data[0])
                self.read_mtllib(mtllib_path)
            
            elif command == 'v': # geometric Vertex
                vertex = [float(i) for i in data[:3]]#lol :3
                self.add_vertex(*vertex)
            
            elif command == 'vp': # free-form geometry statement: Parameter space Vertice
                current_face_group.type = 'point'
                current_face_group.vertices.append([float(i) for i in data])#? idk if it work yet
                print('WARNING: Parameter Vertices are not tested!')
                #raise NotImplemented('Free-form Vertice Parameters are currently not implemented.')
                
            elif command == 'vt': # Texture coordinate
                tex_coord = [float(i) for i in data[:2]]
                self.add_tex_coord(*tex_coord)
            
            elif command == 'vn': # Normal
                normal = [float(i) for i in data[:3]]
                self.add_normal(*normal)
            
            elif command == 'usemtl': # Use MaTeriaL
                current_face_group = FaceGroup(data[0])
                self.face_groups.append(current_face_group)
            
            elif command == 'f': # Face
                current_face_group.len = len(data)
                #assert len(data) == 3, 'Sorry, only triangles are supported'
                assert len(data) in (3, 4), 'Sorry, only triangles and quads are supported currently'
                
                # Parse indices from triples
                for i in range(len(data)):
                    word = data[i]
                    if not '//' in word and word.count('/') == 2:#v/vt/vn
                        # We subtract one (s=1) because Obj indexes start at 1 instead of 0
                        indices = _amol((int(i) for i in word.split('/')), s=1)
                        current_face_group.type = 'tex'
                    # If it's non-textured
                    elif '//' in word and word.count('//') == 1:#v//vn
                        #Still subtracting 1
                        v, n = _amol((int(i) for i in word.split('//')), s=1)
                        indices = (v, 0, n)
                        current_face_group.type = 'notex'
                    # Add the indice we just found
                    current_face_group.indices.append(indices)
            
            elif command == 'l': # Line: polyline - v
                indices = (float(data[0]), 0, 0)
                current_face_group.type = 'line'
                current_face_group.indices.append(indices)
                print('WARNING: Lines are not tested!')
                #raise NotImplemented('Lines are currently not implemented.')
            
            elif command == 'o': # Object (name)?
                self.name = str(data[0])
            
            elif command == 's':
                if self.debug:
                    print('Smooth shading across polygons ("s") is not currently supported.')
            
            else:
                if self.debug:
                    print('Unrecognized command "%s".' % command)
        file_in.close()
        
        if self.debug:
            print('Done reading obj file.\n')
    
    def write_mtl(self, mtl_filename):
        "Write a WaveFont Material Library file"
        if self.debug:
            print('Writing mtl file %s' % mtl_filename)
        file_mtllib = open(mtl_filename, 'w')
        
        order = ('newmtl', 'Ns', 'Ka', 'Kd', 'Ks',  'Tr', 'map_Kd')
        
        if len(self.materials) == 0:
            lastname = None
            for face_group in self.face_groups:
                name = str(face_group.material_name)
                if lastname != name:
                    material = Material(n=name)
                    material.diffuse = (1, 1, 1)
                    material.ambient = (0.2, 0.2, 0.2)
                    material.specular = (0.2, 0.2, 0.2)
                    material.shininess = 10
                    self.materials[name] = material
                    lastname = str(name)
        
        if len(self.materials) >= 0:
            i = 0
            for name in self.materials.keys():
                material = self.materials[name]
                if name == '':
                    name = str(i)
                file_mtllib.write('newmtl '+material.name+'\n')
                for command in order:
                    data = ''
                    if command == 'map_Kd':# Diffuse 'K'olor texture map
                        if not material.texture_filename is None:
                            data = material.texture_filename
                    elif command == 'Ka':# Ambient Kolor
                        data = ' '.join([str(i) for i in material.ambient])
                    elif command == 'Kd': # Diffuse Kolor
                        data = ' '.join([str(i) for i in material.diffuse])
                    elif command == 'Ks': # Specular Kolor
                        data = ' '.join([str(i) for i in material.specular])
                    elif command == 'Ns': # Shininess (specular exponent)
                        temp = float(material.shininess)
                        if temp > 10:
                            temp /= 128
                        data = str(temp)
                    elif command == 'Tr': # Trancparency; 1 - dissolved
                        data = str(1-material.transparency)
                    if not data == '':
                        file_mtllib.write(command+' '+data+'\n')
                i += 1
        file_mtllib.close()
        if self.debug:
            print('Done writeing mtl file %s' % mtl_filename)
    
    def write_obj(self, filename):
        "Write a WaveFont OBJ file"
        vertices = self.vertices
        tex_coords = self.tex_coords
        normals = self.normals
        
        face_groups = self.face_groups
        
        if self.debug:
            print('Writeing obj file', filename)
        file_out = open(filename, mode='w', encoding='utf-8')
        
        order = ('mtllib', 'v', 'vn', 'vt', 'f')
        
        for command in order:
            data = []
            
            if command == 'mtllib':
                # Find the file name of the texture
                path = os.path.split(filename)
                model_path = path[0]
                mtlname = path[1].split('.')[0]+'.mtl'
                mtllib_path = os.path.join(model_path, mtlname)
                self.write_mtl(mtllib_path)
                data.append(mtlname)
            
            elif command == 'v':
                for vertice in vertices:
                    data.append(' '.join((str(i) for i in vertice)))
            
            elif command == 'vn':
                for normal in normals:
                    data.append(' '.join((str(i) for i in normal)))
            
            elif command == 'vt':
                for tex in tex_coords:
                    data.append(' '.join((str(i) for i in tex)))
            
            elif command == 'f':
                lastmtl = None
                for face_group in face_groups:
                    mtlname = str(face_group.material_name)
                    if mtlname != lastmtl:
                        file_out.write('usemtl '+mtlname+'\n')
                        lastmtl = mtlname
                    textures = face_group.len >= 2 and self.tex_coords
                    indices = []
                    for vi, ti, ni in face_group.indices:
                        if not textures:
                            temp = f'{vi+1}//{ni+1}'
                        else:
                            temp = f'{vi+1}/{ti+1}/{ni+1}'
                        indices.append(temp)
                    assert len(indices) % 3 == 0, f'Indices length is {len(indices)}, not equaly divisable by three!'
                    for i in range(int(len(indices)//3)):
                        data.append(' '.join(indices[i*3:(i+1)*3]))
            if not data == []:
                for i in data:
                    file_out.write(command+' '+i+'\n')
        file_out.close()
        if self.debug:
            print('Done writing obj file '+filename)
    pass

if __name__ == '__main__':
    _DO_MIP_MAPS = False
##    
##    walrus = ModelObj(True)
##    walrus.read_obj('models/walrus/walrus.obj')
##    walrus.write_obj('models/walrus/walrus2.obj')
##    del walrus
##    walrus = ModelObj(True)
##    walrus.read_obj('models/walrus/walrus2.obj')
##    
##    cat = Model3D(True)
##    vertices = [ (0, 0, 1),
##                 (1, 0, 1),
##                 (1, 1, 1),
##                 (0, 1, 1),
##                 (0, 0, 0),
##                 (1, 0, 0),
##                 (1, 1, 0),
##                 (0, 1, 0) ]
##
##    normals = [ (0, 0, +1),  # front
##                (0, 0, -1),  # Back
##                (+1, 0, 0),  # right
##                (-1, 0, 0),  # left
##                (0, +1, 0),  # top
##                (0, -1, 0) ] # bottom
##
##    vertex_indices = [ (0, 1, 2, 3),  # front
##                       (4, 5, 6, 7),  # back
##                       (1, 5, 6, 2),  # right
##                       (0, 4, 7, 3),  # left
##                       (3, 2, 6, 7),  # top
##                       (0, 1, 5, 4) ] # bottom
##    cat.vertexindices_to_facegroups(vertex_indices)
##    cat.normals = normals
##    cat.vertices = vertices

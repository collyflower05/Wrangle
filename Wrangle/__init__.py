########################################
# Title: Wrangle source code
# Author: Colleen ("collyflower05")
# Date: 2020
# Version: 0.0.1
# License: MIT
########################################

from pathlib import Path
import numpy

# Barebones mesh class
class Mesh:
    # Geometry
    vertices = []
    uvs = []
    normals = []
    faces = []

    # Returns list of each face's averaged normals
    def get_face_normals(self):
        # Initialize normal list
        normals = []
        
        # For every face
        for fc in self.faces:
            # Initialize average buffer array
            avg = numpy.array([0.0, 0.0, 0.0])

            # For each vertex in face, add its normal to the buffer
            for vd in fc:
                avg += self.normals[vd[2]]
            
            # Average buffer and push to normals list
            avg = avg/len(fc)
            normals.append(avg.tolist())
        
        # Return final list of averaged face normals
        return normals

    # Returns list of each face's vertex positions
    def get_face_vertices(self):
        # Initialize normal list
        vertices = []
        
        # For every face
        for fc in self.faces:
            # Initialize vertex buffer list
            face = []

            # For each vertex in face, add its position to the buffer
            for vd in fc:
                face.append(self.vertices[vd[0]])

            vertices.append(face)
        
        # Return final list of each face's vertices
        return vertices

# Open mesh from file
def open_mesh(filename):
    # Open file for reading and split lines into a list
    mesh = Mesh()
    f = open(filename, "r")
    lines = f.readlines()

    # For every line in .obj
    for i, l in enumerate(lines):
        # If line isn't comment
        if(l[0] != "#"):
            # Split line into tokens
            tok = l.split(" ")

            # Insufficient arguments
            if(len(tok) < 2):
                print("Import Error: Line "+str(i)+" - Insufficient data.")
                return None

            # Vertices: "v x y z"
            elif(tok[0] == "v"):
                mesh.vertices.append([float(tok[1]), float(tok[2]), float(tok[3])])

            # Vertex texture coords (UVs): "vt u v"
            elif(tok[0] == "vt"):   
                mesh.uvs.append([float(tok[1]), float(tok[2])])

            # Vertex normals: "vn i j k"
            elif(tok[0] == "vn"):   
                mesh.normals.append([float(tok[1]), float(tok[2]), float(tok[3])])

            # Faces: "f {v/t/n}"
            elif(tok[0] == "f"):
                # Faces may have multiple vertices, so we make a buffer to store them
                # before submitting them to the final face list.
                face = []

                # For every "v/t/n" section, separate the values and append to buffer
                for vd in tok[1:]:
                    ids = vd.split("/")
                    face.append([int(ids[0])-1, int(ids[1])-1, int(ids[2])-1])
                
                # Submit final face data to face list
                mesh.faces.append(face)

    # Close file and return built mesh
    f.close()
    return mesh

# Save mesh to file
def save_mesh(mesh, filename, filetype="obj"):
    # Open file for writing
    f = open(filename, "w")

    # For .obj files
    if(filetype=="obj"):
        # Initialize output buffer
        lines = []

        # Vertices: "v x y z"
        for v in mesh.vertices:
            lines += "v "+str(v[0])+" "+str(v[1])+" "+str(v[2])+"\n"

        # Vertex texture coords (UVs): "vt u v"
        for vt in mesh.uvs:
            lines += "vt "+str(vt[0])+" "+str(vt[1])+"\n"

        # Vertex normals: "vn i j k"
        for vn in mesh.normals:
            lines += "vn "+str(vn[0])+" "+str(vn[1])+" "+str(vn[2])+"\n"

        # Faces: "f {v/t/n}"
        for fc in mesh.faces:
            lines += "f"
            # For every vertex in face
            for vd in fc:
                lines += " "+str(vd[0]+1)+"/"+str(vd[1]+1)+"/"+str(vd[2]+1)
            lines += "\n"

        # Write output buffer to file
        f.writelines(lines)

    # For ASCII (plaintext) .stl files    
    elif(filetype=="stl_ascii"):
        # Initialize output buffer and start STL solid section
        lines = []
        lines.append("solid "+Path(filename).stem+"\n")

        # Get face normals for facets
        face_normals = mesh.get_face_normals()
        face_vertices = mesh.get_face_vertices()

        # For every face
        for i, fc in enumerate(mesh.faces):
            lines += "\tfacet normal "+str(face_normals[i][0])+" "+str(face_normals[i][1])+" "+str(face_normals[i][2])+"\n"
            lines += "\t\touter loop\n"

            for v in face_vertices[i]:
                lines += "\t\t\tvertex "+str(v[0])+" "+str(v[1])+" "+str(v[2])+"\n"

            lines += "\t\tendloop\n"
            lines += "\tendfacet\n"

        # End STL solid section and write lines
        lines.append("endsolid "+Path(filename).stem+"\n")
        f.writelines(lines)

    # Close file
    f.close()
import Wrangle

# Load original
myMesh = Wrangle.open_mesh("sphere_tris.obj")

# Save as STL
Wrangle.save_mesh(myMesh, "out.stl", filetype="stl_ascii")
import os,sys

# Add the lib/ directory to sys.path to make it all the bundled libraries importable
LIB_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),"lib")
if LIB_PATH not in sys.path:
	sys.path.insert(0,LIB_PATH)

bl_info ={
	"name": "assetfetch-blender",
	"description":"AssetFetch for Blender",
	"author":"ambientCG / Lennart Demes",
	"version":(0,1),
	"blender":(4,0,0),
	"location": "View3D",
	"category": "3D View"
}

def register():

	from .property import register
	property.register()

	from .operator import register
	operator.register()

	from .ui import register
	ui.register()
	
def unregister():
	
	from .ui import unregister
	ui.unregister()

	from .operator import unregister
	operator.unregister()

	from .property import unregister
	property.unregister()

	
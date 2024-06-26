"""This is the main module of the "AssetFetch For Blender" addon.
It houses the main register() and unregister() functions for the addon along with required metadata.
See also: https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html#bringing-it-all-together
"""

import os, sys
import bpy

print("Loading AssetFetch for Blender v0.2.0")

# Add the lib/ directory to sys.path to make it all the bundled libraries importable.
# The addon is distributed with all its required python libraries in the /lib subdirectory.
# This has turned out to be the most reliable since the final python environment of the user (inside Blender) does not need to have pip.
# Check the readme.md for instructions on how to download the dependencies using pip.
LIB_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib")
if LIB_PATH not in sys.path:
	sys.path.insert(0, LIB_PATH)

# The SCHEMA path points to the directory containing the JSON-Schema required for validating all incoming responses.
# Like with the libraries, instructions for filling the json-schema directory for development can be found in readme.md
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "json-schema")

# This variable is used for the "Preferences" (bookmarks/settings) definition.
# Normally, it is common practice to use __name__ in the preferences class to tell Blender under which name the preferences should be stored.
# But because we don't define the preferences here in this init file we instead pipe the name over to properties/preferences.py using this variable.
# During development the name may therefore simply be "src" but in a proper installation it will be the name of the subdirectory in the Blender addons directory.
ADDON_NAME = __name__

# Standard variable with metadata required for all Blender addons.
bl_info = {
	"name": "assetfetch-blender",
	"description": "AssetFetch for Blender",
	"author": "ambientCG / Lennart Demes",
	"version": (0, 2),
	"blender": (4, 0, 0),
	"location": "View3D",
	"category": "3D View"
}

def register():
	"""The main registration function for the entire addon.
	It calls the other registration functions to load all modules.
	"""
	from .property import register
	property.register()

	from .operator import register
	operator.register()

	from .ui import register
	ui.register()

	from .util.ui_images import reset_image_cache
	reset_image_cache()


def unregister():
	"""Main unregistration function for the entire addon (used during uninstallation)."""

	from .util.ui_images import reset_image_cache
	reset_image_cache()

	from .ui import unregister
	ui.unregister()

	from .operator import unregister
	operator.unregister()

	from .property import unregister
	property.unregister()

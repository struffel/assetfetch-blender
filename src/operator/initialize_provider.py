import bpy
from ..util import http

class AF_OP_InitializeProvider(bpy.types.Operator):
	"""Performs the initialization request to the provider and sets the provider settings, if requested."""
	
	bl_idname = "af.initialize_provider"
	bl_label = "Initialize Provider"
	bl_options = {"REGISTER"}

	#url: StringProperty(name="URL")

	def draw(self,context):
		pass
		#layout = self.layout
		#layout.prop(self,'radius')

	def execute(self,context):
		af  = bpy.context.window_manager.af

		# Reset existing connection_state
		if 'current_provider_initialization' in af:
			af['current_provider_initialization'].clear()

		if 'current_connection_state' in af:
			af['current_connection_state'].clear()

		if 'current_asset_list' in af:
			af['current_asset_list'].clear()

		if 'current_asset_list_index' in af:
			af['current_asset_list_index'] = 0

		if 'current_implementation_list' in af:
			af['current_implementation_list'].clear()

		if 'current_implementation_list_index' in af:
			af['current_implementation_list_index'] = 0


		# Contact initialization endpoint and get the response
		query = http.AF_HttpQuery(uri=af.current_init_url,method="get")
		response : http.AF_HttpResponse = query.execute()

		# Set the provider id
		if "id" in response.parsed:
			af.current_provider_initialization.name = response.parsed['id']
		else:
			raise Exception("No provider ID.")

		# Get the provider text (title and description)
		if "text" in response.parsed['data']:
			af.current_provider_initialization.text.configure(response.parsed['data']['text'])
			
		# Provider configuration
		af.current_provider_initialization.provider_configuration.headers.clear()
		if "provider_configuration" in response.parsed['data']:

			provider_config = response.parsed['data']['provider_configuration']

			# Headers
			if len(provider_config['headers']) > 0:
				af.current_connection_state.state = "awaiting_input"
				for header_info in provider_config['headers']:
					current_header = af.current_provider_initialization.provider_configuration.headers.add()
					current_header.configure(header_info)
			else:
				af.current_connection_state.state = "connected"

			# Status endpoint
			af.current_provider_initialization.provider_configuration.connection_status_query.configure(provider_config['connection_status_query'])
		else:
			# No configuration required...
			af.current_connection_state.state = "connected"

		# asset_list_query
		if "asset_list_query" in response.parsed['data']:
			af.current_provider_initialization.asset_list_query.configure(response.parsed['data']['asset_list_query'])
			af.current_asset_list.already_queried = False
		else:
			raise Exception("No Asset List Query!")
		
		return {'FINISHED'}
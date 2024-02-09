from vbuild import render
from fastapi.responses import HTMLResponse
class FrantFront:
	layouts={}
	snippets={}
	def __init__(self,main_app,paths:dict):
		"""
		paths={"app":settings.BASE_DIR}
		"""
		self.main_app=main_app
		self.paths={}

	def load_layouts(self,module,app=None):
		for layout in os.listdir(BASE_DIR+f"/{module}/views/layouts/"):
			if layout.endswith(".ff"):
				with open(layout) as f:
					layout_txt=f.read()
					head=f"<script>FF.load_layouts('{self.host}{layout}')<script>"
					layout_compiled=render(layout_txt)

					self.layouts[(module,layout)]=layout_compiled

	def load_views(self,module,app=None):
		for layout in os.listdir(BASE_DIR+f"/{module}/views/views/"):
			if layout.endswith(".ff"):
				with open(layout) as f:
					layout_txt=f.read()
					head=f"""\
<script >
FF.load_snippets('{self.host}{layout}')
FF.current_#deberia tener la url del archivo
</script>"""
					layout_compiled=render(layout_txt)
					footer="<script>FF.run()</script>"
					self.layouts[(module,layout)]=layout_compiled

	def load_snippets(self,module,app=None):
		for layout in os.listdir(BASE_DIR+f"/{module}/views/snippets/"):
			if layout.endswith(".ff"):
				with open(layout) as f:
					layout_txt=f.read()
					head=f"<script>FF.load_snippets('{self.host}{layout}')<script>"
					f
					layout_compiled=render(layout_txt)
					self.snippets[(module,layout)]=layout_compiled

	def build(bp):
		"""
		/layouts/{module}/<path>
		/snippets/{module}/<path>

		#-----------------------
		/{app}/layouts/{module}/<path>
		/{app}/snippets/{module}/<path>
		"""
		for (module,layout) in self.layouts:
			if "." in module:
				app,module=module.split(".")
				bp.get(f"/{app}/layouts/{module}/{layout[:-len('.ff')]}")(lambda: HTMLResponse(self.layouts[(module,layout)]))
			else:
				bp.get(f"/layouts/{module}/{layout[:-len('.ff')]}")(lambda: HTMLResponse(self.layouts[(module,layout)]))

		for (module,snippet) in self.snippets:
			if "." in module:
				app,module=module.split(".")
				bp.get(f"/{app}/snippets/{module}/{layout[:-len('.ff')]}")(lambda: HTMLResponse(self.snippets[(module,snippet)]))
			else:
				bp.get(f"/snippets/{module}/{layout[:-len('.ff')]}")(lambda: HTMLResponse(self.snippets[(module,snippet)]))



if __name__=="__main__":
	from fastapi import FastApi
	fastapi=FastApi()
	fastapi.build(fastapi)
	app=FrantFront()
	app.load_layouts()
	app.load_components()


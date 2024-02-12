from vbuild import render
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

class FrantFront:
	layouts={}
	snippets={}
	def __init__(self,main_app,paths:dict={}):
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
	def __call__(self):
		return self.main_app

from fastapi import FastAPI
app=FastAPI()
origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/data-json")
def template():
	return {
		"title":"Hola mundo",
		"rows":[
			{"pagina":1},
			{"pagina":2},
			{"pagina":3},
			{"pagina":4},
			{"pagina":5},
		],
		}


@app.get("/version-json")
def template():
	return {
		"title":"Hola mundo",
		"version":"0.0.1"
		}


#fastapi.build(fastapi)
app=FrantFront(app)
#app.load_layouts()
#app.load_components()


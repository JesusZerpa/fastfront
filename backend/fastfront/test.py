from fastfront import FastFront
from fastapi import FastAPI
app = FastAPI()
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
def template2():
	return {
		"title":"Hola mundo",
		"version":"0.0.1"
		}
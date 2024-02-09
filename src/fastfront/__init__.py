from uuid import v4 as uuidv4 

def reemplazarValores(cadena, datos):
	patron = RegExp(r"{{\s*(.*?)\s*}}","g");
	def reemplazo(match, p1):
		clave = p1.trim();
		if datos[clave]!=undefined:
			return datos[clave]
		else:
			return  match;
	resultado = cadena["replace"](patron, reemplazo);
	
	return resultado;


templates={}
components={}
parser=DOMParser()

def handler_attr():
	for attr in doc:
		if attr.startswith("f-"):

			match attr:
				case "f-value":
					node=getattr(doc,attr)

				case "f-model":
					node=getattr(doc,attr)
			

		elif attr.startswith("@"):
			
			match attr:
				case "@click":
					node=getattr(doc,attr)
					def click():
						for elem in store:
							setattr(this,elem,store[elem])
						eval(node)

					doc.addEventListener("click",click)
				case "@change":
					node=getattr(doc,attr)
					def click():
						for elem in store:
							setattr(this,elem,store[elem])
						eval(node)

					doc.addEventListener("change",click)
				case "@focus":
					node=getattr(doc,attr)
					def click():
						for elem in store:
							setattr(this,elem,store[elem])
						eval(node)

					doc.addEventListener("focus",click)
				case "@mouseover":
					node=getattr(doc,attr)
					def click():
						for elem in store:
							setattr(this,elem,store[elem])
						eval(node)

					doc.addEventListener("mouseover",click)
				case "@mousemose":
					node=getattr(doc,attr)
					def click():
						for elem in store:
							setattr(this,elem,store[elem])
						eval(node)

					doc.addEventListener("mousemove",click)
				case "@keyup":
					node=getattr(doc,attr)
					def click():
						for elem in store:
							setattr(this,elem,store[elem])
						eval(node)

					doc.addEventListener("keyup",click)
					
				case "@keydown":
					node=getattr(doc,attr)
					def click():
						for elem in store:
							setattr(this,elem,store[elem])
						eval(node)

					doc.addEventListener("keydown",click)


def build_context(that,data,nodo,template,padre={}):
	context={}
	data=Object.assign({},data)
	
	def builder(name,data):
		def get_func():
			return data[name]
		def set_func(value):
			
			if padre[name]!=undefined:
				padre[name]=value
			data[name]=value
			that.update(context,nodo,template)

		Object.defineProperty(context,name,{
			"get":get_func,
			"set":set_func
			})
	
	for name in data:
		builder(name,data)

		
	return context
		

class Snippet:
	def __init__(self):
		FF.snippets_instances[self.__class__.__name__]=self

class View:
	def __init__(self):
		FF.views_instances[self.__class__.__name__]=self
"""
def travese(component,datos):
	if len(component.children)==0:
		if "{{" in component.innerText and "}}" in component.innerText:
			cadena=reemplazarValores(component.innerText, datos)

			component.innerText=cadena
			
	else:
		for comp in component.children:
			travese(comp,datos)

"""
def travese(that,nodo,context,localdata={}):

	for i,attr in nodo.attributes.items():
		if attr.name.startswith("@"):
			value=attr.value
			nodo.addEventListener(attr.name[1:],
				lambda event: eval("(function(){self=this; "+value+" })").call(context) )

	componente=nodo.getAttribute("f-component")
	
	

	if componente:
		componente=eval("(function(){self=this; return "+componente+" })").call(context)
		template=that.components[componente].template


		data=that.components[componente].data

		for attr in nodo.attributes.values():
			attr.name
			attr.value
			if attr.name.startswith("f-model:"):
				field=attr.name.split(":")

				data[field[1]]=eval("(function(){self=this; return "+attr.value+" })").call(context)

		
		context2=build_context(that,data,nodo,template)
		that.update(context2,nodo,template)
		

	if len(nodo.children)==0:
		nodo.innerHTML=reemplazarValores(nodo.innerHTML,localdata)
	for comp in nodo.children:
		travese(that,comp,context,localdata)


class Component:
	def __init__(self):
		print("Heredando componente2")

class Component2(Component):
	pass
			

class App:
	View=View
	Snippet=Snippet
	stores={}
	dependencies=[]
	components={}
	elifs=[]
	elses=[]
	shows=[]
	render_uuid=uuidv4()
	mounted=[]
	templates={}
	def __init__(self):
		templates=localStorage.getItem("FF-templates")
		snippets=localStorage.getItem("FF-snippets")

		if templates:
			templates=JSON.parse(templates)

		if snippets:
			snippets=JSON.parse(snippets)
		that=self
	async def beforeCreate(self):
		dependencies=[]
		scripts=document.head.querySelectorAll("script[type='text/fastfront']")
		for script in scripts:
			dependencies.append(fetch(script.src))

		dependencies=await Promise.all(dependencies)

		# ===============================================
		# =           Lectura de Dependencias           =
		#                 (nivel documento)
		# ===============================================
		
		for k,dependency in enumerate(dependencies):
			body=await dependency.text()
			doc=parser.parseFromString(body,"text/html")
			
			module=scripts[k].getAttribute("module")
			setup=doc.scripts[0]
			script=doc.scripts[1]
			template=doc.head.children[1]

			data=template.getAttribute("f-data")
			if data:
				data=JSON.parse(data)
			else:
				data={}
			self.components[template.getAttribute("name")]={
				"module":module,
				"data":data,
				"template":template.outerHTML,
				"setup":setup,
				"script":script
			}
		
		
		# ======  End of Lectura de Dependencias  =======
		# ==============================================
		# =           Lectura de templates           =
		#                 (nivel del documento)
		# ==============================================
		for template in document.querySelectorAll("template"):
			
			data=template.getAttribute("f-data")
			if data:
				data=JSON.parse(data)
			else:
				data={}

			self.components[template.getAttribute("name")]={
				"template":template.outerHTML,
				"data":data
			}

		
		# ======  End of Lectura de Componentes  =======
		
		for componente in document.querySelectorAll("template[name]"):
			console.log("ooooooooooo",componente)
			data=componente.getAttribute("f-data")
			if data:
				data=JSON.parse(data)
			else:
				data={}
			self.components[name]={
				"template":componente.outerHTML,
				"data":data,
				}

		self.render_uuid=uuidv4()

		name=self.container.getAttribute("component")
		
		console.log("jjjjjjjj",self.components)
		

		if name in self.components:
			template=self.components[name].template
			data=data
		
		context=build_context(self,data,self.container,template)
		console.log("zzzzzzzz",data["titulo"])
		self.update(context,self.container,template)



	def mount(self):
		
		pass
		

			


	def update(self,context,nodo,template,field=None,value=None):
		"""
		Vuelve a Dibujar los componentes, cargando el contexto actual en lugar
		de resetear el contexto
		"""
		console.log("kkkkkk",context)
		doc=document.createElement("div")
		doc.innerHTML=template
		console.log("$$$$$$$$$$$$$$$$$$$ ",template)
		nodo.innerHTML=reemplazarValores(doc.children[0].innerHTML,context)
		

		ftarget=nodo.getAttribute("f-target")
		ftrigger=nodo.getAttribute("f-tigger")
		
		fget=nodo.getAttribute("f-get")

		fpost=nodo.getAttribute("f-post")
		fpatch=nodo.getAttribute("f-patch")
		fput=nodo.getAttribute("f-put")
		fdelete=nodo.getAttribute("f-delete")
		fswap=nodo.getAttribute("f-swap")#reemplasar elemento, transicion
		fload=nodo.getAttribute("f-load")#spinner

		if ftrigger==undefined:
			async def trigger():
				if fget!=undefined:
					req=await fetch(fget)
					data=await req.json()
				elif fpost!=undefined:
					
					req=await fetch(fget,{"method":"POST",
						"body":JSON.stringify({
							nodo.getAttribute("name"):nodo.getAttribute("value")
							})
						})

				elif fpatch!=undefined:
					pass
				elif fput!=undefined:
					pass
				elif fdelete!=undefined:
					pass

			nodo.addEventListener("click",trigger)
			
		ifs=nodo.querySelectorAll("[f-if]")
		for node in ifs:
			#conditions[k]=[]
			
			node_if=node.getAttribute("f-if")
			node_elif_before=None
			
			valor=eval("(function(){"+f"self=this; return {node_if}"+"})").call(context)
			
			condition=valor==True
			node2=node.nextSibling
			if node2 :
				if not valor:
					node.remove()
				while node2!=undefined:
					
					if node2.__proto__.constructor.name!="Text":

						node_elif=node2.getAttribute("f-elif")

						node_else=node2.getAttribute("f-else")


						if node_elif!=None:
							valor=eval("(function(){"+f"self=this; return {node_elif}"+"})").call(self.context)
							
							if not condition and valor==True:

								condition=valor

							else:
								node_before=node2
								node2=node2.nextSibling
								node_before.remove()
						
						if condition and node_else!=None:
							node2.remove()
							
						if node_else!=None:
							break

					node2=node2.nextSibling
						
		ffors=nodo.querySelectorAll("[f-for]")				
		for node in ffors:
			fnode=node.children[0]
			forval=node.getAttribute("f-for")
			elem,iterable=forval.split(" in ")
			iterador=eval("(function(){"+f"self=this; return {iterable}"+"})").call(context)



			if "(" in elem and ")" in elem:
				k,v=elem.strip()[1:-1].split(",") 
			
			for k2,valor in enumerate(iterador):
				

				clon=fnode.cloneNode(True)
				data={k:k2,v:valor}
				travese(self,clon,context,data)


				node.appendChild(clon)
			fnode.remove()


		for node2 in nodo.children:
			travese(self,node2,context)


		# =====================================================
		# =           Renderizado de subcomponentes           =
		# =====================================================
		"""
		console.log("QQQQQQQQQQQ",node)
		for sub in doc.querySelectorAll("[f-component]"):

			subcomp=self.components[sub.getAttribute("f-component")]
			data=subcomp.getAttribute("f-data")
			store=subcomp.getAttribute("f-store")
			console.log("PPPPPPPPPPPPPPPP")
			context={}
			if data:
				data=JSON.parse(data)
			else:
				data={}
			console.log("zzzzzzzzz")
			context2=build_context(self,data,sub,subcomp.template,context)
			self.update(context2,sub,subcomp.template)
		"""
		
		# ======  End of Renderizado de subcomponentes  =======
		
		

		
		"""
		for node in FF.ifs[name]:
			code=node.getAttribute("f-if")
			cond=eval("(function(){ "+f"self=this; return {code} "+"})").call(context)
			if not cond:
				node.innerHTML=""
				node2=node.nextSibling
				if node2 in FF.elses[name]:
					node2.children.append(node2.contenido)
		"""
		
	
	def process(self,nodo,context):
		"""
		procesa los nodos
		"""
		for name, componente in self.components[name].items():
			# ===============================================
			# =           Parseamos el componente           =
			# ===============================================
			
			doc=document.createElement("div")
			
			

			data=componente.getAttribute("f-data")
			store=componente.getAttribute("f-store")

			if data:
				data=JSON.parse(data)
			else:
				data={}
			

			name=doc.getAttribute("f-name")
			self.stores[name]=data
			context={}
			if store:
				self.store[store]=context
			for d in data:
				
				def get_func():
		
					return data[d]
				def set_func(value):
					
					that.update(context,doc,d,value)

				Object.defineProperty(context,d,{
					"get":get_func,
					"set":set_func
					})
			

			init=componente.getAttribute("f-init")
			if init:
				eval("\(function\(\){"+f"self=this; {init}"+"}\)").call(self.context)

			
			
			# ======  End of Parseamos el componente  =======
			
						

			self.process(componente,data)
			

			

				
			console.log("ppppp",node)

			ffors=componente.querySelectorAll("[f-for]")
			for node in ffors:
				forval=node.getAttribute("f-for")
				elem,iterable=forval.split(" in ")
				if "(" in elem and ")" in elem:
					k,v=elem.strip()[1:-1].split(",") 
					console.log("ttttttt ",k,v)
					"""
					for node2 in forval.children:
						n1,n2=self.context[iterable].items()
						travese(node2,{*self.context,*{k:v,n1:n2}})
						self.process(node2,{*self.context,*{k:v,n1:n2}})

					for n1,n2 in self.context[iterable].items():



						k,v=eval("for (let "+elem+" of "+iterable+"){ }").call(self.context)
					"""


			self.lifs[name]=ifs

			elifs=componente.querySelectorAll("[f-elif]")
			self.elifs[name]=elifs

			elses=componente.querySelectorAll("[f-else]")
			self.elses[name]=elses

		#Procesado para renderizar las variables embebidas
		
		

					




	def save(self):
		localStorage.setItem("FF-templates", JSON.stringify(templates));
		localStorage.setItem("FF-snippets", JSON.stringify(snippets));

	async def get_layout(self,url,app=None):
		if not app:
			req=await fetch(window.BACKEND+f"/layouts/{url}")
			templates[url]=req.text()
		else:
			req=await fetch(window.BACKEND+f"/{app}/layouts/{url}")
			templates[url]=req.text()

	async def get_snippet(self,url,app=None):
		if not app:
			req=await fetch(window.BACKEND+f"/snippets/{url}")
			snippets[url]=req.text()
		else:
			req=await fetch(window.BACKEND+f"/{app}/snippets/{url}")
			snippets[url]=req.text()
	def load_view(self,view):
		self.view=view

	def render(self,view):
		document.outerHTML=self.views[view]

	async def run(self,selector):
		self.container=document.querySelector(selector)
		componente=self.container.getAttribute("component")

		for name,comp in self.components.items():
			if name==componente:
				node.children=[]
				node.children.append(self.process(comp.template.innerHTML,comp.script))
				break

		await self.beforeCreate()
		await self.mount()
		return ""

FF=App()

FF.stores={}
FF.elifs=[]
FF.elses=[]
FF.shows=[]

Component2()
from uuid import v4 as uuidv4 

def reemplazarValores(cadena, datos):
    #patron = RegExp(r"{{\s*(.*?)\s*}}","g");
    patron = RegExp(r"\{\{\s*([^{}.]+(?:\.[^{}.]+)*)\s*\}\}","g");
    
    def reemplazo(match, p1):
        clave = p1.trim();
        
        if "." in clave:
            response=datos

            for elem in clave.split("."):
                if response[elem]!=undefined:
                    response=response[elem]
        else:
            response=datos[clave]

        if response!=undefined:
            
            if typeof(response)=="object":
                response=JSON.stringify(response)

            return response
        else:
            return  "";

    resultado = cadena["replace"](patron, reemplazo);
    
    return resultado;


templates={}
components={}
parser=DOMParser()

#def handler_attr():
#    for attr in doc:
#        if attr.startswith("f-"):
#
#            match attr:
#                case "f-value":
#                    node=getattr(doc,attr)
#
#                case "f-model":
#                    node=getattr(doc,attr)
#            
#
#        elif attr.startswith("@"):
#            
#            match attr:
#                case "@click":
#                    node=getattr(doc,attr)
#                    def click():
#                        for elem in store:
#                            setattr(this,elem,store[elem])
#                        eval(node)
#
#                    doc.addEventListener("click",click)
#                case "@change":
#                    node=getattr(doc,attr)
#                    def click():
#                        for elem in store:
#                            setattr(this,elem,store[elem])
#                        eval(node)
#
#                    doc.addEventListener("change",click)
#                case "@focus":
#                    node=getattr(doc,attr)
#                    def click():
#                        for elem in store:
#                            setattr(this,elem,store[elem])
#                        eval(node)
#
#                    doc.addEventListener("focus",click)
#                case "@mouseover":
#                    node=getattr(doc,attr)
#                    def click():
#                        for elem in store:
#                            setattr(this,elem,store[elem])
#                        eval(node)
#
#                    doc.addEventListener("mouseover",click)
#                case "@mousemose":
#                    node=getattr(doc,attr)
#                    def click():
#                        for elem in store:
#                            setattr(this,elem,store[elem])
#                        eval(node)
#
#                    doc.addEventListener("mousemove",click)
#                case "@keyup":
#                    node=getattr(doc,attr)
#                    def click():
#                        for elem in store:
#                            setattr(this,elem,store[elem])
#                        eval(node)
#
#                    doc.addEventListener("keyup",click)
#                    
#                case "@keydown":
#                    node=getattr(doc,attr)
#                    def click():
#                        for elem in store:
#                            setattr(this,elem,store[elem])
#                        eval(node)
#
#                    doc.addEventListener("keydown",click)


def build_context(that,data,nodo,template,padre={}):
    context={"__data__":None}
    data2=Object.assign({"$refs":that.refs,"$stores":that.stores},data)
    context={"__data__":data2}
    def builder(name,data):
        def get_func():
            return data2[name]
        def set_func(value):
            that.render_idx=nodo.idx
            data[name]=value
            data2[name]=value
            if padre[name]!=undefined:
                padre[name]=value
                return 
            that.update(context,nodo,template)

        Object.defineProperty(context,name,{
            "get":get_func,
            "set":set_func
            })
    
    for name in data2:
        builder(name,data)

        
    return context
        

class Snippet:
    def __init__(self):
        FF.snippets_instances[self.__class__.__name__]=self

class View:
    def __init__(self):
        FF.views_instances[self.__class__.__name__]=self


def process_api(that,nodo,context,doc=None):
    if doc:
        tpl=doc
    else:
        tpl=nodo

    fhead=tpl.getAttribute("f-head")
    ftarget=tpl.getAttribute("f-target")
    ftrigger=tpl.getAttribute("f-trigger")

    fswap=tpl.getAttribute("f-swap")#reemplasar elemento, transicion
    fload=tpl.getAttribute("f-load")#spinner

    form_type=None

    for attr in tpl.attributes.values():
        
        
        if attr.name.startswith("f-post") or attr.name.startswith("f-get") \
            or attr.name.startswith("f-put") or attr.name.startswith("f-patch") or attr.name.startswith("f-delete"):
            
            value=eval("(function(){"+f" self=this;return {attr.value} "+"})").call(context)

            if attr.name.endswith(".formdata"):
                form_type="multipart/form-data"
            elif attr.name.endswith(".urlencoded"):
                form_type="application/x-www-form-urlencoded"
            elif attr.name.endswith(".plain"):
                form_type="text/plain"
            else:
                form_type="application/json"
        if value!=undefined:
            if attr.name.startswith("f-post"):
                fpost=value
            elif attr.name.startswith("f-get"):
                fget=value
            elif attr.name.startswith("f-error"):
                ferror=value
            elif attr.name.startswith("f-success"):
                fsuccess=value
            elif attr.name.startswith("f-put"):
                fput=value
            elif attr.name.startswith("f-patch"):
                fpatch=value
            elif attr.name.startswith("f-delete"):
                fdelete=value
        if attr.name.startswith(":"):
            cadena=""
            for name in localdata:
                cadena+=f"let {name}={JSON.stringify(localdata[name])};"
            _str=lambda x:str(x)





    if fhead:
        fhead=context[fhead]
    else:
        fhead={
            "Content-Type":"application/json",
            }
    if form_type:
        fhead["Content-Type"]=form_type

    async def trigger(event):
        data={}
        if event!=undefined:
            event.preventDefault()
            event.stopPropagation()

            if tpl.getAttribute("f-form"):
                fform=tpl.getAttribute("f-form")
                
                if fform!=undefined and event.target!=undefined:
                    data=that.process_form(context,event.target)
            elif tpl.getAttribute("f-payload"):
                fpayload=tpl.getAttribute("f-payload")
                
                if fpayload!=undefined and event.target!=undefined:
                    data=that.process_payload(context,event.target)


        if fget!=undefined:
            try:
                req=await fetch(fget)
                data=await req.json()
            except Exception as e:
                if ferror:
                    eval("(function(){"+f" self=this;{ferror} "+"})").call(context)
            if fsuccess:
                eval("(function(data){"+f" self=this;{fsuccess} "+"})").call(context,data)

            fkey=None
            for attr in tpl.attributes.values():
                attr.name
                attr.value
                if attr.name.startswith(":"):
                    cadena=""
                    for name in localdata:
                        cadena+=f"let {name}={JSON.stringify(localdata[name])};"
                    _str=lambda x:str(x)

                if attr.name.startswith("f-key"):
                    fkey=attr.value

                if attr.name.startswith("f-response:"):
                    field=attr.name.split(":")
                    response=eval(f"({attr.value})").call(None,data,fkey)

                    context[field[1]]=response
                    
                    if field[2]:
                        response=eval(f"({attr.value})").call(None,data,fkey)#lambda data:data.rows
                        
                        context[field[2]]=response
                        


        elif fpost!=undefined:
            
            if fhead["Content-Type"]=="application/json":
                req=await fetch(fpost,{"method":"POST",
                    "head":fhead,
                    "body":JSON.stringify(data)
                    })
            else:
                req=await fetch(fpost,{"method":"POST",
                    "head":fhead,
                    "body":data
                    })


            data=await req.json()
            fkey=None
            
            for attr in tpl.attributes.values():
                attr.name
                attr.value

                if attr.name.startswith(":"):
                    cadena=""
                    for name in localdata:
                        cadena+=f"let {name}={JSON.stringify(localdata[name])};"
                    _str=lambda x:str(x)

                if attr.name.startswith("f-key"):
                    fkey=attr.value

                if attr.name.startswith("f-reponse:"):
                    field=attr.name.split(":")
                    
                    response=eval(f"({attr.value})(data,fkey)").call(None,data,fkey)#lambda data:data.rows
                    
                    context[field[1]]=response
                    


        elif fpatch!=undefined:
            
            if fhead["Content-Type"]=="application/json":
                req=await fetch(fpost,{"method":"PATCH",
                    "head":fhead,
                    "body":JSON.stringify(data)
                    })
            else:
                req=await fetch(fpost,{"method":"PATCH",
                    "head":fhead,
                    "body":data
                    })

            data=await req.json()
            fkey=None
            
            for attr in tpl.attributes.values():
                attr.name
                attr.value

                if attr.name.startswith(":"):
                    cadena=""
                    for name in localdata:
                        cadena+=f"let {name}={JSON.stringify(localdata[name])};"
                    _str=lambda x:str(x)

                if attr.name.startswith("f-key"):
                    fkey=attr.value

                if attr.name.startswith("f-reponse:"):
                    field=attr.name.split(":")
                    context[field[1]]=eval(f"({attr.value})(data,fkey)").call(None,data,fkey)#lambda data:data.rows
                    
        elif fput!=undefined:
            
            if fhead["Content-Type"]=="application/json":
                req=await fetch(fpost,{"method":"PUT",
                    "head":fhead,
                    "body":JSON.stringify(data)
                    })
            else:
                req=await fetch(fpost,{"method":"PUT",
                    "head":fhead,
                    "body":data
                    })
            data=await req.json()
            fkey=None
            
            for attr in tpl.attributes.values():
                attr.name
                attr.value

                if attr.name.startswith(":"):
                    cadena=""
                    for name in localdata:
                        cadena+=f"let {name}={JSON.stringify(localdata[name])};"
                    _str=lambda x:str(x)

                if attr.name.startswith("f-key"):
                    fkey=attr.value

                if attr.name.startswith("f-reponse:"):
                    field=attr.name.split(":")
                    context[field[1]]=eval(f"({attr.value})(data,fkey)").call(None,data,fkey)#lambda data:data.rows
                    
        elif fdelete!=undefined:
            
            if fhead["Content-Type"]=="application/json":
                req=await fetch(fpost,{"method":"DELETE",
                    "head":fhead,
                    "body":JSON.stringify(data)
                    })
            else:
                req=await fetch(fpost,{"method":"DELETE",
                    "head":fhead,
                    "body":data
                    })
            data=await req.json()
            fkey=None
            
            for attr in tpl.attributes.values():
                attr.name
                attr.value

                if attr.name.startswith(":"):
                    cadena=""
                    for name in localdata:
                        cadena+=f"let {name}={JSON.stringify(localdata[name])};"
                    _str=lambda x:str(x)

                if attr.name.startswith("f-key"):
                    fkey=attr.value

                if attr.name.startswith("f-reponse:"):
                    field=attr.name.split(":")
                    context[field[1]]=eval(f"({attr.value})(data,fkey)").call(None,data,fkey)#lambda data:data.rows
    
    if ftrigger!=undefined :
        
        ftrigger=eval("(function(){"+f" self=this;return {ftrigger} "+"})").call(context)
        

    if ftrigger==undefined :
        if nodo.triggered==undefined and any([bool(fget),bool(fput),bool(fdelete),bool(fpost)]):
            
            tpl.addEventListener("click",trigger)
            tpl.triggered=True
    elif ftrigger=="init":
        if nodo.inited==undefined:
            trigger()
            nodo.inited=True
        
        
    pass

def travese(that,nodo,context,idx,localdata={},lock=False):
    if nodo.__proto__.constructor.name=="Text":

        nodo.nodeValue=reemplazarValores(nodo.nodeValue,Object.assign({},context["__data__"],localdata))

        return nodo
    if nodo.__proto__.constructor.name=="Comment":
        return 
    if not lock:
        for attr in nodo.attributes:
            attr= nodo.attributes[attr]

            if attr.name.startswith("@"):
                value=attr.value
               
                """
                nodo.addEventListener(attr.name[1:],
                    lambda event: eval("(function(){self=this; "+value+" })").call(context) )
                """
                def evento(event):
                    return eval("(function(){self=this; "+value+" })").call(context) 
                nodo.addEventListener(attr.name[1:],evento)
    

    componente=nodo.getAttribute("f-component")
    ref=nodo.getAttribute("f-ref")
    store=nodo.getAttribute("f-store")
    specials={}
    
    if ref:
        eval("(function(nodo){ this['$refs']["+ref+"]= nodo; })").call(context,nodo)

    if store:
        eval("(function(){ if (this['$store']["+store+"]==undefined){this['$store']["+store+"]={}}else{ throw Error('No se puede crear store ya '"+store+"' ya existia')} })").call(context)
    
    binds={}
    for attr in nodo.attributes.values():
        
        if attr.name.startswith(":"):
            cadena=""
            for name in localdata:
                cadena+=f"let {name}={JSON.stringify(localdata[name])};"

            _str=lambda x:str(x)
            
         
            binds[attr.name[1:]]=eval("(function(str){self=this; "+cadena+" return "+attr.value+" })").call(context,_str)
            
    for name in binds:
        nodo.removeAttribute(":"+name)
        valor=binds[name]
        accept=[]
        if valor:

            if typeof(valor)=="string":
                accept.append(valor)
            elif typeof(valor)=="number":
                accept.append(valor)
            elif Array.isArray(valor):
                for elem in valor:
                    if typeof(elem)=="object":

                        for atrr in elem:
                            if elem[attr]:
                                accept.append(attr)
                    
                    else:
                        accept.append(elem)

                valor=" ".join(accept)
            nodo.setAttribute(name,valor)
        

    if len(nodo.children)==0:
        process_api(that,nodo,context)
        
        nodo.innerHTML=reemplazarValores(nodo.innerHTML,Object.assign({},context["__data__"],localdata))
        
        binds={}
        for attr in nodo.attributes.values():
            if attr.name.startswith("f-model"):
                
                value=eval("(function(){self=this; return "+attr.value+" })").call(context)
                nodo.value=value
                def wrapper(attr):
        
                    def change(event):
        
                        eval("(function(valor){self=this; "+attr.value+"=valor; })").call(context,event.target.value)
                    return change
                change=wrapper(attr)
        
                nodo.addEventListener("change",change)


            if attr.name.startswith("f-text"):#
                text=eval("(function(){self=this; return "+attr.value+" })").call(context)
                nodo.innerText=text
                pass
            
            if attr.name=="f-value":
                text=eval("(function(){self=this; return "+attr.value+" })").call(context)
                data[text]=node.innerText
                

            if attr.name.startswith("f-html"):

                text=eval("(function(){self=this; return "+attr.value+" })").call(context)
                nodo.innerHTML=text
                pass
            if attr.name=="f-show":

                _boolean=eval("(function(){self=this; return "+attr.value+" })").call(context)
                if _boolean:
                    nodo.style.opacity = "1";
                else:
                    nodo.style.opacity = "0";
            if attr.name=="f-transition":
                eval("(function(){self=this; return "+attr.value+" })").call(context)
                nodo.style.opacity = "0";


        for name in binds:
            nodo.removeAttribute(":"+name)
            nodo.setAttribute(name,binds[name])

            

            

            

    

    


    # ==============================================
    # =           Section Subcomponentes           =
    # ==============================================
    
    if componente:
        padre={}
        componente=eval("(function(){self=this; return "+componente+" })").call(context)
        template=that.components[componente].template

        if nodo.idx==undefined :
            that.generate_render_id()
            nodo.idx=that.render_idx
        

            if not that.is_mounted:
                
                data=that.components[componente].data
                data=Object.assign({},data)
                that.states.append(data)

        if not that.is_mounted:
            pass#hay que ver porque me lo esta pintando 2 veces, al crear, pienso que es por el travese en el ffor y el child
        else:
            data=that.states[nodo.idx]

        binds={}
        for attr in nodo.attributes.values():
            attr.name
            attr.value
            if attr.name.startswith(":"):
                cadena=""
                for name in localdata:
                    cadena+=f"let {name}={JSON.stringify(localdata[name])};"

                _str=lambda x:str(x)

             
                binds[attr.name[1:]]=eval("(function(str){self=this; "+cadena+" return "+attr.value+" })").call(context,_str)

            if attr.name.startswith("f-model:"):
                field=attr.name.split(":")
                #actualiza la data local del componente al la del contexto superior, esto es asi porque,
                #gracias al f-model, el superior se debio haber modificado y el componente debe heredar su valor

                data[field[1]]=eval("(function(){self=this; return "+attr.value+" })").call(context)
                padre=context

            if attr.name.startswith("f-action:"):
                field=attr.name.split(":")
                if data[field[1]]:
                    eval("("+attr.value+")").call(context)
            if attr.name=="f-show":

                _boolean=eval("(function(){self=this; return "+attr.value+" })").call(context)
                if _boolean:
                    nodo.style.opacity = "1";
                else:
                    nodo.style.opacity = "0";
            if attr.name=="f-transition":
                eval("(function(){self=this; return "+attr.value+" })").call(context)
                nodo.style.opacity = "0";

        for name in binds:
            
            nodo.removeAttribute(":"+name)

            valor=binds[name]
            if valor:
                accept=[]
                console.log("fffffff",valor)
                if typeof(valor)=="string":
                    accept.append(valor)
                else:
                    for elem in valor:
                        if typeof(elem)=="object":
                            for atrr in elem:
                                if elem[attr]:
                                    accept.append(attr)
                        
                        else:
                            console.log(">>>>>>>>>>>>>>>><",elem)
                            accept.extend(elem)
                valor=" ".join(accept)

                nodo.setAttribute(name,valor)
            

            



        
            

        

        context2=build_context(that,data,nodo,template,padre)
        
        that.update(context2,nodo,template) 
    else:
        for comp in nodo.childNodes:
            console.log("eeeeeeee",comp.innerHTML)
            if comp.idx==undefined:# Esto evita que se atravisen nodos ya procesados en un travese anterior
                
                travese(that,comp,context,idx,localdata,lock)
        
    # ======  End of Section Subcomponentes  =======
    
    
        

    


class Component:
    def __init__(self):
        print("Heredando componente2")

class Component2(Component):
    pass
            

class App:
    View=View
    Snippet=Snippet
    stores={}
    refs={}
    dependencies=[]
    components={}
    elifs=[]
    elses=[]
    shows=[]
    
    mounted=[]
    templates={}
    states=[]
    render_idx=0
    is_mounted=False
    is_created=False
    is_updating=False
    def __init__(self):
        templates=localStorage.getItem("FF-templates")
        snippets=localStorage.getItem("FF-snippets")

        if templates:
            templates=JSON.parse(templates)

        if snippets:
            snippets=JSON.parse(snippets)
        that=self
    async def build_component(self,dependency):
        body=await dependency.text()
        doc=parser.parseFromString(body,"text/html")
        setup="export default []"
        script=""
        if doc.scripts:
            setup=doc.scripts[0].innerText
            script=doc.scripts[1].innerText
        
        __default__=None
        eval(setup.replace("export default","__default__="))
        
        if __default__:
            for elem in __default__:
                await self.import_component(elem)
             
        for child in doc.head.children:
            if child.tagName=="TEMPLATE":
                template=child
        data=template.getAttribute("f-data")
        if data:
            data=JSON.parse(data)
        else:
            data={}
        return template,data,setup,script

    async def import_component(self,importer):
        scripts=[]
        dependencies=[]
        dependencies2=[]
        names=[]
        if typeof(importer)=="object":
            for name, url in importer.items():
                names.append(name)
                dependencies2.append(fetch(url))     

        else:
            scripts.append(importer)
            
        for script in scripts:
            dependencies.append(fetch(script.src))
        
        dependencies=await Promise.all(dependencies)

        for k,dependency in enumerate(dependencies):
            template,data,setup,script=await self.build_component(dependency)

            self.components[template.getAttribute("name")]={
                #"module":module,
                "data":data,
                "template":template.outerHTML,
                "setup":setup,
                "script":script
            }

        dependencies2=await Promise.all(dependencies2)

        for k,dependency in enumerate(dependencies2):
            console.log("ZZZZZZZZZZZZZ",dependency)
            template,data,setup,script=await self.build_component(dependency)

            self.components[names[k]]={
                #"module":module,
                "data":data,
                "template":template.outerHTML,
                "setup":setup,
                "script":script
            }


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
            template,data,setup,script=await self.build_component(dependency)
            self.components[template.getAttribute("name")]={
                #"module":module,
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
        

        if name in self.components:
            template=self.components[name].template
            data=data
        
        data=Object.assign({},data)
        self.states.append(data)
        self.container.idx=0
        


        context=build_context(self,data,self.container,template)

        self.update(context,self.container,template)
        self.is_created=True

    def generate_render_id(self):
        self.render_idx+=1
        return self.render_idx



    def mount(self):
        self.is_mounted=True

    def process_form(self,context,nodo):
        form=nodo.getAttribute("f-form")
        form=eval("(function(){"+f"let self=this;let $stores=self.$stores; return {form}"+"})").call(context)
        data={}
        def travese_nodo(nodo):
            if len(nodo.children)==0:
                model=nodo.getAttribute("f-model")
                if model!=undefined:
                    name=nodo.getAttribute("name")
                    
                    value=eval("(function(){"+f"let self=this;let $stores=self.$stores; return {model}"+"})").call(context)
                    data[name]=value

            for nodo2 in nodo.children:
                travese_nodo(nodo2)
        
        travese_nodo(self.refs[form])
        return data

    def process_payload(self,context,nodo):
        form=nodo.getAttribute("f-payload")
        return eval("(function(){"+f"let self=this;let $stores=self.$stores; return {form}"+"})").call(context)
        
        

            


    def update(self,context,nodo,template,field=None,value=None):
        """
        Vuelve a Dibujar los componentes, cargando el contexto actual en lugar
        de resetear el contexto
        """
        that=self

        if nodo.idx==undefined:
            nodo.idx=1
            self.render_idx=1
            idx=1
        else:
            idx=self.render_idx

        doc=document.createElement("div")
        doc.innerHTML=template

        
        tpl=doc.children[0]
        finit=doc.children[0].getAttribute("f-init")
        nodo.innerHTML=tpl.innerHTML
        process_api(that,nodo,context,doc.children[0])


        if finit:
            eval("(function(){"+f"let self=this;let $stores=self.$stores; return {finit}"+"})").call(context)
        

        
        ifs=nodo.querySelectorAll("[f-if]")
        for node in ifs:
            #conditions[k]=[]
            
            node_if=node.getAttribute("f-if")
            node_elif_before=None
            
            valor=eval("(function(){"+f"let self=this;let $stores=self.$stores; return {node_if}"+"})").call(context)
            
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
                            valor=eval("(function(){"+f"let self=this;let $stores=self.$stores; return {node_elif}"+"})").call(self.context)
                            
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
            fnode=node
            forval=node.getAttribute("f-for")
            elem,iterable=forval.split(" in ")
            iterador=eval("(function(){"+f"self=this; return {iterable}"+"})").call(context)

            if "(" in elem and ")" in elem:
                k,v=elem.strip()[1:-1].split(",") 
            
                for k2,valor in enumerate(iterador):
                    

                    clon=fnode.cloneNode(True)
                    data={k:k2,v:valor}
                    travese(self,clon,context,idx,data,True)
                    clon.removeAttribute("f-for")
                    node.parentNode.appendChild(clon)

            else:
                v=elem.strip() 
            
                for valor in iterador:
                    

                    clon=fnode.cloneNode(True)
                    data={v:valor}
                    travese(self,clon,context,idx,data,True)
                    clon.removeAttribute("f-for")
                    node.parentNode.appendChild(clon)
            fnode.remove()

        for node2 in nodo.children:
            travese(self,node2,context,idx,{},False)

                    




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

        await self.beforeCreate()
        await self.mount()
        return ""

FF=App()

FF.stores={}
FF.elifs=[]
FF.elses=[]
FF.shows=[]

window.FF=FF
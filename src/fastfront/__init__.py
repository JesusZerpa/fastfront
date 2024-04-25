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
            if typeof(response)=="object":
                 response=JSON.stringify(response)

            return response
        elif "[" in clave:
            clave=clave.strip()
            result=eval("const { "+",".join(datos.keys())+" } = datos; "+clave)
            return result
        else:

            response=datos[clave]


        if response!=undefined:
            if typeof(response)=="object":
                #Esto se hace para evitar la recursividad al hacer
                # stringify por el attributo $store

                response2=Object.assign({},response)

                del response2["$stores"]
                
                response2=JSON.stringify(response2)
                return response2


        else:
            return  "";
    resultado = cadena["replace"](patron, reemplazo);
    
    return resultado;


TEMPLATES={}
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
            console.log("pppppppppppppp",name)
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


def process_api(that,nodo,context,localdata,doc=None):
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
def process_for(that,node,context,idx,localdata,lock):
    """
    El problema de usar self ajuro es que para los condicionales no se sabe cual 
    """
    fnode=node
    forval=node.getAttribute("f-for")
    elem,iterable=forval.split(" in ")
    
    cadena=""




    try:
        if iterable in context.__data__:
            iterador=context[iterable]

        elif iterable in localdata:
            iterador=localdata[iterable]

        elif "." in iterable:
            valor=None
            for n in iterable.split("."):    
                if valor is None:
                    if n in context.__data__:
                        valor=context.__data__[n]
                    elif n in localdata:
                        valor=localdata[n]
                else:
                    valor=valor[n]

            iterador=valor

    except Exception as e:
        console.error(e)
        if "ReferenceError" in str(e):
            console.log(node.outerHTML)
            console.warn("Recordar que las variables de contextos se usan desde el objeto 'self' ejemplo: self.attributo")
    
    if "(" in elem and ")" in elem:
        k,v=elem.strip()[1:-1].split(",") 
        
        
        parent=node.parentNode
        nuevos=[]
        for k2,valor in enumerate(iterador):
            #localdata[v]=valor    
            clon=fnode.cloneNode(True)
            #lo quitamos antes de el travese para que el nodo se
            #procese con process_attr
            clon.removeAttribute("f-for")
            node.removeAttribute("f-for")

            data={k.strip():k2,v.strip():valor}
            data.update(localdata)
            #clon.removeAttribute("f-for")
            travese(that,clon,context,idx,data,lock)
            parent.insertBefore(clon,node)

        
            
        node.remove()
            


    else:
        v=elem.strip() 
    
        for valor in iterador:
            

            clon=fnode.cloneNode(True)
            clon.removeAttribute("f-for")
            data={v:valor}
            data.update(localdata)

            node.parentNode.insertBefore(clon,node)
            travese(that,clon,context,idx,data,lock)
            #clon.removeAttribute("f-for")
            #node.parentNode.appendChild(clon)
    fnode.remove()





def process_attr(that,nodo,context,idx,localdata,lock):
    #nodo,context,idx,data,localdata
    binds={}
     #deberia ser el contexto padre o algo asi ver mas tarde

    data=that.states[idx]
    #Atributos no componentes
    componente=nodo.getAttribute("f-component")
    

    for attr in dict(nodo.attributes).values():

        cadena=""

        for name in localdata:
                cadena+=f"let {name}=_localdata['{name}'];"
        for name in context.__data__:
            cadena+=f"let {name}=self.{name};"

        if attr.name.startswith(":"):
            
            _str=lambda x:str(x)
            

            binds[attr.name[1:]]=eval("(function(str,_localdata){let self=this; "+cadena+" return "+attr.value+" })").call(context,_str,localdata)

            
        if attr.name.startswith("f-action:"):
            field=attr.name.split(":")
            if data[field[1]]:
                eval("("+attr.value+")").call(context)
        if attr.name=="f-show":

            _boolean=eval("(function(_localdata){self=this; "+cadena+";return "+attr.value+" })").call(context,localdata)
            if _boolean:
                nodo.style.opacity = "1";
            else:
                nodo.style.opacity = "0";
        if attr.name=="f-transition":
            
            eval("(function(_localdata){self=this;"+cadena+"; return "+attr.value+" })").call(context,localdata)
            nodo.style.opacity = "0";
            
        if attr.name=="f-if":
            
            process_if(that,nodo,context,idx,localdata)
            pass
            
        
        if attr.name.startswith("f-model"):
            
            fields={}
            def build(context,value,name=None):

                
              
                def change(event):
                    """
                    los f-model in : solo son para nodos con f-component
                    """
                    
                    if event.target.getAttribute("type")=="checkbox":

                        if event.target.checked:
                            
                            if event.target._value:
                                context[value].append(event.target._value)

                        else:
                            if event.target._value:
                                context[value].remove(event.target._value)
                        
                    elif event.target.getAttribute("type")=="radio":
                        context[value]=event.target.value
                        
                    else:
                       
                        if event.target._value:
                            context[value]=event.target._value
                        else:
                            context[value]=event.target.value
                    
                return change
        
            result=eval("(function(_localdata){let self=this;"+cadena+" return "+attr.value+" })").call(
                context,localdata)
            #nodo.value

            change=build(context,attr.value,attr.name)
            
    
            nodo.addEventListener("change",change)
            
            #nodo.removeAttribute(attr.name)
    

    for name in binds:
        
        nodo.removeAttribute(":"+name)
        valor=binds[name]
        if valor:
            
            accept=[]
            if typeof(valor)=="string":
                accept.append(valor)
            elif typeof(valor)=="number":
                accept.append(valor)
            else:
                for elem in valor:

                    if typeof(elem)=="object":
                        for attr in elem:
                            if elem[attr]:
                                accept.append(attr)
                    elif typeof(elem)=="array":
                        accept.extend(elem)
                    else:
                        accept.append(elem)
            _valor=" ".join(accept)
            if name=="value":
                nodo._value=valor
            else:
                nodo.setAttribute(name,_valor)
                pass
    
    
    ref=nodo.getAttribute("f-ref")
    store=nodo.getAttribute("f-store")
    specials={}
    
    if ref:
        eval("(function(nodo){ this['$refs']["+ref+"]= nodo; })").call(context,nodo)

    if store:
        eval("(function(){ if (this['$store']["+store+"]==undefined){this['$store']["+store+"]={}}else{ throw Error('No se puede crear store ya '"+store+"' ya existia')} })").call(context)
    

        
            

        
    # ==============================================
    # =           Section Subcomponentes           =
    # ==============================================
    
    if componente:
        padre={}
        componente=eval("(function(){let self=this; return "+componente+" })").call(context)
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

        #Atributos que son componentes
        for attr in nodo.attributes.values():
            cadena=""
            for name in localdata:
                cadena+=f"let {name}=_localdata['{name}'];"
            for name in context.__data__:
                cadena+=f"let {name}=self.{name};"

            
            if attr.name.startswith("f-model:"):
                field=attr.name.split(":")
                #actualiza la data local del componente al la del contexto superior, esto es asi porque,
                #gracias al f-model, el superior se debio haber modificado y el componente debe heredar su valor
        
                result=eval("(function(){let self=this; "+cadena+";return "+attr.value+" })").call(context)
                
                data[field[1]]=result
                padre=context

            if attr.name.startswith("f-text") and not attr.name.startswith("f-text:"):#
                text=eval("(function(){let self=this;"+cadena+" ;return "+attr.value+" })").call(context)
                nodo.innerText=text
                pass
            
            if attr.name=="f-value" and not attr.name.startswith("f-value:"):
                text=eval("(function(){let self=this; "+caden+";return "+attr.value+" })").call(context)
                data[text]=node.innerText
                

            if attr.name.startswith("f-html") and not attr.name.startswith("f-html:"):

                text=eval("(function(){let self=this;"+cadena+" ;return "+attr.value+" })").call(context)
                nodo.innerHTML=text
                pass

        cadena=""
        context2=build_context(that,data,nodo,template,padre)
        #esto es para poder hacer live reload

        context2=build_context(that,data,nodo,template,padre)
        #esto es para poder hacer live reload

        that.nodes[nodo.idx]={"nodo":nodo,"componente":componente}
        that.update(context2,nodo,template) 
    else:
        
        for comp in nodo.childNodes:
            if comp.idx==undefined:# Esto evita que se atravisen nodos ya procesados en un travese anterior
                
                travese(that,comp,context,idx,localdata,lock)
        
        
    # ======  End of Section Subcomponentes  =======        



def process_if(that,node,context,idx,localdata):
    node_if=node.getAttribute("f-if")
    node_elif_before=None
    cadena=""
    for name in localdata:
        cadena+=f"let {name}=_localdata['{name}'];"
    for name in context.__data__:
        cadena+=f"let {name}=self.{name};"

    valor=eval("(function(_localdata){"+f"let self=this;"+cadena+f"return {node_if}"+"})").call(context,localdata)

    condition=valor==True
    node2=node.nextSibling
    if node2 :
        if not valor:
            node.remove()
            pass
        else:
            node.removeAttribute("f-if")
        
        
        
        while node2!=undefined:
            
            if node2.__proto__.constructor.name!="Text":

                node_elif=node2.hasAttribute("f-elif")

                node_else=node2.hasAttribute("f-else")
                
                if node_elif:
                    _elif=node2.getAttribute("f-elif")
                    valor=eval("(function(iterador){"+f"let self=this;let $stores=self.$stores; let {iterable}=iterador; console.log('bbbbbbb','{iterable}');return {_elif}"+"})").call(self.context,iterador)
    
                    if not condition and valor==True:

                        condition=valor
                    else:
                        node2.remove()    

                        
                elif condition and not node_else:#elif
                    node2.remove()
                    pass
                    
                elif condition and node_else:#else
                    
                    node2.remove()
                    pass

                if condition:
                    if node2.hasAttribute("f-if"):
                        node2.removeAttribute("f-if") 
                    if node2.hasAttribute("f-elif"):
                        node2.removeAttribute("f-elif")
                    if node2.hasAttribute("f-else"):
                        node2.removeAttribute("f-else") 
                
            if node_else:
                break

            node2=node2.nextSibling
        

def travese(that,nodo,context,idx,localdata={},lock=False):
    
    if nodo.__proto__.constructor.name=="Text":
        
        nodo.nodeValue=reemplazarValores(nodo.nodeValue,
            Object.assign({},context["__data__"],localdata))
        return nodo
    if nodo.__proto__.constructor.name=="Comment":
        return 
    if not lock:
        cadena=""
        for name in localdata:
            cadena+=f"let {name}=_localdata['{name}'];"
        for name in context.__data__:
            cadena+=f"let {name}=self.{name};"

        for attr in nodo.attributes:
            attr= nodo.attributes[attr]
            if attr.name.startswith("@"):
                value=attr.value
                if "." in attr.name:
                    event=attr.name.split(".")[0][1:]
                    modifiers=attr.name.split(".")[1]
                    """
                    nodo.addEventListener(attr.name[1:],
                        lambda event: eval("(function(){self=this; "+value+" })").call(context) )
                    """
                    

                    def evento(event):
                        for elem in modifiers:
                            if elem=="stop":
                                event.stopPropagation()
                            elif elem=="prevent":
                                event.preventDefault()
                            elif elem=="caputre":
                                pass
                            elif elem=="once":
                                pass
                            elif elem=="passive":
                                pass
                            elif elem=="enter":
                                pass
                            elif elem=="tab":
                                pass
                            elif elem=="esc":
                                pass
                            elif elem=="space":
                                pass
                            elif elem=="up":
                                pass
                            elif elem=="down":
                                pass
                            elif elem=="left":
                                pass
                            elif elem=="right":
                                pass
                            elif elem=="middle":
                                pass
                            elif elem=="ctrl":
                                pass
                            elif elem=="alt":
                                pass
                            elif elem=="meta":
                                pass
                            elif elem=="exact":
                                pass


                        return eval("(function(event,_localdata){let self=this; "+cadena+" "+value+" })").call(context,event,localdata) 
                    nodo.addEventListener(attr.name[1:],evento)
                else:

                    """
                    nodo.addEventListener(attr.name[1:],
                        lambda event: eval("(function(){self=this; "+value+" })").call(context) )
                    """
                    console.log("hhhhhh")
                    def build(context,localdata):
                        def evento(event):
                            before_state={}
                            for n in context["__data__"]:
                                if not n.startswith("$"):
                                    before_state[n]=context["__data__"][n]
                            before_state=JSON.stringify(before_state)
                            eval("(function($event,_localdata){let self=this;"+cadena+"; console.log('llllll',$event);"+value+" })").call(context,event,localdata) 
                            for n in context["__data__"]:
                                if not n.startswith("$"):
                                    if before_state[n]!=JSON.stringify(context["__data__"][n]):
                                        console.log("kkkkk ",n,context["__data__"][n])
                                        context[n]=context["__data__"][n]
                        return evento
                    evento=build(context,localdata)
                    nodo.addEventListener(attr.name[1:],evento)
            if attr.name.startswith(":"):

                if attr.name==":value":
                    result=eval("(function(_localdata){let self=this;"+cadena+" ;"+attr.value+" })").call(context,localdata)
                    nodo._value=result



    if len(nodo.children)==0:
        process_api(that,nodo,context,localdata)
        
        nodo.innerHTML=reemplazarValores(nodo.innerHTML,Object.assign({},context["__data__"],localdata))
        
        binds={}

        if nodo.getAttribute("f-for"):
            # Procesado cuando no hay hijos
            
            process_for(that,nodo,context,idx,localdata,lock)
        else:
            
            process_attr(that,nodo,context,idx,localdata,lock)
    else:
        
        if nodo.getAttribute("f-for"):
            # Procesado cuando no hay hijos
            
            process_for(that,nodo,context,idx,localdata,lock)
        else:
            
            process_attr(that,nodo,context,idx,localdata,lock)
        """
        console.log("wwwwwwwwwwwwwww",localdata)
        for comp in nodo.childNodes:
            if comp.idx==undefined:# Esto evita que se atravisen nodos ya procesados en un travese anterior
                console.log("CCCCCCCCCCC ",comp,localdata,nodo)
                travese(that,comp,context,idx,localdata,lock)
        """

        
            

            

            

    

    


    

class App:
    View=View
    Snippet=Snippet
    
    
    
    render_idx=0
    is_mounted=False
    is_created=False
    is_updating=False
    def __init__(self,is_reload=False):
        self.nodes={}
        self.stores={}
        self.refs={}
        self.dependencies=[]
        self.components={}
        self.elifs=[]
        self.elses=[]
        self.shows=[]
        self.stores={}
        self.mounted=[]
        self.templates={}
        self.states=[]
        self.is_reload=is_reload


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

        data=data["replace"](RegExp(',([^,]*)$'),'$1');

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
            name=template.getAttribute("name")
            self.components[name]={
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
        if not self.is_reload:
            for template in document.querySelectorAll("template[name]"):
                name = template.getAttribute("name")
                data = template.getAttribute("f-data")
           
                if data:
                    data=eval("("+data+")")
                    
                else:
                    data={}

                self.components[name]={
                    "template":template.outerHTML,
                    "data":data
                }
        else:
            console.log(TEMPLATES)
            for template_name in TEMPLATES:
                
                template=TEMPLATES[template_name]
   
                data = template["data"]
      

                self.components[template_name]={
                    "template":template["template"],
                    "data":data
                }

        # ======  End of Lectura de Componentes  =======
        """
        for componente in document.querySelectorAll("template[name]"):
           
            data=componente.getAttribute("f-data")
            name=componente.getAttribute("name")
            if data:
                data=JSON.parse(data)
            else:
                data={}
            self.components[name]={
                "template":componente.outerHTML,
                "data":data,
                }
            console.log("PPPPPPPPP",data,name)
        """
        self.render_uuid=uuidv4()

        name=self.container.getAttribute("component")

        data2=self.container.getAttribute("f-data")
        if data2:
            data2=eval("("+data2+")")
            
        else:
            data2={}
        if name in self.components:

            template=self.components[name].template

            data=self.components[name].data

            
            data=Object.assign({},data,data2)
            
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
                    
                    value=eval("(function(){"+f"let self=this;let $stores=self.$stores;console.log('44444444444 ',{model}) return {model}"+"})").call(context)
                    data[name]=value
                nodo.removeAttribute("f-model")

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

        self.stores[idx]=context
        doc=document.createElement("div")
        doc.innerHTML=template

        
        tpl=doc.children[0]
        finit=doc.children[0].getAttribute("f-init")

        nodo.innerHTML=tpl.innerHTML
        localdata={}
        process_api(that,nodo,context,localdata,doc.children[0])


        if finit:
            eval("(function(){"+f"let self=this;let $stores=self.$stores; return {finit}"+"})").call(context)
        
        #travese(nodo)
        """
        ffors=nodo.querySelectorAll("[f-for]")              
        for node in ffors:
        """    

        
        """
        for node in ifs:
            #conditions[k]=[]
        """
        for node2 in nodo.children:
            travese(self,node2,context,idx,localdata,False)

                    




    def save(self):
        localStorage.setItem("FF-templates", JSON.stringify(templates));
        localStorage.setItem("FF-snippets", JSON.stringify(snippets));

    async def get_layout(self,url,app=None):
        if not app:
            req=await fetch(FF.BACKEND+f"/layouts/{url}")
            templates[url]=req.text()
        else:
            req=await fetch(FF.BACKEND+f"/{app}/layouts/{url}")
            templates[url]=req.text()

    async def get_snippet(self,url,app=None):
        if not app:
            req=await fetch(FF.BACKEND+f"/snippets/{url}")
            snippets[url]=req.text()
        else:
            req=await fetch(FF.BACKEND+f"/{app}/snippets/{url}")
            snippets[url]=req.text()

    def load_view(self,view):
        self.view=view

    def render(self,view):
        document.outerHTML=self.views[view]

    async def run(self,nodo):
        self.container=nodo
        componente=self.container.getAttribute("component")
        self.container.getAttribute("component")
        await self.beforeCreate()
        await self.mount()
FF={} 
FF.BACKEND=None
FF.apps={}
window.FF=FF
FF.signals={}
def on(name,callback):
    if name in FF.signals:
        console.log("vvvvvv ",name)
        FF.signals[name].append(callback)
    else:
        FF.signals[name]=[callback]
FF.on=on
def emit(name,params):
    console.log("mmmmm",FF.signals)
    if name in FF.signals:
        console.log("RRRRRRRR",name)
        for callback in FF.signals[name]:
            console.log("KKKKKKKKKKKKK",callback)
            callback(params)
FF.emit=emit

def main(is_reload=False):
    if window.FASTFRONT_DEVELOP:
        if window.FASTFRONT_SOCKET==undefined:
            window.FASTFRONT_SOCKET=io("/fastfront")
            FF.emit("init")

            def travese(nodo2,before):
                k=0
                for nodo in before.childNodes:

                    if nodo.nodeValue:
                        nodo.nodeValue=nodo2.childNodes[k].nodeValue
                    else:

                        if nodo2.childNodes[k]:

                            if nodo2.childNodes[k].innerHTML!=nodo.innerHTML \
                                and not nodo2.childNodes[k].hasAttribute("fastfront"):
                                #lo que estaba pasando es que los componentes con fastfront no los puedo atravezar
                                if len(nodo.childNodes)==0:
                                 
                                    nodo.innerHTML=nodo2.childNodes[k].innerHTML
                                    
                                elif nodo2.childNodes[k]!=undefined:
                                 
                                    travese(nodo2.childNodes[k],nodo)

                        else:
                            console.log("es posible que nodo este al nivel de nodo2 osea k no es valida")
                    k+=1


            def reload(data):
                doc = document.implementation.createHTMLDocument("New Document");
                doc=document.createDocumentFragment()
                doc2=document.createDocumentFragment()
                head = document.createElement('head')
                body = document.createElement('body')
                doc.appendChild(head)
                doc2.appendChild(body)
                i=data["content"].find("<head>")
                i2=data["content"].rfind("</head>")

                head.innerHTML=data["content"][i+len("<head>"):i2]
                i=data["content"].find("<body>")
                i2=data["content"].rfind("</body>")
                body.innerHTML=data["content"][i+len("<body>"):i2]

                for template in body.querySelectorAll("template[name]"):
                    name = template.getAttribute("name")
                    data = template.getAttribute("f-data")
               
                    if data:
                        data=eval("("+data+")")
                        
                    else:
                        data={}

                    TEMPLATES[name]={
                        "template":template.outerHTML,
                        "data":data
                    }

                travese(body,document.body)




                FF.reload()
                FF.emit("render")
                
                
                            
            window.FASTFRONT_SOCKET.on("fastfront-reload",reload)



    aplicaciones=[]
    before_render=document.body.outerHTML
    console.log("ZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
    for nodo in document.querySelectorAll("[fastfront]"):
        app=App(is_reload)
        FF.apps[nodo.idx]=app
        app.run(nodo)
        
FF.reload=lambda: main(True)
main()

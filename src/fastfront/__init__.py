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
                return response.toString()


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
    def builder(name,data,context):
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
        context["__data__"]["$set_"+name]=set_func

        Object.defineProperty(context,name,{
            "get":get_func,
            "set":set_func
            })
    
    for name in data2:
        builder(name,data,context)

        
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
    
    if  nodo.__proto__.constructor.name!="Text" and nodo.__proto__.constructor.name!="Comment":
        cadena=""

        for name in localdata:
            if "." not in name:
                cadena+=f"let {name}=_localdata['{name}'];"
        for name in context.__data__:
            cadena+=f"let {name}=self.{name};"

        fhead=nodo.getAttribute("f-head")
        ftarget=nodo.getAttribute("f-target")
        ftrigger=nodo.getAttribute("f-trigger")

        fswap=nodo.getAttribute("f-swap")#reemplasar elemento, transicion
        fload=nodo.getAttribute("f-load")#spinner
        
        fpost=None
        fget=None
        fput=None
        fdelete=None
        fpacth=None
        fresponse=None
        fresponse_name=None
        fsuccess=None
        ferror=None

        form_type=None
        value=None

        keys=["1","2"]
        attributes=dict(nodo.attributes).values()
        attributes2=dict(tpl.attributes).values()
  

        for k,attr in enumerate(attributes2):
            
            #console.log("hhhhhh",nodo.attributes[attr])
            if attr.name.startswith(":"):
                cadena=""
                for name in localdata:
                    if "." not in name:
                        cadena+=f"let {name}={JSON.stringify(localdata[name])};"
                _str=lambda x:str(x)

            if attr.name.startswith("f-key"):
                if attr.name in nodo.attributes:
                    fkey=nodo.attributes[attr.name].value
                else:
                    fkey=attr.value
            if attr.name.startswith("f-trigger"):
                if attr.name in dict(nodo.attributes):
                    ftrigger=nodo.attributes[attr.name].value
                else:
                    ftrigger=attr.value
            attr_name=None
            if attr.name.startswith("f-response"):
                if attr.name in dict(nodo.attributes):
                    fresponse=nodo.attributes[attr.name].value
                    fresponse_name=attr.name
                else:
                    
                    fresponse=attr.value
                    fresponse_name=attr.name

            if attr.name.startswith("f-post") or attr.name.startswith("f-get") \
                or attr.name.startswith("f-put") or attr.name.startswith("f-patch") or attr.name.startswith("f-delete"):
                
                attr_value=attr.value
                if typeof(attr_value)!="undefined":
                
                    
          
                    if nodo.hasAttribute(attr.name):
                        value=eval("(function(_localdata){"+f"let self=this; "+cadena+f" return {attr_value} "+"})").call(context,localdata)    
                    
                        if attr.name.endswith(".formdata"):
                            form_type="multipart/form-data"
                        elif attr.name.endswith(".urlencoded"):
                            form_type="application/x-www-form-urlencoded"
                        elif attr.name.endswith(".plain"):
                            form_type="text/plain"
                        else:
                            form_type="application/json"
                    elif doc:
                        attr_value=doc.getAttribute(attr.name)
                        value=eval("(function(_localdata){"+f"let self=this; "+cadena+f" return {attr_value} "+"})").call(context,localdata)
                       
                        if attr.name.endswith(".formdata"):
                            form_type="multipart/form-data"
                        elif attr.name.endswith(".urlencoded"):
                            form_type="application/x-www-form-urlencoded"
                        elif attr.name.endswith(".plain"):
                            form_type="text/plain"
                        else:
                            form_type="application/json"
              
                    if attr.name.startswith("f-post"):
                        fpost=value
                        pass
                    
                    elif attr.name.startswith("f-get"):
                        fget=value
                    elif attr.name.startswith("f-put"):
                        fput=value
                    elif attr.name.startswith("f-patch"):
                        fpatch=value
                    elif attr.name.startswith("f-delete"):
                        fdelete=value

            if attr.name.startswith("f-error"):
                ferror=attr.value
            if attr.name.startswith("f-success"):
        
                fsuccess=attr.value
            
 
            if attr.name.startswith(":"):
                cadena=""
                _str=lambda x:str(x)
                for name in localdata:
                    if "." not in name:
                        cadena+=f"let {name}={JSON.stringify(localdata[name])};"
                
        
            
        
        if fhead:
            fhead=context[fhead]
        else:
            fhead={
                "Content-Type":"application/json",
                "accept":"application/json"
                }
        if form_type:
            fhead["Content-Type"]=form_type
        
        async def trigger(event):
            data={}
            console.log("HHHHHHHHHHHHH")
            if event!=undefined:
                event.preventDefault()
                event.stopPropagation()

                if nodo.getAttribute("f-form"):
                    fform=nodo.getAttribute("f-form")
                    
                    if fform!=undefined and event.target!=undefined:
                        data=that.process_form(context,event.target)
                elif nodo.getAttribute("f-payload"):
                    fpayload=nodo.getAttribute("f-payload")
                    
                    if fpayload!=undefined and event.target!=undefined:
                        data=that.process_payload(context,event.target,localdata)


            if fget!=None:

                if fhead["Content-Type"]=="application/json":
                    req=await fetch(fget,{"method":"GET",
                        "headers":fhead,
                        
                        })
                else:
                    req=await fetch(fget,{"method":"GET",
                        "headers":fhead,
                        })


             

            elif fpost!=None:
                console.log("EEEEEEEEEEEEEE",{"method":"POST",
                        "headers":fhead,
                        "body":JSON.stringify(data)
                        }
                        )
                if fhead["Content-Type"]=="application/json":
                    req=await fetch(fpost,{"method":"POST",
                        "headers":fhead,
                        "body":JSON.stringify(data)
                        })
                else:
                    req=await fetch(fpost,{"method":"POST",
                        "headers":fhead,
                        "body":data
                        })


                

            elif fpatch!=undefined:
                
                if fhead["Content-Type"]=="application/json":
                    req=await fetch(fpatch,{"method":"PATCH",
                        "headers":fhead,
                        "body":JSON.stringify(data)
                        })
                else:
                    req=await fetch(fpatch,{"method":"PATCH",
                        "headers":fhead,
                        "body":data
                        })

                
            elif fput!=undefined:
                
                if fhead["Content-Type"]=="application/json":
                    req=await fetch(fput,{"method":"PUT",
                        "headers":fhead,
                        "body":JSON.stringify(data)
               })
                else:         
                    req=await fetch(fput,{"method":"PUT",
                        "headers":fhead,
                        "body":data
                        })
                data=await req.json()
                
               
            elif fdelete!=undefined:
                
                if fhead["Content-Type"]=="application/json":
                    req=await fetch(fdelete,{"method":"DELETE",
                        "headers":fhead,
                        "body":JSON.stringify(data)
                        })
                else:
                    req=await fetch(fdelete,{"method":"DELETE",
                        "headers":fhead,
                        "body":data
                        })

            if req.status>=200 and req.status<300: 
                data=await req.json()
                for attr in nodo.attributes.values():
                    
                    if attr.name.startswith("f-reponse:"):
                        field=attr.name.split(":")
                        console.log("ddddd ",f"({fresponse})")
                        context[field[1]]=eval(f"({fresponse})").call(None,data,fkey)#lambda data:data.rows
                console.log("$$$$$$$ ",fsuccess)
                if fresponse:
                    field=fresponse_name.split(":")
                    response=eval(f"({fresponse})").call(None,data,fkey)#lambda data:data.rows
                    console.log("wwwww ",response)
                    context[field[1]]=response
                    console.log("YYYYY ",context)
                if fsuccess:
                    console.log("WWWWWWW")
                    eval("(function(data,_localdata){"+f"let self=this;"+cadena+f" {fsuccess} "+"})").call(context,data,localdata)
                

            else:
                try:
                    data=await req.json()
                except:
                    response=await req.text()
                    console.error(response)

                if ferror:
                    eval("(function(_localdata){"+f"let self=this;"+cadena+f" {ferror} "+"})").call(context,localdata)

            fkey=None

        
        if typeof(ftrigger)!="undefined" :
  
            ftrigger=eval("(function(_localdata){"+f" let self=this;"+cadena+f" return {ftrigger} "+"})").call(context,localdata)

        if typeof(ftrigger)=="undefined" or ftrigger==None:
            
            if typeof(nodo.triggered)=="undefined" and any([bool(fget),bool(fput),bool(fdelete),bool(fpost)]):

                nodo.addEventListener("click",trigger)
                nodo.triggered=True
        if ftrigger=="init":
            if typeof(nodo.inited)=='undefined':
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
            travese(that,clon,context,idx,data,lock,)
            parent.insertBefore(clon,node)
        
        if parent:
            parent._for=True

        
            
        node.remove()
            


    else:
        v=elem.strip() 
        l=[]
        for valor in iterador:
            

            clon=fnode.cloneNode(True)
            clon.removeAttribute("f-for")
            data={v:valor}
            data.update(localdata)
            if node.parentNode:
                node.parentNode.insertBefore(clon,node)
            l.append([clon,data])
            
            #clon.removeAttribute("f-for")
            #node.parentNode.appendChild(clon)
        condition={"condition":False}
        for item in l:
            travese(that,item[0],context,idx,item[1],lock,condition)
        if node.parentNode:
            node.parentNode._for=True
    fnode.remove()





def process_attr(that,nodo,context,idx,localdata,lock,condition={}):
    #nodo,context,idx,data,localdata
    binds={}
     #deberia ser el contexto padre o algo asi ver mas tarde

    data=that.states[idx]
    #Atributos no componentes
    componente=nodo.getAttribute("f-component")
    def build(context,value,name,that):              
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
                console.log("ttttt ",context["__data__"],"$set_"+value)
                if event.target._value:
                    if "." in value:
                        c=context
                        path=value.split(".")
                        for k,n in enumerate(path):
                            if k==len(path)-1:
                                c[n]=event.target._value
                            else:
                                c=c[n]
                        context[path[0]]=context["__data__"][path[0]]
                        event.target.value=c    
                 

                    else:
                        context[value]=event.target._value
                        event.target.value=context[value]
                    

                else:
                    if "." in value:
                        c=context
                        path=value.split(".")
                        for k,n in enumerate(path):
                            if k==len(path)-1:
                                c[n]=event.target.value
                            c=c[n]

                        context[path[0]]=context["__data__"][path[0]]
                        
                    
                    else:
                        context[value]=event.target.value
            event.target.focus()
           
        return change

    for attr in dict(nodo.attributes).values():

        cadena=""

        for name in localdata:
                cadena+=f"let {name}=_localdata['{name}'];"
        for name in context.__data__:
            cadena+=f"let {name}=self.{name};"

        if attr.name.startswith(":"):
            
            _str=lambda x:str(x)
            

            binds[attr.name[1:]]=eval("(function(str,_localdata){let self=this; "+cadena+" return "+attr.value+" })").call(context,_str,localdata)
            nodo._render=True
            
        if attr.name.startswith("f-action:"):

            field=attr.name.split(":")
            if data[field[1]]:
                eval("("+attr.value+")").call(context)
            nodo._render=True
        if attr.name=="f-show":
            
            _boolean=eval("(function(_localdata){self=this; "+cadena+";return "+attr.value+" })").call(context,localdata)
            if _boolean:
                nodo.style.opacity = "1";
            else:
                nodo.style.opacity = "0";
            nodo._render=True
        if attr.name=="f-transition":
            
            eval("(function(_localdata){self=this;"+cadena+"; return "+attr.value+" })").call(context,localdata)
            nodo.style.opacity = "0";
            nodo._render=True
        if attr.name=="f-if":
            
            process_if(that,nodo,context,idx,localdata,condition)
            nodo._render=True
            
        
        if attr.name.startswith("f-model"):
            
            fields={}
            
            
            result=eval("(function(_localdata){let self=this;"+cadena+" return "+attr.value+" })").call(
                context,localdata)
            if result is not None and typeof(result)!="undefined":
                nodo.value=result.toString()

            change=build(context,attr.value,attr.name,that)
            nodo_type=nodo.getAttribute("type")
            """
            if nodo_type=="text" or nodo_type=="textarea":
                nodo.addEventListener("keyup",change)
            else:
                nodo.addEventListener("change",change)
            """
            nodo.addEventListener("change",change)
            nodo._render=True
            nodo._model=True
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
        nodo._render=True
    if store:
        eval("(function(){ if (this['$store']["+store+"]==undefined){this['$store']["+store+"]={}}else{ throw Error('No se puede crear store ya '"+store+"' ya existia')} })").call(context)
        nodo._render=True

        
            

        
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
                if "." not in name:
                    cadena+=f"let {name}=_localdata['{name}'];"
            for name in context.__data__:
                if "." not in name:
                    cadena+=f"let {name}=self.{name};"

            
            if attr.name.startswith("f-model:"):
                field=attr.name.split(":")
                #actualiza la data local del componente al la del contexto superior, esto es asi porque,
                #gracias al f-model, el superior se debio haber modificado y el componente debe heredar su valor
        
                result=eval("(function(){let self=this; "+cadena+";return "+attr.value+" })").call(context)
                
                data[field[1]]=result
                padre=context
                nodo._render=True

            if attr.name.startswith("f-text") and not attr.name.startswith("f-text:"):#
                text=eval("(function(){let self=this;"+cadena+" ;return "+attr.value+" })").call(context)
                nodo.innerText=text
                nodo._render=True
            
            if attr.name=="f-value" and not attr.name.startswith("f-value:"):
                text=eval("(function(){let self=this; "+caden+";return "+attr.value+" })").call(context)
                data[text]=node.innerText
                nodo._render=True
                

            if attr.name.startswith("f-html") and not attr.name.startswith("f-html:"):

                text=eval("(function(){let self=this;"+cadena+" ;return "+attr.value+" })").call(context)
                nodo.innerHTML=text
                nodo._render=True

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



def process_if(that,node,context,idx,localdata,condition={}):
    node_if=node.getAttribute("f-if")
    node_elif_before=None
    cadena=""
    for name in localdata:
        if "." not in name:
            cadena+=f"let {name}=_localdata['{name}'];"
    for name in context.__data__:
        if "." not in name:
            cadena+=f"let {name}=self.{name};"

    node2=node

    node_if=node2.hasAttribute("f-if")

    node_elif=node2.hasAttribute("f-elif")

    node_else=node2.hasAttribute("f-else")
    
    _remove=True

    if  node_if:
        _if=node2.getAttribute("f-if")
        valor=eval("(function(_localdata){"+f"let self=this; {cadena} return {_if}"+"})").call(context,localdata)
        console.log("FFFFF",valor,context,localdata,_if)
        condition=valor
        if condition:
            condition["condition"]=True
        if not condition:
            node2.remove()

            console.log("iiii",_remove)
        console.log("nnnnnnnnnnnnn",valor,condition,_remove)
    elif node_elif:
        _elif=node2.getAttribute("f-elif")
        valor=eval("(function(_localdata){"+f"let self=this; {cadena} return {_elif}"+"})").call(context,localdata)

        if not condition and valor==True:

            condition=valor
        elif condition:

            node2.remove() 
        nodo2._render=True
    elif condition and not node_else and node_elif:#elif
        
        _remove=True
        
    elif condition and node_else:#else
        
        _remove=True
        pass

    if node2.hasAttribute("f-if"):
        node2.removeAttribute("f-if") 
    if node2.hasAttribute("f-elif"):
        node2.removeAttribute("f-elif")
    if node2.hasAttribute("f-else"):
        node2.removeAttribute("f-else") 

        

        

def travese(that,nodo,context,idx,localdata={},lock=False,condition={}):

    process_api(that,nodo,context,localdata)
    if nodo.__proto__.constructor.name=="Text":
        
        nodo.nodeValue=reemplazarValores(nodo.nodeValue,
            Object.assign({},context["__data__"],localdata))
        return nodo
    if nodo.__proto__.constructor.name=="Comment":
        return 
    if not lock:
        cadena=""
        for name in localdata:
            if "." not in name:
                cadena+=f"let {name}=_localdata['{name}'];"
        for name in context.__data__:
            if "." not in name:
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
                    nodo._render=True
                else:

                    """
                    nodo.addEventListener(attr.name[1:],
                        lambda event: eval("(function(){self=this; "+value+" })").call(context) )
                    """
                    
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
                                    if typeof(context["__data__"][n])=="object" and before_state[n]!=JSON.stringify(context["__data__"][n]):
                                        #solo seria necesario una vez puesto que __data__
                                        #ya tiene todos los cambios
                                        context[n]=context["__data__"][n]
                                        break
                        return evento
                    evento=build(context,localdata)
                    nodo.addEventListener(attr.name[1:],evento)
                    nodo._render=True
            if attr.name.startswith(":"):

                if attr.name==":value":
                    result=eval("(function(_localdata){let self=this;"+cadena+" ;"+attr.value+" })").call(context,localdata)
                    nodo._value=result

                nodo._render=True



    if len(nodo.children)==0:
        
        
        nodo.innerHTML=reemplazarValores(nodo.innerHTML,Object.assign({},context["__data__"],localdata))
        
        binds={}

        if nodo.getAttribute("f-for"):
            # Procesado cuando no hay hijos
            
            process_for(that,nodo,context,idx,localdata,lock)

        else:
            
            process_attr(that,nodo,context,idx,localdata,lock,condition)
    else:
        
        if nodo.getAttribute("f-for"):
            # Procesado cuando no hay hijos
            
            process_for(that,nodo,context,idx,localdata,lock)
        else:
            
            process_attr(that,nodo,context,idx,localdata,lock,condition)
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
                nodo._model=True
                nodo.removeAttribute("f-model")

            for nodo2 in nodo.children:
                travese_nodo(nodo2)
        
        travese_nodo(self.refs[form])
        return data

    def process_payload(self,context,nodo,localdata):
        form=nodo.getAttribute("f-payload")
        cadena=""
        for name in localdata:
            if "." not in name:
                cadena+=f"let {name}=_localdata['{name}'];"
        for name in context.__data__:
            if "." not in name:
                cadena+=f"let {name}=self.{name};"

        return eval("(function(){"+f"let self=this;{cadena} return {form}"+"})").call(context)
        
        

            


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

        #nodo.innerHTML=tpl.innerHTML
        def travese2(nodo,nodo2):
            if len(nodo.childNodes)==len(nodo2.childNodes):
                
                
                if nodo2.childNodes==0:
                    if nodo.__proto__.constructor.name=="Text":
                        nodo.nodeValue=nodo2.nodeValue
                    else:
                        nodo.innerHTML=nodo2.innerHTML
                        #console.log("oooooooo",nodo,nodo2)
                else:
                    k=0
                    for n2 in nodo2.childNodes:
                        n=nodo.childNodes[k]
                        
                        if n and n._model:
                            pass
                        elif n and n._render:
                            
                            if n.__proto__.constructor.name=="Text":
                                n.nodeValue=n2.nodeValue
                            else:
                                """
                                if len(n.childNodes)>0:
                                    travese2(n,n2)
                                else:
                                """
                                n.outerHTML=n2.outerHTML


                        elif n and n._for:
                            n.outerHTML=n2.outerHTML
                            #console.log("aaaaaa",nodo,nodo2)
                        else:
                            if n:

                                travese2(
                                    n,
                                    n2)

                        
                        
                        k+=1
                
            else:

                nodo.innerHTML=nodo2.innerHTML
        
        travese2(nodo,tpl.content.children[0])

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
      
        FF.signals[name].append(callback)
    else:
        FF.signals[name]=[callback]
FF.on=on
def emit(name,params):

    if name in FF.signals:
     
        for callback in FF.signals[name]:
      
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
    for nodo in document.querySelectorAll("[fastfront]"):
        app=App(is_reload)
        FF.apps[nodo.idx]=app
        app.run(nodo)
        
FF.reload=lambda: main(True)
main()

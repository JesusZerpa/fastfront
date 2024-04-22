#from vbuild import render
from fastapi.responses import HTMLResponse
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter,Path
import htmlmin
import fastfmk,os
from fastapi_socketio import SocketManager
router = APIRouter()

def json_dump(valor):
    import json
    return json.dumps(valor)


def explore_snippets(cls,name,app=None,dependencies=[],settings=None):
    
    BASE_DIR=str(settings.BASE_DIR)

    for module in os.listdir(BASE_DIR):
        if os.path.isdir(BASE_DIR+"/"+module):
            if os.path.exists(BASE_DIR+"/"+module+"/templates"+cls.snippets_folder+name+".ff"):
                dependencies.append([BASE_DIR+"/"+module+"/templates"+cls.snippets_folder+name+".ff",name,app,"snippets"])
                with open(BASE_DIR+"/"+module+"/templates"+cls.snippets_folder+name+".ff") as f:
                    return f.read()

def explore_layouts(cls,name,app=None,dependencies=[],settings=None):
    BASE_DIR=str(settings.BASE_DIR)

    for module in os.listdir(BASE_DIR):
        if os.path.isdir(BASE_DIR+"/"+module):
            if os.path.exists(BASE_DIR+"/"+module+"/templates"+cls.layouts_folder+name+".ff"):
                #lista la serie de dependencias
                print("UUUUUUUU")
                dependencies.append([
                    BASE_DIR+"/"+module+"/templates"+cls.layouts_folder+name+".ff",name,app,"layouts"]
                    )
                
                with open(BASE_DIR+"/"+module+"/templates"+cls.layouts_folder+name+".ff") as f:
                    return f.read()


def process_template(cls,content,app=None,blocks={},dependencies=[],settings=None):
    import re
    import json
    from fastfmk import extensions
    print("YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
    include_pattern=r"\{%\s*include\s*['\"][\w|\-|_]+['\"]\s*(?:['\"]\w+['\"])?\s*%\}"
    #pattern=r"\{%\s*include\s*(?:\"\w+\")|(?:'\w+')\s*(?:\"\w+\")?\s*%\}"
    #pattern2=r"\{%\s*include\s*((?:\"\w+\")|(?:'\w+'))\s*((?:\"\w+\")|(?:'\w+'))?\s*%\}"
    include2_pattern=r"\{%\s*include\s*(['\"][\w|_|\-]+['\"])\s*(['\"]\w+['\"])?\s*%\}"

    #pattern3=r"\{%\s*extend\s*(?:['\"]\w+['\"])\s*(?:['\"]\w+['\"])?\s*%\}"
    extend_pattern=r"\{%\s*extend\s*((?:['\"][\w|_|\-]+['\"]))\s*((?:['\"]\w+['\"]))?\s*%\}"



    block_pattern=r"\{%\s*block\s*((?:['\"][\w|\-|_]+['\"]))\s*((?:['\"]\w+['\"]))?\s*%\}"

    section_pattern=r"\{%\s*section\s*((?:['\"][\w|\-|-]+['\"]))\s*((?:['\"]\w+['\"]))?\s*%\}"
    
    sectionextended_pattern=r"\{%\s*section\-extended\s*((?:['\"][\w|\-|-]+['\"]))\s*((?:['\"]\w+['\"]))?\s*%\}"
    

    section2_pattern=r"\{%\s*section\s*(?:['\"][\w|\-|_]+['\"])\s*(?:['\"]\w+['\"])?\s*%\}"

    endblock_pattern=r"\{%\s*?endblock\s*?%\}"
    endsection_pattern=r"\{%\s*?endsection\s*?%\}"

    endsectionextended_pattern=r"\{%\s*?endsection\-extended\s*?%\}"

    import_pattern=r"\{%\s*?import_components\s*?%\}"

    pattern=r"<[A-Z][a-zA-Z0-9]*[^>]*>"
    for elem in re.findall(pattern,content):
        i=elem.find(" ")

        content=content.replace(elem[:i+1],elem[:i]+f" fastfront component='{elem[1:i]}' ")


    extend_matches=re.findall(extend_pattern,content)
    
    include_matches=re.findall(include_pattern,content)
    include2_matches=re.findall(include2_pattern,content)
    for k, match in enumerate(include2_matches):
        if not app and match[1]:
            app=json.loads(match[1].replace("'",'"'))
        snippet=json.loads(match[0].replace("'",'"'))

        content2=explore_snippets(cls,snippet,app,
            dependencies=dependencies,
            settings=settings)


        content=content.replace(include_matches[k],content2)

    section_matches=re.findall(section_pattern,content)

    sectionextended_matches=re.findall(sectionextended_pattern,content)


    endsections=list(re.finditer(endsection_pattern,content))

    endsectionsextended=list(re.finditer(endsectionextended_pattern,content))

    section_searches=re.match(section2_pattern,content)
    


    code=[]
    
    if not app:
        
        app=settings.ROOT_URLCONF.split(".")[0]
        BASE_DIR=str(settings.BASE_DIR)
    elif app in extensions:

        BASE_DIR=str(extensions[app].BASE_DIR)

    
    for k,match in enumerate(re.finditer(section2_pattern,content)):
        
        section=match.span()
        name=json.loads(section_matches[k][0].replace("'",'"'))
        
        blocks[name]=content[section[1]:endsections[k].span()[0]]

        end=endsections[k].span()

        blocks[name]=content[section[1]:end[0]]

    for k,match in enumerate(re.finditer(sectionextended_pattern,content)):
        
        section=match.span()
        name=json.loads(sectionextended_matches[k][0].replace("'",'"'))
        if name in blocks:
            blocks[name]+=content[section[1]:endsectionsextended[k].span()[0]]
        else:
            blocks[name]=content[section[1]:endsectionsextended[k].span()[0]]

        end=endsections[k].span()
        if name in blocks:
            blocks[name]+=content[section[1]:end[0]]
        else:
            blocks[name]=content[section[1]:end[0]]
    
    if extend_matches:
        extend = extend_matches[0][0]
        extend= json.loads(extend.replace("'",'"'))
        if extend_matches[0][1]:
            app=json.loads(extend_matches[0][1].replace("'",'"'))

    
        content2=explore_layouts(cls,extend,app=app,
            dependencies=dependencies,
            settings=settings)
        content2=process_template(cls,content2,
            app=app,
            blocks=blocks,
            dependencies=dependencies,
            settings=settings)

        #cls.pages[app+"@"+extend]=



    
        block_find=re.findall(block_pattern,content2)
     
        endblocks=list(re.finditer(endblock_pattern,content2))
        last=0
        for k,block in enumerate(re.finditer(block_pattern,content2)):
   
            end=endblocks[k].span()
            name=json.loads(block_find[k][0].replace("'",'"'))

            if block.span()[0]>0:
                #primero HTML
                code.append(content2[last:block.span()[0]])
            
            if name in blocks:
                if not blocks[name]:
                    #Si no sea sobreescrito la seccion
                    code.append(content2[block.span()[1]:end[0]])

                else:
                    code.append(blocks[name])
            last=end[1]

        if end[0]<len(content2):
            
            code.append(content2[end[1]:])

    else:
        code.append(content)
        #content=content.blocks[section[0]]
        """

    
        for module2 in os.listdir(BASE_DIR):

            BASE_DIR+"/"+module2+"/templates"+cls.pages_folder+name+".ff"
            with open(BASE_DIR+"/"+module2+"/templates"+cls.layout_folder+name+".ff") as f:
                content=f.read()
                cls.layouts[app+"@"+extend]=content
        
        cls.layouts[app+"@"+extend]=htmlmin.minify(layout)
        layout=cls.layouts[app+"@"+extend]
        """
    return "".join(code)

def snake_slug_to_camel(cadena):
  """
  Convierte una cadena en SnakeCase a CamelCase.

  Parámetros:
    cadena (str): La cadena a convertir.

  Retorno:
    str: La cadena convertida a CamelCase.
  """
  import re

  # Reemplaza "_" y "-" por "".
  cadena = re.sub('([-_])', '', cadena)

  # Convierte la primera letra a mayúscula.
  return cadena[0].upper() + cadena[1:]  
                            

def camel_to_snake_slug(cadena):
  """
  Convierte una cadena en CamelCase a SnakeCase.

  Parámetros:
    cadena (str): La cadena a convertir.

  Retorno:
    str: La cadena convertida a SnakeCase.
  """
  import re

  # Reemplaza las letras mayúsculas por "_".
  result=re.sub('([A-Z])', r'-\1', cadena).lower()
  if result.startswith("-"):
    return result[1:]
  return result

class FastFront:
    constants={}
    import_componentes={}
    snippets={}
    pages={}
    layouts={}
    snippets_folder="/snippets/"
    layouts_folder="/layouts/"
    pages_folder="/pages/"
    watching_files={}
    watching_dependencies={}
    livereload_thread=None
    modifiers={
        "json":json_dump
    }
    idx=0
    
    def __init__(self,app,settings,module=None,folder="pages/"):
        """
        Monta rutas de navecion a partir de un folder dentro de templates
        """
        if module==None:
            module=settings.ROOT_URLCONF.split(".")[1]
            appname=settings.ROOT_URLCONF.split(".")[0]


        BASE_DIR=str(settings.BASE_DIR)
        for raiz, directorios, archivos in os.walk(BASE_DIR+"/"+module+"/templates/"+folder):
            url=raiz.replace(BASE_DIR+"/"+module+"/templates/"+folder,"")
            rutas=url.split("/")
            
            for archivo in archivos:
                if archivo.startswith("_") and archivo.endswith(".ff"):
                    def build(archivo):
                        def auto_route(
                            parametro:str,
                            request: Request,
                            operation_id="auto_"+archivo[:-len(".ff")]):
                            
                            #(user_id, item_id, category) = path_params_extractor(request.url.path)
                            
                            path=request.url.path.split("/")
                            
                            return FastFront.render(
                                request,
                                "/".join([*path[1:-1],archivo[:-len(".ff")]]),
                                variables={"$params":request.path_params},
                                settings=settings
                                )
                        
                        app.get("/"+url+"/{"+archivo[1:-len(".ff")]+"}")(
                            auto_route)

                    build(archivo)
                elif archivo=="Index.ff":
                    def auto_route(
                        request: Request,
                        operation_id="auto_"+archivo[:-len(".ff")]):
                        
                        path=request.url.path.split("/")
                        print("wwwww ",path)
                        print("mmmmmm ","/".join([*path[1:],"Index"]))
                        return FastFront.render(
                            request,
                            "/".join([*path[1:],"Index"]),
                            app=appname,
                            settings=settings)

                    print("++++++++++++ ","/"+url)
                    app.get(
                        "/"+url)(
                        auto_route)

                elif archivo.endswith(".ff"):
                    
                    def auto_route(
                        request: Request,
                        operation_id="auto_"+archivo[:-len(".ff")]):
                        
                        path=request.url.path.split("/")
                        
                        view=snake_slug_to_camel(path[-1])
                        
                        return FastFront.render(
                            request,
                            "/".join([*path[1:-1],view]),
                            app=appname,
                            settings=settings)

                    
                    app.get(
                        "/"+url+"/"+camel_to_snake_slug(archivo[:-len(".ff")]))(
                        auto_route)



    @classmethod
    def register_pages(cls,name,app=None,dependencies=[],settings=None):
        import json
        
        if not app:
            
            app=settings.ROOT_URLCONF.split(".")[0]
        BASE_DIR=str(settings.BASE_DIR)

        for module in os.listdir(BASE_DIR):
            
            if os.path.isdir(BASE_DIR+"/"+module):
                print("cccccccccccccc",BASE_DIR+"/"+module+"/templates"+cls.pages_folder+name+".ff")
                if os.path.exists(BASE_DIR+"/"+module+"/templates"+cls.pages_folder+name+".ff"):
                    print("ggggg")
                    with open(BASE_DIR+"/"+module+"/templates"+cls.pages_folder+name+".ff") as f:
                        import re
                        full_path=BASE_DIR+"/"+module+"/templates"+cls.pages_folder+name+".ff"
                        print("llllllllllllllllllll",settings)
                        cls.watching_files[full_path]=[
                            os.path.getmtime(full_path),
                            set([app+"@"+name]),
                            "pages"]

                        template=f.read()
                        content3=process_template(cls,template,
                            app=app,dependencies=dependencies,
                            settings=settings)
                        
                        cls.pages[app+"@"+name]=content3
                        
    @classmethod
    def register_snippet(cls,name,app=None):
        if not app:
            from fastfmk import settings
            app=settings.ROOT_URLCONF.split(".")[0]
        
        assert app+"@"+name in cls.snippets

        if app in fastfmk.extensions:
            BASE_DIR=str(fastfmk.extensions[app].BASE_DIR)
        else:
            BASE_DIR=str(settings.BASE_DIR)


        if os.path.exists(BASE_DIR+"/templates"+cls.snippets_folder+name+".ff"):
            with open(BASE_DIR+"/templates"+cls.snippets_folder+name+".ff") as f:
                cls.snippets[app+"@"+name]=f.read()
                full_path=BASE_DIR+"/templates"+cls.snippets_folder+name+".ff"
                cls.watching_files[full_path]=[os.path.getmtime(full_path),set([app+"@"+name]),"snippets"]

    @classmethod
    def register_layout(cls,name,app=None):
        if not app:
            from fastfmk import settings
            app=settings.ROOT_URLCONF.split(".")[0]


        assert app+"@"+name in cls.layouts
        
        if app in fastfmk.extensions:
            BASE_DIR=fastfmk.extensions[app].BASE_DIR
        else:
            BASE_DIR=settings.BASE_DIR

        if os.path.exists(BASE_DIR+"/templates"+cls.layouts_folder+name+".ff"):
            with open(BASE_DIR+"/templates"+cls.layouts_folder+name+".ff") as f:
                cls.layouts[app+"@"+name]=f.read()
                import re
                pattern=r"\{%\s*include\s*\"[\w|_|\-]+\"\s*(?:\"\w+\")?\s*%\}"
                pattern2=r"\{%\s*include\s*(\"[\w|\-|_]+\")\s*(\"\w+\")?\s*%\}"
                template=f.read()
                matches=re.findall(pattern,template)
                for match in matches:
                    math2=re.findall(pattern2,match)
                    app=match2[1]

                    template=template.replace(
                        match,
                        cls.snippets[app+"@"+match2[0]])
                cls.layouts[app+"@"+name]=template

                full_path=BASE_DIR+"/templates"+cls.layouts_folder+name+".ff"
                cls.watching_files[full_path]=[os.path.getmtime(full_path),set([app+"@"+name]),"layouts"]

    @classmethod
    def register_dependency(cls,name,app):
        """
        La idea es listar todas los snippets y layouts que queremos que se carguen
        de manera offline 
        """

    @classmethod
    def view(cls,route):
        def wrapper(fn):
            router.get(route)(fn)
            return router
        return wrapper

    @classmethod
    def assets(cls,router,settings):
        from fastapi import Path
        from fastapi.responses import FileResponse
        from fastapi.staticfiles import StaticFiles
        import mimetypes
        """
        app.mount("/static", StaticFiles(directory="static"), 
            name="static")
        """
        async def get_static_file(file_path: str):
            """
            This function takes a file path within your project structure and
            returns a FastAPI response object for that file.
            """
            # Construct the full path to the file
            

            full_path = os.path.join(os.getcwd(), file_path)  # os.getcwd() gets current working directory
            
            BASE_DIR=str(settings.BASE_DIR)
            file_content=None
            # Check if the file exists
            
            for module in os.listdir(BASE_DIR):
                
                if os.path.exists(BASE_DIR+"/"+module+"/templates/assets/"+file_path):
                    with open(BASE_DIR+"/"+module+"/templates/assets/"+file_path,"rb") as f:
                        file_content=f.read()
                        break
            if not file_content:
                return {"detail": "File not found"}, 404

            # Create a FileResponse with appropriate headers
            response = FileResponse(BASE_DIR+"/"+module+"/templates/assets/"+file_path, media_type=mimetypes.guess_type(file_path)[0])  # Adjust media_type if needed

            # Set content length header for better performance
            response.headers["Content-Length"] = str(len(file_content))

            return response
    
        router.get("/assets/{file_path:path}")(get_static_file)

    @classmethod
    def _render(cls,request,name,app=None,variables={},settings=None):

        import re,json
        if not app and settings:
            app=settings.ROOT_URLCONF.split(".")[0]

        dependencies=[]
        print("uuuuuuu ",settings,app,name)
        
        cls.register_pages(name,app=app,dependencies=dependencies,
            settings=settings)

        for elem in dependencies:
            if elem[0] not in cls.watching_files:
                cls.watching_files[elem[0]]=[
                os.path.getmtime(elem[0]),set([app+"@"+name])]
            else:
                cls.watching_files[elem[0]][1].add(app+"@"+name)

        
        content=cls.pages[app+"@"+name]
        
        variables_pattern=r"\{\{\s*?[\w|$]+\s*(?:\w+)?\s*?\}\}"
        variables2_pattern=r"\{\{\s*?([\w|$]+)\s*((?:\w+)?)\s*?\}\}"
        variables_matches=re.findall(variables_pattern,content)
        variables2_matches=re.findall(variables2_pattern,content)
        
        for k, match in enumerate(variables2_matches):
            variable=variables2_matches[k]
            match2=variables_matches[k]

            modifier=variable[1]
            variable=variable[0]
            
            if variable in variables:
                valor=variables[variable]
                
                if modifier:
                    valor=cls.modifiers[modifier](valor)
                
                if variable in variables:
                    content=content.replace(match2,valor)
                
        return content


    @classmethod
    def render(cls,request,name,app=None,variables={},settings=None):
        
        variables={**cls.constants,**variables}
        #request.path.url
        print(dir(request))
        print(request.path_params)
        print(request.url)
        variables["$params"]=request.path_params

        content=cls._render(request,name,app=app,variables=variables,
            settings=settings)
        
        return HTMLResponse(content)

    @classmethod
    def livereload(cls,app,settings):
        import threading
        import socketio,asyncio
        from fastapi import Request
        print(">>>>>>>>>>>>",settings)
        
        async def live_reload(idx):
            import time
            while True:
                for path in cls.watching_files:
                    selector=cls.watching_files[path][1]
                    if cls.watching_files[path][0]<os.path.getmtime(path):
                        print("Observando: "+path)
                        print(cls.watching_files[path][1])
                        for page in cls.watching_files[path][1]:
                            print("sssss ",page)
                            _app,name=page.split("@")
                            cls.watching_files[path][0]=os.path.getmtime(path)

                            await app.sio.emit("fastfront-reload",{
                                "name":name,
                                "content":cls._render(None,
                                     name,
                                        app=_app,
                                        settings=settings)},
                                    namespace="/fastfront")
                        """
                        match tipo:
                            case "snippets":
                                
                                await app.sio.emit("fastfront-reload",{
                                    "type":"snippet",
                                    "name":name,
                                    "content":cls.snippets[_app+"@"+name]},namespace="/fastfront")
                            case "pages":
                                
                                
                            case "layouts":
                                await app.sio.emit("fastfront-reload",{
                                    "type":"layouts",
                                    "name":name,
                                    "content":cls.layouts[_app+"@"+name]},namespace="/fastfront")
                        """
                await asyncio.sleep(0.05)
            
        @app.on_event("startup")
        async def startup():
            print("INICIANDO")
            FastFront.constants.update({
                "HOST":"http://localhost:5000"
                })

            ff=FastFront(app,settings)
            FastFront.assets(app,settings)

            asyncio.create_task(live_reload(int(cls.idx) ))
            
        if "sio" not in dir(app):
            pass
            
        

        @app.on_event("shutdown")
        async def on_shutdown():
            print("Apagando servidor")
        cls.idx+=1
        




@router.get("/routes")
def routes():
    """
    Rutas de la aplicación para el webworker que para que no tenga que cargarse
    la vista desde el servidor si es que la vista ya esta cargada en la cache 

    """
    return {
        "pages":[]
    }

@router.get("/{app}/snippets/{name}")
def snippets(app,name):
    return HTMLResponse(FastFront.snippets[app+"@"+name])

@router.get("/{app}/layouts/{name}")
def layouts(app,name):
    return HTMLResponse(FastFront.layouts[app+"@"+name])


#fastapi.build(fastapi)
#app=FastFront(app)
#app.load_layouts()
#app.load_components()


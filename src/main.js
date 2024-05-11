    /*
  pudo manejar los bucles for como shadow ya que esto me permitiria 
  que no se listara los subfor al documento queryselector 
  y igual con los f-if f-elif y f-else 
  */
  let HTMLTAGS = [
    "A",
    "ABBR",
    "ADDRESS",
    "AMP",
    "ARTICLE",
    "ASIDE",
    "AUDIO",
    "B",
    "BASE",
    "BDI",
    "BDO",
    "BLOCKQUOTE",
    "BODY",
    "BR",
    "BUTTON",
    "CANVAS",
    "CAPTION",
    "CENTER",
    "CITE",
    "CODE",
    "COL",
    "COLGROUP",
    "COMMAND",
    "COMMENT",
    "DATALIST",
    "DD",
    "DEL",
    "DETAILS",
    "DFN",
    "DIALOG",
    "DIR",
    "DIV",
    "DL",
    "DT",
    "ELEMENT",
    "EM",
    "EMBED",
    "FIGCAPTION",
    "FIGURE",
    "FONT",
    "FOOTER",
    "FORM",
    "FRAMESET",
    "H1",
    "H2",
    "H3",
    "H4",
    "H5",
    "H6",
    "HEAD",
    "HEADER",
    "HR",
    "HTML",
    "I",
    "IFRAME",
    "IMG",
    "INPUT",
    "INS",
    "KBD",
    "KEYGEN",
    "LABEL",
    "LEGEND",
    "LI",
    "LINK",
    "MAP",
    "MARK",
    "MATH",
    "MENU",
    "MENUITEM",
    "META",
    "METER",
    "NAV",
    "NOBR",
    "NOSCRIPT",
    "OBJECT",
    "OL",
    "OPTGROUP",
    "OPTION",
    "OUTPUT",
    "P",
    "PAGEBREAK",
    "PARAM",
    "PRE",
    "PROGRESS",
    "Q",
    "R",
    "RADIO",
    "RAW",
    "RB",
    "RDF",
    "REF",
    "REGION",
    "REM",
    "RP",
    "RT",
    "RUBY",
    "S",
    "samp",
    "SCRIPT",
    "SECTION",
    "SELECT",
    "SELF",
    "SLOT",
    "SMALL",
    "SOURCE",
    "SPAN",
    "SQRT",
    "STABLE",
    "STANDALONE",
    "STRONG",
    "STYLE",
    "SUB",
    "SUMMARY",
    "SUP",
    "TABLE",
    "TBODY",
    "TD",
    "TEMPLATE",
    "TERMAL",
    "TFOOT",
    "TH",
    "THEAD",
    "TIME",
    "TITLE",
    "TRACK",
    "TR",
    "U",
    "UL",
    "VAR",
    "VIDEO",
    "WBR",
    "XMP"
  ];
  function dynamic_attr(valor){
    let accept=[]
            
        if (typeof(valor)=="string"){
            accept.push(valor)
        }
        else if (typeof(valor)=="number"){
            accept.push(valor)
        }
        else{
            if (Array.isArray(valor)){
              console.log("GGGGGGGGG")
              for (let elem of valor){

                  if (typeof(elem)=="object"){

                      for (let attr in elem){
                        console.log("+++++ ",attr)
                        if (typeof(elem[attr])=='boolean'){
                          if (elem[attr]){
                                accept.push(attr)
                            }
                        }
                          else{
                            accept.push(attr+":"+elem[attr]+";")
                            
                          }
                      }
                  }
                  else if (typeof(elem)=="array"){
                      accept.extend(elem)
                  }
                  else{
                      accept.push(elem)
                  }
        }
      }
      else{
        for (let elem in valor){
          if (typeof(valor[elem])=='boolean'){
            accept.push(elem)
          }else{
            accept.push(elem+":"+valor[elem]+";")
          }
        }
      }
    }

    let _valor=accept.join(" ")
    return _valor
  }
  function process_payload(context, nodo, localdata) {
      let form = nodo.getAttribute("f-payload");
      let cadena = "";
      for (let name in localdata) {
          if (!name.includes(".")) {
              cadena += `let ${name}=_localdata['${name}'];`;
          }
      }
      for (let name in context.__data__) {
          if (!name.includes(".")) {
              cadena += `let ${name}=self.${name};`;
          }
      }
      return (function () {
          let self = this;
          return eval(`${cadena} ${form}`);
      }).call(context);
  }
  function process_form(context, nodo) {
      let form = nodo.getAttribute("f-form");
      form = (function () {
          let self = this;
          let $stores = self.$stores;
          return eval(`${form}`);
      }).call(context);
      let data = {};

      function traverse_node(nodo) {
          if (nodo.children.length === 0) {
              let model = nodo.getAttribute("f-model");
              if (model !== undefined) {
                  let name = nodo.getAttribute("name");
                  let value = (function () {
                      let self = this;
                      let $stores = self.$stores;
                      return eval(`${model}`);
                  }).call(context);
                  data[name] = value;
              }
              nodo._model = true;
              nodo.removeAttribute("f-model");
          }
          for (let nodo2 of nodo.children) {
              traverse_node(nodo2);
          }
      }
      traverse_node(context.refs[form]);
      return data;
  }
  function process_api(that, nodo, context, localdata, doc = null) {
      let tpl = doc ? doc : nodo;

      if (nodo.constructor.name !== "Text" && nodo.constructor.name !== "Comment") {
          let cadena = "";

          for (let name in localdata) {
              if (!name.includes(".")) {
                  cadena += `let ${name}=_localdata['${name}'];`;
              }
          }
          for (let name in context.__data__) {
              cadena += `let ${name}=self.${name};`;
          }

          let fhead = nodo.getAttribute("f-head");
          let ftarget = nodo.getAttribute("f-target");
          let ftrigger = nodo.getAttribute("f-trigger");
          let fswap = nodo.getAttribute("f-swap");
          let fload = nodo.getAttribute("f-load");

          let fpost = null;
          let fget = null;
          let fput = null;
          let fdelete = null;
          let fpatch = null;
          let fresponse = null;
          let fresponse_name = null;
          let fsuccess = null;
          let ferror = null;

          let form_type = null;
          let value = null;

          let keys = ["1", "2"];
          let attributes = Object.values(nodo.attributes);
          let attributes2 = Object.values(tpl.attributes);

          for (let k = 0; k < attributes2.length; k++) {
              let attr = attributes2[k];

              if (attr.name.startsWith(":")) {
                  cadena = "";
                  for (let name in localdata) {
                      if (!name.includes(".")) {
                          cadena += `let ${name}=${JSON.stringify(localdata[name])};`;
                      }
                  }
                  let _str = (x) => String(x);
              }

              if (attr.name.startsWith("f-key")) {
                  fkey = nodo.hasAttribute(attr.name) ? nodo.attributes[attr.name].value : attr.value;
              }
              if (attr.name.startsWith("f-trigger")) {
                  ftrigger = nodo.hasAttribute(attr.name) ? nodo.attributes[attr.name].value : attr.value;
              }
              if (attr.name.startsWith("f-response")) {
                  fresponse = nodo.hasAttribute(attr.name) ? nodo.attributes[attr.name].value : attr.value;
                  fresponse_name = attr.name;
              }
              if (attr.name.startsWith("f-post") || attr.name.startsWith("f-get") ||
                  attr.name.startsWith("f-put") || attr.name.startsWith("f-patch") || attr.name.startsWith("f-delete")) {
                  let attr_value = attr.value;
                  if (typeof attr_value !== "undefined") {
                      if (nodo.hasAttribute(attr.name)) {
                          value = (function (_localdata) {
                              let self = this;
                              return eval(`${cadena} ${attr_value}`);
                          }).call(context, localdata);
                          if (attr.name.endsWith(".formdata")) {
                              form_type = "multipart/form-data";
                          } else if (attr.name.endsWith(".urlencoded")) {
                              form_type = "application/x-www-form-urlencoded";
                          } else if (attr.name.endsWith(".plain")) {
                              form_type = "text/plain";
                          } else {
                              form_type = "application/json";
                          }
                      } else if (doc) {
                          attr_value = doc.getAttribute(attr.name);
                          value = (function (_localdata) {
                              let self = this;
                              return eval(`${cadena} ${attr_value}`);
                          }).call(context, localdata);
                          if (attr.name.endsWith(".formdata")) {
                              form_type = "multipart/form-data";
                          } else if (attr.name.endsWith(".urlencoded")) {
                              form_type = "application/x-www-form-urlencoded";
                          } else if (attr.name.endsWith(".plain")) {
                              form_type = "text/plain";
                          } else {
                              form_type = "application/json";
                          }
                      }
                      if (attr.name.startsWith("f-post")) {
                          fpost = value;
                      } else if (attr.name.startsWith("f-get")) {
                          fget = value;
                      } else if (attr.name.startsWith("f-put")) {
                          fput = value;
                      } else if (attr.name.startsWith("f-patch")) {
                          fpatch = value;
                      } else if (attr.name.startsWith("f-delete")) {
                          fdelete = value;
                      }
                  }
              }
              if (attr.name.startsWith("f-error")) {
                  ferror = attr.value;
              }
              if (attr.name.startsWith("f-success")) {
                  fsuccess = attr.value;
              }
              if (attr.name.startsWith(":")) {
                  cadena = "";
                  let _str = (x) => String(x);
                  for (let name in localdata) {
                      if (!name.includes(".")) {
                          cadena += `let ${name}=${JSON.stringify(localdata[name])};`;
                      }
                  }
              }
          }

          if (fhead) {
              fhead = context[fhead];
          } else {
              fhead = {
                  "Content-Type": "application/json",
                  "accept": "application/json"
              };
          }
          if (form_type) {
              fhead["Content-Type"] = form_type;
          }

          async function trigger(event) {
              let data = {};
              if (event !== undefined) {
                  event.preventDefault();
                  event.stopPropagation();
                  if (nodo.getAttribute("f-form")) {
                      let fform = nodo.getAttribute("f-form");
                      if (fform !== undefined && event.target !== undefined) {
                          data = process_form(context, event.target);
                      }
                  } else if (nodo.getAttribute("f-payload")) {
                      let fpayload = nodo.getAttribute("f-payload");
                      if (fpayload !== undefined && event.target !== undefined) {
                          data = process_payload(context, event.target, localdata);
                      }
                  }
              }
              if (fget !== null) {
                  let req;
                  if (fhead["Content-Type"] === "application/json") {
                      req = await fetch(fget, {
                          "method": "GET",
                          "headers": fhead,
                      });
                  } else {
                      req = await fetch(fget, {
                          "method": "GET",
                          "headers": fhead,
                      });
                  }
              } else if (fpost !== null) {
                  let req;
                  if (fhead["Content-Type"] === "application/json") {
                      req = await fetch(fpost, {
                          "method": "POST",
                          "headers": fhead,
                          "body": JSON.stringify(data)
                      });
                  } else {
                      req = await fetch(fpost, {
                          "method": "POST",
                          "headers": fhead,
                          "body": data
                      });
                  }
              } else if (fpatch !== null) {
                  let req;
                  if (fhead["Content-Type"] === "application/json") {
                      req = await fetch(fpatch, {
                          "method": "PATCH",
                          "headers": fhead,
                          "body": JSON.stringify(data)
                      });
                  } else {
                      req = await fetch(fpatch, {
                          "method": "PATCH",
                          "headers": fhead,
                          "body": data
                      });
                  }
              } else if (fput !== null) {
                  let req;
                  if (fhead["Content-Type"] === "application/json") {
                      req = await fetch(fput, {
                          "method": "PUT",
                          "headers": fhead,
                          "body": JSON.stringify(data)
                      });
                  } else {
                      req = await fetch(fput, {
                          "method": "PUT",
                          "headers": fhead,
                          "body": data
                      });
                  }
                  data = await req.json();
              } else if (fdelete !== null) {
                  let req;
                  if (fhead["Content-Type"] === "application/json") {
                      req = await fetch(fdelete, {
                          "method": "DELETE",
                          "headers": fhead,
                          "body": JSON.stringify(data)
                      });
                  } else {
                      req = await fetch(fdelete, {
                          "method": "DELETE",
                          "headers": fhead,
                          "body": data
                      });
                  }
              }
              if (req.status >= 200 && req.status < 300) {
                  data = await req.json();
                  for (let attr of Object.values(nodo.attributes)) {
                      if (attr.name.startsWith("f-reponse:")) {
                          let field = attr.name.split(":");
                          context[field[1]] = eval(`(${fresponse})`).call(null, data, fkey);
                      }
                  }
                  if (fresponse) {
                      let field = fresponse_name.split(":");
                      let response = eval(`(${fresponse})`).call(null, data, fkey);
                      console.log("ooooooo ", field[1], response);
                      context[field[1]] = response;
                  }
                  if (fsuccess) {
                      (function (data, _localdata) {
                          let self = this;
                          eval(`${cadena} ${fsuccess}`);
                      }).call(context, data, localdata);
                  }
              } else {
                  try {
                      data = await req.json();
                  } catch {
                      let response = await req.text();
                      console.error(response);
                  }
                  if (ferror) {
                      (function (_localdata) {
                          let self = this;
                          eval(`${cadena} ${ferror}`);
                      }).call(context, localdata);
                  }
              }
              fkey = null;
          }

          if (typeof ftrigger !== "undefined") {
              ftrigger = (function (_localdata) {
                  let self = this;
                  return eval(`${cadena} ${ftrigger}`);
              }).call(context, localdata);
          }

          if (typeof ftrigger === "undefined" || ftrigger === null) {
              if (typeof nodo.triggered === "undefined" && [Boolean(fget), Boolean(fput), Boolean(fdelete), Boolean(fpost)].some(Boolean)) {
                  nodo.addEventListener("click", trigger);
                  nodo.triggered = true;
              }
          }
          if (ftrigger === "init") {
              if (typeof nodo.inited === 'undefined') {
                  trigger();
                  nodo.inited = true;
              }
          }
      }
  }
  function build_context(widget,data,parentContext){
    /*
    Los contextos se encargan de actualizar los valores de los atributos de las directivas de sus elementos hijos
    */
    //context={"__data__":None}
      //data2=Object.assign({"$refs":that.refs,"$stores":that.stores},data)
      let context={"__data__":data}
      function builder(widget,name,data,context){

        
          function get_func(){

              return data[name]
          }
          function set_func(value){

              cadena=""
              data[name]=value
              if (!Object.keys(widget.nodes).includes(name)){
                return
              }
              for (let node of widget.nodes[name]){
                let nodo=node[0]
                let directiva=node[1]
                let code=node[2]
                let parent=node[3]
                let cadena=""
          for (let elem in data){
            cadena+=`let ${elem}=data['${elem}'];`;
            
          }
          
                if (nodo.__proto__.constructor.name!="Text" && 
                  nodo.__proto__.constructor.name!="Comment"){
                  if (HTMLTAGS.includes(nodo.tagName)){
                    // atributos span normales
                    if (directiva==null){
                      let result=eval("(function(){"+cadena+";return ("+code.slice(2,-2)+")})").call(context)
                      nodo.innerHTML=result
                    }else{
                      let result=eval("(function(){"+cadena+";return ("+code+")})").call(context)
                      let _valor=dynamic_attr(result)
                      nodo.setAttribute(
                        directiva.slice(1,),
                        _valor
                        )


                    }
                    
                    
                  }
                  else{
                    //custom elements
                    let d={}
                    d[name]=value
                    nodo.render(d)
                    if (nodo.__proto__.constructor.name=="FIf"){
                      nodo.process()

                    }
                  }
                }
              else{
                let result=reemplazarValores(code,data)
                nodo.nodeValue=result
                }
              }

              for (let elem of widget.subcomponents){
                let reconect=false
                for (let model in elem.f_models){
                  let parent=elem.f_models[model]
                  if (parent==name){
                    reconect=true
                    break
                  }
                }
                if (reconect){
                  elem.connectedCallback()
                
                }
              }

          }
      
      Object.defineProperty(context,name,{
              "get":get_func,
              "set":set_func
              })

    }

    for (let name in data){
      builder(widget,name,data,context)
      
    }
    return context
  }
  function reemplazarValores(cadena, datos){
      //patron = RegExp(r"{{\s*(.*?)\s*}}","g");
      patron = RegExp("\{\{([^{}.]+(?:\.[^{}.]+)*)\s*\}\}","g");
      let response
      
      function reemplazo(match, p1){

          clave = p1.trim();
          if (clave.indexOf(".")>-1 && clave.indexOf("?")==-1){

              response=datos
   
              for (let elem of clave.split(".")){
                if (response[elem]!=undefined){
                      response=response[elem]
                  }

              }
          
                  
              if (typeof(response)=="object"){
                response=JSON.stringify(response)
              }
                  
              return response
           }
          else if(clave.indexOf("[")>-1 || clave.indexOf("?")>-1 || clave.indexOf(":")>-1){
            clave=clave.trim()
            let cadena2=""
        for (let elem in datos){
          cadena2+=`let ${elem}=datos['${elem}'];`;
          
        }
      
              result=eval("(function(){"+cadena2+";return "+clave+"})").call(datos)
          }
              
          else{
            response=datos[clave]
          }
          
          if (response!=undefined){
              if (typeof(response)=="object"){


                  //Esto se hace para evitar la recursividad al hacer
                  // stringify por el attributo $store

                  response2=Object.assign({},response)

                  //del response2["$stores"]
                  
                  response2=JSON.stringify(response2)
                  return response2
                  }
              else{
                  return response.toString()
              }
          }
          else{
              return  "";
          }
      }

      resultado = cadena["replace"](patron, reemplazo);
      
      return resultado;
  }
  function travese(nodo,data,localdata,root=null,customs=[],ifs=[]){
    
    nodo.root=root
    
    let data2=Object.assign({},data["__data__"],localdata)
    let localdata2=Object.assign({},localdata)
    
    
    for (let elem of nodo.childNodes){
      if (elem.__proto__.constructor.name=="Text"){
        elem._value=elem.nodeValue
        elem.nodeValue=reemplazarValores(elem.nodeValue,data["__data__"])
        for (let key in data2){
          if (elem._value){//este condicional es para evitar procesar cadenas vacias
            let nombreVariableRegex = new RegExp( key + "\\b");

            if (nombreVariableRegex.test(elem._value)){
              if (root.nodes[key]){
                let valid=true
                for (let n of root.nodes[key]){

                  if (n[0]==elem ){
                    valid=false
                    break
                  }
                }
                if (valid){
                  root.nodes[key].push(
                    [elem,null,elem._value,elem.parentNode]
                  )
                }
                
                
              }
              else{
                root.nodes[key]=[
                    [elem,null,elem._value,elem.parentNode]
                  ]
                
                
              }
              
            }
          }
        }
      
      }
      
          
    }
    let fif_node

    for (let elem of nodo.children) {
      let is_for
      let condition=false
      if (root){
        elem.root=root
      }
      if (elem.processed){
        continue
      }

      /*
      if (elem.__proto__.constructor.name=="FIf"){
        if (!ifs.includes(elem)){
          ifs.push(elem)
        }
        
        fif_node=elem
        continue
      }
      if (elem.__proto__.constructor.name=="FELif"){
        fif_node.group.push(elem)
        continue
      }

      if (fif_node && elem.__proto__.constructor.name=="FElse"){
        fif_node.else=elem
        continue
      }
      */
    
      let is_custom=false;
      
      
      if (HTMLTAGS.includes(elem.tagName)
        ){

      }
      else if (elem.render && !elem.rendered){
        is_custom=true
        elem.localdata=localdata
        if (elem.__proto__.constructor.name=="FFor"){

          if (!customs.includes(elem)){
            customs.push(elem)
            elem.innerHTML=""


          }
          
        }
        
        /*
        if (!elem.rendered){
          
            elem.render(localdata,data)
        
          

        } 
        */

      }else if(elem.comp){
        is_custom=true
      }
      if (elem.__proto__.constructor.name=="FFor"){
        console.log("ZZZZZZZZZZZZZZZZZZZZZZZZZZ",elem)

      }

      if (elem.children.length==0){
      
        let template
        if (elem._value){
          template=elem._value
        }else{
          template=elem.innerHTML
        }
        if (!elem._value &&template.indexOf("{{")>-1 && template.indexOf("}}")>-1){

          elem._value=template
          
          let compiled=reemplazarValores(elem._value,
            data2)
          
          
          elem.innerHTML=compiled
          
          for (let key in data2){
            var nombreVariableRegex = new RegExp( key + "\\b");
            
            if (root && nombreVariableRegex.test(elem._value)){
              if (root.nodes[key]){
                let valid=true
                for (let n of root.nodes[key]){

                  if (n[0]==elem ){
                    valid=false
                    break
                  }
                }
                if (valid){
                  root.nodes[key].push(
                    [elem,null,elem._value,elem.parentNode]
                  )
                }

                
              }
              else{
                root.nodes[key]=[
                    [elem,null,elem._value,elem.parentNode]
                  ]
                
                
              }
              
            }
          }
        }

        
      }
      
      let cadena=""
      
      for (let elem in localdata){
        cadena+=`let ${elem}=localdata['${elem}'];`;
        
      }
      for (let elem in data["__data__"]){
        if (!Object.keys(localdata).includes(elem)){
          cadena+=`let ${elem}=data['${elem}'];`;
        }
        
        
      }
      process_api(root,elem,data,localdata)
      
      for (let attr of elem.attributes){
        if (attr.name=="f-for"){
          if (root){
            part=attr.value.split(" in ")
            if (attr.value.indexOf("(")>-1){
              part2=part[0].trim().slice(1,-1).split(",")
              
              elem._iterable=[part2[0],part2[1],part[1]]
            }
            else{
              elem._iterable=[null,part[0],part[1]]
            }
            elem._value=elem.innerHTML
            elem.previuos=elem.previousSlibling
            elem.next=elem.nextSlibling
            elem.parent=elem.parentNode
            elem.nodes={}
            root.fors.push(elem)
          }
          
          is_for=true
        }
      }
      let ifs=[]
      for (let attr of elem.attributes){
        if (attr.name=="f-if"){
          fif_node=elem
          fif_node.elifs=[]
          fif_node.nodes={}
          root.ifs.push(elem)
          condition=true

        }
        else if (attr.name=="f-elif"){
          elem.nodes={}
          elem.ifs=[]
          elem.elifs=[]
          if (fif_node){
            fif_node.elifs.push(elem)
          }
          condition=true
        }
        else if (attr.name=="f-else"){
          elem.ifs=[]
          elem.elifs=[]
          elem.nodes={}
          if (fif_node){
            elem.nodes={}
            fif_node.else=elem
          }
          condition=true
        }
        
        else if (attr.name.startsWith(":")){
          
          
          for (let key in data["__data__"]){

            var nombreVariableRegex = new RegExp( key + "\\b");
            if (root && nombreVariableRegex.test(attr.value)){
              if (root.nodes[key]){
                let valid=true
                for (let n of root.nodes[key]){
              
                  if (n[0]==elem && n[1]==attr.name){
                    valid=false
                    break
                  }
                }
                if (is_custom){
                  
                  
                  if (valid){
                    root.nodes[key].push(
                    [elem,attr.name,attr.value,elem.parent]
                    )
                  }
                  

                }else{
                
                  if (valid){
                    root.nodes[key].push(
                    [elem,attr.name,attr.value,elem.parentNode]
                    )
                  }
                }
                
              }
              else{
                if (is_custom){
                  root.nodes[key]=[
                    [elem,attr.name,attr.value,elem.parent]
                  ]
                }else{
                  root.nodes[key]=[
                    [elem,attr.name,attr.value,elem.parentNode]
                  ]
                }
                
                
              }
              
            }
          }
          
          
          if (!is_custom){
        
            let valor=eval("(function(localdata){"+cadena+";return "+attr.value+"})").call(data["__data__"],localdata)
            
            valor=dynamic_attr(valor)
            
            elem.setAttribute(attr.name.slice(1,),valor)
            elem.processed=true
            
        
          }
          
          
          
          //elem.removeAttribute(attr.name)
        }
        if (attr.name=="f-model"){
          function build(context,localdata){
            return function(event){
              let code=event.target.getAttribute(attr.name)
              
              
              c=context
              if (attr.value.indexOf(".")>-1){
                map=attr.value.split(".")
                for (let elem of map.slice(0,-1)){
                  c=c[elem]
                }
                c[map[-1]]=event.currentTarget.value
                context[map[0]]=context[map[0]]
              }else{
                context[attr.value]=event.currentTarget.value
              }
              

              console.log("EJECUTANDO2",event.target)

            }
          }
          let fn=build(data,localdata)
          elem.addEventListener("keyup",fn)
          elem.processed=true
        }
        else if(attr.name.startsWith("f-model:")){
          let name=attr.name.replace("f-model:","")
          /*Asumiremos que es un custom component igualmente*/
          elem.f_context=data
          elem.f_localdata=localdata
          let models={}
          models[name]=attr.value
          elem.f_models=models
        }
        if (attr.name.startsWith("@")){
          function build(context,localdata){
            return function(event){
              let code=event.target.getAttribute(attr.name)
              
              let cadena=""
              for (let elem in localdata){
                cadena+=`let ${elem}=localdata['${elem}'];`;
                
              }
              for (let elem in data["__data__"]){
                if (!Object.keys(localdata).includes(elem)){
                  cadena+=`let ${elem}=data['${elem}'];`;
                }
                
                  
              }
              

              eval("(function(event,localdata){"+cadena+"("+code+")(event)})").call(data,event,localdata)

              console.log("EJECUTANDO",event.target)

            }
          }
          let fn=build(data,localdata)
          elem.addEventListener(attr.name.slice(1,),fn)
          elem.processed=true
        }
      
      
      }
      if (!is_for && !condition){
        travese(elem,data,localdata,root,customs,ifs)
      }
      
    }
  }
  function updater(nodo,data,localdata,root=null){
    nodo.root=root
    for (let elem of nodo.childNodes){
      if (elem.__proto__.constructor.name=="Text"){

        elem.nodeValue=reemplazarValores(elem._value,data["__data__"])
      }
    }
    for (let elem of nodo.children){
      if (root){
        elem.root=root
      }
      let is_custom=false;
      if ([
        "DIV","SPAN","H1","H4","BUTTON","INPUT"
        ].includes(elem.tagName)
        ){


      }
      else{
        is_custom=true

        elem.render(localdata)
      }


      for (let attr of elem.attributes){
        if (attr.name.startsWith(":")){
          for (let key in data["__data__"]){
            var nombreVariableRegex = new RegExp( key + "\\b");
            
            if (nombreVariableRegex.test(attr.value)){

              if (root.nodes[key]){
                if (is_custom){
                  root.nodes[key].push(
                    [elem,attr.name,attr.value,elem.parent]
                  )

                }else{
                  root.nodes[key].push(
                    [elem,attr.name,attr.value,elem.parentNode]
                  )
                }
                
              }
              else{
                if (is_custom){
                  root.nodes[key]=[
                    [elem,attr.name,attr.value,elem.parent]
                  ]
                }else{
                  root.nodes[key]=[
                    [elem,attr.name,attr.value,elem.parentNode]
                  ]
                }
                
                
              }
              
            }
          }
          
          
          if (!is_custom){
            valor=eval(attr.value)
            elem.setAttribute(attr.name.slice(1,))
        
          }
          
          
          
          //elem.removeAttribute(attr.name)
        }
        if (attr.name.startsWith("@")){
          
        }

      updater(elem,data,localdata,root)
      }
    }
  }
  function process_for(root,loop,context,_localdata,n_foor){
    let localdata=Object.assign({},_localdata)
    let value=context[loop._iterable[2]]
    if (value==undefined){
      value=localdata[loop._iterable[2]]
    }
          
    let cadena=""
    let c=0
    
    for (let elem in localdata){
        cadena+=`let ${elem}=localdata['${elem}'];`;
        
      }
    for (let elem in context["__data__"]){

      if (!Object.keys(localdata).includes(elem)){

        cadena+=`let ${elem}=this['${elem}'];`;
      }
      
      
    }
    let comment_node=document.createComment(`forloop #${n_foor}`)

    loop.parent.insertBefore(comment_node,loop)

    loop.parent.removeChild(loop)   
    for (let iter of value){
      let clon=loop.cloneNode(true)
      clon.nodes={}
      clon.ifs=[]
      clon.fors=[]
      localdata[loop._iterable[1]]=iter
      if (loop._iterable[0]){
        

        let _cadena=cadena+`let ${loop._iterable[0].trim()}=${c};`
      }
      let _cadena=cadena+`let ${loop._iterable[1].trim()}=localdata['${loop._iterable[1]}'];`

      if (loop._if){

        let val=eval("(function(localdata){"+_cadena+"return "+loop._if+")").call(this.context)

        if (comment_node.nextSlibling){

          comment_node.parentNode.insertBefore(clon,comment_node.nextSlibling)
        }
        else{
          comment_node.parentNode.appendChild(clon)
        }
        
        travese(clon,this.context,localdata,clon)


      }else{

        if (comment_node.nextSlibling){
          
          comment_node.parentNode.insertBefore(clon,comment_node.nextSlibling)
        }
        else{
          comment_node.parentNode.appendChild(clon)
        }

        travese(clon,context,localdata,clon)
      }
      let n_foor2=0;
      for (let subloop of  clon.fors){
        process_for(root,
          subloop,
          context,
          localdata,
          n_foor2)
        n_foor2+=1

      }
      let n_if=0;
      for (let if_node of clon.ifs){
            
        process_if(this,
          if_node,
          context,
          localdata,
          n_if)

        n_if+=1;
        
      }

      


      
    }

  }
  
  function process_if(root,node_if,context,_localdata,n_if){
    let localdata=Object.assign({},_localdata)
    let condition=false
    let _if=node_if.getAttribute("f-if")
    let cadena=""
    for (let elem in localdata){
      cadena+=`let ${elem}=localdata['${elem}'];`;
      
    }
    console.log("AAAAAAAAAAAAA",context)
    for (let elem in context["__data__"]){
      if (!Object.keys(localdata).includes(elem)){
        cadena+=`let ${elem}=this['${elem}'];`;
      }
      
        
    }

    if (_if){
      condition=eval("(function(localdata){"+cadena+"return "+_if+"})").call(context,localdata)
      console.log("TTTTTTTTTTTTTTTTTT",condition,_if,cadena)
      
      if (!condition){
        console.log("VVVVVVVVVVV",node_if,node_if.parentNode)
        node_if.parentNode.removeChild(node_if)
      }
      else{
        travese(node_if,context,localdata,node_if)
      }
      console.log("")
      

    }
    console.log("eeeeeeeeeeeee",condition)
    for (let node of node_if.elifs){
      let elif=node.getAttribute("f-elif")
      if (elif){
        
        

        let condition=eval("(function(localdata){"+cadena+"return "+elif+"})").call(context,localdata)
        
        if (!condition){
          node.parentNode.removeChild(node)
        }
      }else{
        travese(node_if,context,localdata,node_if)
      }
    }
    console.log("mmmmmmmmmmmmmm",condition,node_if.else)
    if (condition){
      
      node_if.parentNode.removeChild(node_if.else)
    }else{
      travese(node_if.else,context,localdata,node_if.else)
    }
    


  }

  class HolaMundo extends HTMLElement{
    constructor(){
      super()
    }
    connectedCallback(){
      this.innerHTML="<H1>Hola Mundo con un web Component</H1>"
    }

  }
  class FComponent extends HTMLElement{
    constructor(){
      super()

    }
    connectedCallback(){
      this.outerHTML="<H1>Hola Mundo con un web Component</H1>"
    }
    render(localdata={}){

    }

  }
  class FWidget extends HTMLElement{
    constructor(){
      super()
      this.subcomponents=[]
      if (this.getAttribute("f-data")){
        let data=eval("("+this.getAttribute("f-data")+")")
        this.data=data
        this.nodes={}
        this.context=build_context(this,this.data)
        this.ifs=[]

      }


      
    }
    connectedCallback(){
      //this.outerHTML="<H1>Hola Mundo con un web Component</H1>"

      travese(this,this.context,{},this)

      for (let if_node of this.ifs){
        if_node.clean()
        if_node.process()
      }


      
    }
    render(localdata={}){
      //Sub widgets
      //updater(this,this.context,localdata,this)
      

    }

  }
  class FIf extends HTMLElement{
    constructor(){
      super()

      this.template=this.innerHTML
      this.condition=this.getAttribute(":condition")

      this.parent=this.parentNode
      this.current=this
      this.group=[]
      let start=false

      for (let elem of this.parent.children){
        if (elem==this){
          start=true
        }
        if (start && elem.tagName=="F-ELSE"){
          this.else=elem
          break
        }
      }
      
      
    }
    connectedCallback(){
      
      
    }
    render(localdata={}){
      /*
      this.localdata=localdata
      console.log("uuuuu",localdata)
      

      
      
      this.root.ifs.push(this)

      
      console.log("zzzzzz",localdata)
      
    
      this.rendered=true  
      */
      
    }
    clean(){
      for (let elem of this.parent.children){

        if (elem.__proto__.constructor.name=="FElse" || elem.__proto__.constructor.name=="FElif"){

          elem.parent.removeChild(elem)
        }
      }   

    }
    process(localdata={}){
      /*
      Vamos a trabajar la eliminacion de los que no complen la condicion 
      desde una funcion diferente y que sea lanzada por el root despues que termine de renderizar porque 
      */
      let cadena=""
      for (let elem in localdata){
        cadena+=`let ${elem}=localdata['${elem}'];`;
        
      }

      for (let elem in this.root.context["__data__"]){
        if (!Object.keys(localdata).includes(elem)){
          cadena+=`let ${elem}=this['${elem}'];`;

        }
                
      }

      let valid=eval("(function(){"+cadena+";return "+this.condition+"})").call(this.root.context)
      
      if (this.current && valid){
        this.parent.replaceChild(this,this.current)
      }

      if (!valid){
        for (let elem of this.group){
          if (elem.is_valid()){
            valid=true
            this.current=elem
            this.parent.replaceChild(elem,this)
            break
          }
        }
      }
      if (!valid){
        this.current=this.else
        this.parent.replaceChild(this.else,this)
        
      }
      travese(this.current,this.root.context,localdata,this.root)
    }
  }
  class FElif extends FIf{
    constructor(){
      super()
    }
  }
  class FElse extends HTMLElement{
    constructor(){
      super()
      this.template=this.innerHTML
      this.parent=this.parentNode
    }
    connectedCallback(){
      if (this.parentNode.condition){
        this.parentNode.remove(this)
      }
    }
    render(localdata={}){
      if (this.parent.condition){
        this.remove()
      }
      else if(this.parentNode==undefined){
        this.parent.appendChild(this)
      }
      this.rendered=true  

    }
  }
  class FFor extends HTMLElement{
    constructor(){
      super()
      this.template=this.innerHTML
      this.parent=this.parentNode
      this.mounted=false
      this.localdata={}
      this.ifs=[]
    }
    connectedCallback(){
      this.innerHTML=""
      /*
      //this.outerHTML="<H1>Hola Mundo con un web Component</H1>"
      let iterable={}
      let valor=null
      let name=null
      let cadena=""
  
      for (let elem in this.localdata){
        cadena+=`let ${elem}=localdata['${elem}'];`;
        
      }
    
      if (this.root){
        for (let elem in this.root.context["__data__"]){
          if (!Object.keys(localdata).includes(elem)){
            cadena+=`let ${elem}=this['${elem}'];`;
          }
          
          
        }
        for (let attr of this.attributes){

          if (attr.name.startsWith(":")){
              if (attr.name!=":id" 
                && attr.name!=":class" 
                && attr.name!=":style"
                && attr.name!=":key"){
                
                valor=eval("(function(){"+cadena+";return "+attr.value+"})").call(this.root.data)
                
                name=attr.name.slice(1,)

                break

            }
          }
          
        }
        let template=this.template
        this.innerHTML=""
        let k=0
        
        if (valor){
          for (let elem of valor){
            if (typeof(elem)!="object"){
              eval("let "+name+`=${elem}`)
            }
            else{
              eval("let "+name+"=elem[k]")
            }
            let d=Object.assign({},this.localdata)
            
            d[name]=elem

            let template_temp=reemplazarValores(template,d)
            let node_template=document.createElement("template")
            
            node_template.innerHTML=template
            this.appendChild(node_template.content)
            travese(this,this.root.context,d,this.root)

            k+=1
              
              
            
            

            
            
          }
        }else if(valor==undefined){
          console.error(`UndefinedValue: ${name}\n`,this,"\n",this.template)
        }
      


      }
      
      
      
      
      for (let if_node of this.ifs){
        if_node.clean()
        if_node.process()
      }
      this.mounted=true
      */
      
    
      
    }
    attributeChangedCallback(name, oldValue, newValue){
    //console.log("+++++++++++++",name, oldValue, newValue)     
    }
    render(localdata={}){
      /*For se trabaja aca porque depende de un componente inicial*/
      let iterable={}
      let valor=null
      let name=null
      let cadena=""
      this.innerHTML=""
      let template=this.template
      
      for (let elem in localdata){
        cadena+=`let ${elem}=localdata['${elem}'];`;
        
      }

      for (let elem in this.root.context["__data__"]){
        if (!Object.keys(localdata).includes(elem)){
          cadena+=`let ${elem}=this['${elem}'];`;
        }
        
        
      }
      let key_value
      for (let attr of this.attributes){

        if (attr.name.startsWith(":")){
            if (attr.name!=":id" 
              && attr.name!=":class" 
              && attr.name!=":style"
              && attr.name!=":key"){
              
              valor=eval("(function(){"+cadena+";return "+attr.value+"})").call(this.root.data)
              
              name=attr.name.slice(1,)

              break

          }
        }
        else if(attr.name=="key"){
          key_value=attr.value
        }
        
      }
      
      let k=0
      if (valor){
        let d=Object.assign({},localdata)
        for (let elem of valor){
          if (typeof(elem)!="object"){
            eval("let "+name+`=${elem}`)
          }
          else{
            eval("let "+name+"=elem[k]")
          }
          
          
          d[name]=elem
          if (key_value){
            d[key_value]=k
          }

          let template_temp=reemplazarValores(template,d)
          let node_template=document.createElement("template")
          
          node_template.innerHTML=template
          this.appendChild(node_template.content)
          let customs=[]
          let ifs=[]
          travese(this,this.root.context,d,this.root,
            customs,ifs)
          for (let custom of customs){
            
            custom.render(d)
      
          }
          console.log("IFS",ifs)
          for (let if_node of ifs){
              if_node.clean()
              if_node.process(d)
            }
        
          k+=1
            
            
          
          

          
          
        }
      }else if(valor==undefined){
        console.error(`UndefinedValue: ${name}\n`,this,"\n",this.template)
      }
      

      
      this.mounted=true
      
      
    this.rendered=true  
    }

  }

  window.customElements.define("hola-mundo",HolaMundo)
  //window.customElements.define("f-component",FComponent)
  //window.customElements.define("f-for",FFor)
  //window.customElements.define("f-if",FIf)
  //window.customElements.define("f-else",FElse)
  //window.customElements.define("f-widget",FWidget)
  for (let nodo of document.querySelectorAll("template")){
    
    // head
    // body
    // script
    let content=null
    let links=[]
    let script=null
    let style=null
    for (let elem of nodo.content.children){
      if (elem.__proto__.constructor.name!="HTMLLinkElement" 
        && elem.__proto__.constructor.name!="HTMLScriptElement"
        && elem.__proto__.constructor.name!="HTMLStyleElement"){
        content=elem
        
      }else if (elem.__proto__.constructor.name=="HTMLStyleElement"){
        style=elem
      }else if (elem.__proto__.constructor.name=="HTMLScriptElement"){
        script=elem
      }else if (elem.__proto__.constructor.name=="HTMLLinkElement"){
        links.push(elem)
      }


    }

    let name=nodo.getAttribute("name")
    if (style){
      document.body.appendChild(style)
    }
    let Component
    if (script){
      
      //encontraria el nombre del componente
      let pattern=new RegExp("export\\s+default\\s+class\\s+(\\w+)")
      
      match=script.innerHTML.match(pattern)

      let code=script.innerHTML.replace("export default","")

      let Comp=eval("(function(){"+code+"; return "+match[1]+"})").call()

      function build(Comp,nodo){
        return class Component extends HTMLElement{
          constructor(){
            super()
            this.fors=[]
            this.ifs=[]
            if (nodo.getAttribute("f-data")){
              let data=eval("("+nodo.getAttribute("f-data")+")")
              this.data=data
              this.nodes={}
              this.context=build_context(this,this.data,this.f_context)
              

            }
            else{
              this.data={}
            }

            if (this.getAttribute("f-data")){
              let data=eval("("+this.getAttribute("f-data")+")")
              this.data=data
            }
            if (content.getAttribute("class")){
              this.setAttribute("class",content.getAttribute("class"))
            }
            if (content.getAttribute("id")){
              this.setAttribute("class",content.getAttribute("class"))
            }
            if (content.getAttribute("style")){
              this.setAttribute("class",content.getAttribute("class"))
            }
            
            this.template=content.innerHTML
            
            this.parent=this.parentNode
            this.mounted=false
            this.comp=new Comp(this)
            if (this.root){
              this.root.subcomponents.push(this)
            }
            

            

          }
          connectedCallback(){
            this.innerHTML=this.template
            //this.outerHTML="<H1>Hola Mundo con un web Component</H1>"
            if (this.comp.connectedCallback){
              this.comp.connectedCallback()

            }
            for (let elem in this.f_models){
              let parent=this.f_models[elem]

              if (parent){
                this.context["__data__"][elem]=this.f_context[parent]
              }
              else{
                this.context["__data__"][elem]=this.f_localdata[parent]

              }
              
            }
            travese(this,this.context,{},this)
            for (let if_node of this.ifs){
              if_node.clean()
              if_node.process()
            }
            
          }
          attributeChangedCallback(){
            if (this.comp.attributeChangedCallback){
              this.comp.attributeChangedCallback()
            }
            
          }
          render(localdata={}){
      
            if (this.comp.render){
              this.comp.render(localdata)
            }
            
          }

        }


      }

      Component=build(Comp,nodo)
      
      if (name){
        window.customElements.define("f-"+name,Component)
      }
      
    }
    else{

      class Component extends HTMLElement{
        constructor(){
          super()
          this.fors=[]
          this.ifs=[]
          this.localdata={}
          if (nodo.getAttribute("f-data")){
            let data=eval("("+nodo.getAttribute("f-data")+")")
            this.data=data
            

          }
          else{
            this.data={}
          }
          if (this.getAttribute("f-data")){
            let data=eval("("+this.getAttribute("f-data")+")")
            this.data=data
          }
          if (content.getAttribute("class")){
            this.setAttribute("class",content.getAttribute("class"))
          }
          if (content.getAttribute("id")){
            this.setAttribute("class",content.getAttribute("class"))
          }
          if (content.getAttribute("style")){
            this.setAttribute("class",content.getAttribute("class"))
          }

          this.nodes={}
          this.context=build_context(this,this.data,this.f_context)
          
          this.template=content.innerHTML
          
          this.parent=this.parentNode
          this.mounted=false
          if (this.root){
            this.root.subcomponents.push(this)
          }
          

          

        }
        connectedCallback(){
          console.log("ROOT: ",this.root,this,this.context)
          this.innerHTML=this.template
          //this.outerHTML="<H1>Hola Mundo con un web Component</H1>"
  
          for (let elem in this.f_models){
            let parent=this.f_models[elem]

            if (parent){
              this.context["__data__"][elem]=this.f_context[parent]
            }
            else{
              this.context["__data__"][elem]=this.f_localdata[parent]

            }
            
          }
          let customs=[]
          travese(this,this.context,{},this,customs)

          
          for (let custom of customs){

            custom.render()
          }
          let localdata=Object.assign({},this.localdata)
          //fors principal
          let n_foor=0;
          for (let loop of this.fors){
            
            process_for(this,loop,this.context,localdata,n_foor)
            n_foor+=1

            
            

          }
          let n_if=0;
          console.log("HHHHHHHHHHHHH ",this.ifs)
          for (let if_node of this.ifs){
            
            process_if(this,
              if_node,
              this.context,
              localdata,
              n_if)

            n_if+=1;
            
          }
          
        }
        attributeChangedCallback(){
          
        }
        render(localdata={}){
          /*Si se usa por render quiere decir que es un sub elemento*/
        }

      }
      if (name){
        window.customElements.define("f-"+name.toLowerCase(),Component)

      }
      
    }
    
    

  }

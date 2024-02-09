# para el idratado se usa una combinacion de serializacion en base64,

f-model="variable"
f-value:base64="sdkgnskvnshgñnhñ4mnhpobhbsdh==="
para no serlaizado
f-value="'valor de string'"

# para los hidratados cuyo valor es el contenido del propio html

se utilizara la etiqueta f-html sin ninun valor

# Tipos de vista

Existen don tipos de vista:
	* las informativas que se sirven por server side rendering que requieren reidratacion
	* la de aplicacion, que devuelven un layout o snippet, estos layouts se guardan en un store de layouts para no ser solicitados nuevamente, estos se renderizan desde la aplicacion



class Component:
	def DATA(self):
		return {"valiable":None}


# Modificadores HTML

html```
<meta f-mode="cache" >
```
Esta etiqueta significa que el manejador de la aplicacion hara uso del service worker para no volver a solicitar esta pagina una segunda vez ya que sus componentes fueron ya cargados en la cache del manejador de la aplicacion flastfront

# Directivas

*f-name* Esta directiva es usada para dar el nombre de componente a un snippet, esto sera usado para registrarlo en la aplicacion 

*f-if* Esta directiva es usada para dar el nombre de componente a un snippet, esto sera usado para registrarlo en la aplicacion 

*f-elif* Esta directiva es usada para dar el nombre de componente a un snippet, esto sera usado para registrarlo en la aplicacion 

*f-else* Esta directiva es usada para dar el nombre de componente a un snippet, esto sera usado para registrarlo en la aplicacion 

*f-for* Esta directiva es usada para dar el nombre de componente a un snippet, esto sera usado para registrarlo en la aplicacion 

*f-model* Esta directiva es usada para dar el nombre de componente a un snippet, esto sera usado para registrarlo en la aplicacion 

*f-value* Esta directiva es usada para dar el nombre de componente a un snippet, esto sera usado para registrarlo en la aplicacion 

*f-component* Esta directiva es usada para dar el nombre de componente a un snippet, esto sera usado para registrarlo en la aplicacion 

*f-show* Esta directiva es usada para dar el nombre de componente a un snippet, esto sera usado para registrarlo en la aplicacion 

*f-html* Esta directiva es usada para dar el nombre de componente a un snippet, esto sera usado para registrarlo en la aplicacion 

*f-text* Esta directiva es usada para dar el nombre de componente a un snippet, esto sera usado para registrarlo en la aplicacion 



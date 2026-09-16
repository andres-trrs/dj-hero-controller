extends Node2D

var udp := PacketPeerUDP.new()
var puerto = 5005

# Variables de estado
var v = 0
var r = 0
var a = 0
var scratch = 0

# NUEVO: Bloqueador hasta que nos conectemos
var conectado = false 

var dedos_activos = {}
var ancho_pantalla = 0.0

func _ready():
	# Ya no conectamos aquí, solo preparamos las medidas
	ancho_pantalla = get_viewport_rect().size.x
	print("Esperando IP. Ancho total: ", ancho_pantalla)

# ESTA FUNCIÓN SE EJECUTA CUANDO TOCAS EL BOTÓN DE CONECTAR
func _on_boton_conectar_pressed():
	# 1. Leer el texto de la caja
	var ip_ingresada = $UI/InputIP.text
	
	# 2. Conectar al servidor UDP
	udp.connect_to_host(ip_ingresada, puerto)
	conectado = true # Liberamos los controles
	
	# 3. Ocultar todo el menú visualmente
	$UI.hide()
	print("Conectado a IP: ", ip_ingresada)

func _input(event):
	# Si no hemos puesto la IP, ignoramos los toques
	if not conectado:
		return
		
	var modificado = false
	
	# 1. DETECTAR TOQUES MULTIPLES (Pulsar y soltar)
	if event is InputEventScreenTouch:
		var id = event.index
		
		if event.pressed:
			dedos_activos[id] = event.position.x
			modificado = actualizar_botones(event.position.x, 1)
		else:
			if dedos_activos.has(id):
				modificado = actualizar_botones(dedos_activos[id], 0)
				dedos_activos.erase(id)
	
	# 2. DETECTAR SCRATCH (Deslizamiento continuo)
	elif event is InputEventScreenDrag:
		scratch = int(event.relative.y)
		modificado = true

	# 3. EMPAQUETAR Y ENVIAR AL SERVIDOR
	if modificado:
		var mensaje = str(v) + "|" + str(r) + "|" + str(a) + "|" + str(scratch)
		udp.put_packet(mensaje.to_utf8_buffer())
		
		if scratch != 0:
			scratch = 0

func actualizar_botones(pos_x, estado) -> bool:
	var cuarto = ancho_pantalla / 4.0
	var cambio = false
	
	if pos_x < cuarto:
		pass 
	elif pos_x < cuarto * 2.0:
		v = estado
		cambio = true
	elif pos_x < cuarto * 3.0:
		r = estado
		cambio = true
	else:
		a = estado
		cambio = true
		
	return cambio

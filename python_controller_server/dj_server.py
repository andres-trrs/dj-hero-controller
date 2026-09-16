import socket
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController

# Configuración de Red
IP = "0.0.0.0"
PUERTO = 5005

# Inicializar controladores de Windows
teclado = KeyboardController()
raton = MouseController()

# Mapeo de teclas (puedes cambiarlas por las que más te acomoden)
TECLA_VERDE = 'j'
TECLA_ROJA  = 'k'
TECLA_AZUL  = 'l'

# Memoria para guardar qué botones ya están presionados
estado_ant = [0, 0, 0]

# Crear el servidor UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PUERTO))

print("🎛️  Servidor Traductor DJ Hero ACTIVO.")
print(f"Escuchando en el puerto {PUERTO}... (Presiona Ctrl+C para salir)\n")

try:
    while True:
        datos, _ = sock.recvfrom(1024)
        # El mensaje llega como "1|0|0|-25", lo separamos por la barra vertical "|"
        mensaje = datos.decode('utf-8').split('|')
        
        # Nos aseguramos de que el paquete llegó completo
        if len(mensaje) == 4:
            v = int(mensaje[0])
            r = int(mensaje[1])
            a = int(mensaje[2])
            scratch = int(mensaje[3])
            
            # --- LÓGICA DE BOTONES (Teclado) ---
            # Botón Verde
            if v == 1 and estado_ant[0] == 0: teclado.press(TECLA_VERDE)
            elif v == 0 and estado_ant[0] == 1: teclado.release(TECLA_VERDE)
            
            # Botón Rojo
            if r == 1 and estado_ant[1] == 0: teclado.press(TECLA_ROJA)
            elif r == 0 and estado_ant[1] == 1: teclado.release(TECLA_ROJA)
            
            # Botón Azul
            if a == 1 and estado_ant[2] == 0: teclado.press(TECLA_AZUL)
            elif a == 0 and estado_ant[2] == 1: teclado.release(TECLA_AZUL)
            
            # Actualizamos la memoria
            estado_ant = [v, r, a]
            
            # --- LÓGICA DE SCRATCH (Ratón) ---
            if scratch != 0:
                # Movemos el cursor físico de Windows en el eje Y (arriba/abajo).
                # Si el scratch se siente muy lento en el juego, puedes multiplicar este valor (ej: scratch * 2)
                raton.move(0, scratch)

except KeyboardInterrupt:
    print("\nServidor apagado exitosamente. ¡Nos vemos!")
finally:
    sock.close()
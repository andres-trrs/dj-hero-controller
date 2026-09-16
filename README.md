# 🎧 DJ Hero Controller

Convierte tu **celular** en un controlador de turntable estilo *DJ Hero* para jugar **DJ Hero en el emulador RPCS3 (PS3)** desde tu PC. La pantalla táctil del teléfono se divide en tres botones de color (verde, rojo, azul) y detecta el gesto de "scratch" arrastrando el dedo. Todo eso viaja por WiFi hasta un pequeño servidor en Python que lo traduce en pulsaciones de teclado y movimiento de mouse, que a su vez RPCS3 interpreta como un mando de PS3.

```
┌────────────┐   WiFi (UDP:5005)   ┌──────────────────┐   Teclado / Mouse   ┌───────────┐
│  App Godot │ ───────────────────▶│ Servidor Python   │────────────────────▶│  RPCS3    │
│ (celular)  │                     │ (dj_server.py)    │                     │ (DJ Hero) │
└────────────┘                     └──────────────────┘                     └───────────┘
```

## 📁 Estructura del proyecto

| Archivo / Carpeta | Descripción |
|---|---|
| `main.gd` / `main.tscn` | App de Godot 4 que se instala en el celular. Dibuja los 3 botones táctiles y envía los datos por UDP. |
| `python_controller_server/dj_server.py` | Servidor UDP que corre en la PC. Traduce los mensajes del celular a pulsaciones de teclado (`J`, `K`, `L`) y movimiento de mouse. |
| `rpcs3_controller_config/Default.yml` | Perfil de control de RPCS3 (handler **Keyboard**) ya configurado para que esas teclas y el mouse funcionen como el mando de PS3 dentro de DJ Hero. |

---

## ✅ Requisitos

- **PC con Windows** con [RPCS3](https://rpcs3.net/) instalado y el juego DJ Hero funcionando.
- **Python 3** instalado en la PC, con la librería `pynput`:
  ```
  pip install pynput
  ```
- **Celular Android** con la app exportada desde este proyecto de **Godot 4** (o el editor de Godot para correrla directo).
- PC y celular deben quedar **en la misma red WiFi**.

---

## 🚀 Cómo se usa (paso a paso)

### 1. Prepara el celular
Conecta el celular a la PC con el **cable USB** (para mantenerlo cargado durante la partida) y activa el **Punto de acceso WiFi / Hotspot** del teléfono. La PC se conectará a esta red WiFi que crea el celular.

> El cable USB es solo para no quedarte sin batería a mitad de canción — la comunicación entre celular y PC va por WiFi, no por USB.

### 2. Conecta la PC al hotspot y busca su IP
En la PC, conéctate a la red WiFi que acaba de crear el celular. Luego abre una consola (`cmd`) y escribe:

```
ipconfig
```

Busca el adaptador WiFi conectado al hotspot del celular y anota la **dirección IPv4** (ejemplo: `192.168.43.100`). Esa es la IP de tu PC dentro de la red del celular, y es la que el celular necesita para poder enviarle los datos.

### 3. Ingresa la IP en la app de Godot
Abre la app en el celular. Vas a ver un campo de texto y un botón **"Conectar"**. Escribe ahí la IP que anotaste en el paso anterior y presiona **Conectar**. El menú desaparecerá y quedará la pantalla lista para tocar los botones.

### 4. Lanza el servidor y juega
En la PC, dentro de la carpeta `python_controller_server`, ejecuta:

```
python dj_server.py
```

Deberías ver el mensaje `🎛️ Servidor Traductor DJ Hero ACTIVO.`. Abre RPCS3, carga el perfil de mando de la carpeta `rpcs3_controller_config` (o ajusta uno propio con el mismo mapeo, ver más abajo) y arranca DJ Hero. Ya puedes tocar los botones de color y hacer scratch en el celular para jugar. 🎶

---

## 🎮 Cómo funciona el mapeo de controles

### En el celular (Godot)
La pantalla se divide en 4 franjas verticales iguales:

| Franja | Acción |
|---|---|
| 1ª (más a la izquierda) | Sin uso |
| 2ª | Botón **Verde** |
| 3ª | Botón **Rojo** |
| 4ª (más a la derecha) | Botón **Azul** |

Arrastrar el dedo por la pantalla (en cualquier zona) genera el gesto de **scratch**, calculado con el movimiento vertical (`relative.y`) del arrastre.

Cada vez que cambia algo, la app envía por UDP al puerto `5005` un mensaje con el formato:

```
verde|rojo|azul|scratch
```

Ejemplo: `1|0|0|-14` significa "botón verde presionado, sin scratch en rojo/azul, moviendo el scratch -14".

### En la PC (`dj_server.py`)
El servidor escucha ese puerto y traduce:

| Señal recibida | Acción en Windows |
|---|---|
| Verde | Tecla `J` |
| Rojo | Tecla `K` |
| Azul | Tecla `L` |
| Scratch | Mueve el mouse en el eje Y (arriba/abajo) |

### En RPCS3 (`Default.yml`)
El perfil de mando usa el handler **Keyboard** y mapea esas mismas teclas al mando virtual de PS3:

| Tecla / entrada | Botón de PS3 |
|---|---|
| `J` | ✕ Cross |
| `K` | ○ Circle |
| `L` | ▢ Square |
| Mouse arriba / abajo | Left Stick Up / Down |

Es decir: los botones de color del celular terminan presionando ✕ / ○ / ▢, y el gesto de scratch mueve el stick izquierdo, que es lo que DJ Hero usa para el turntable.

---

## 🛠️ Personalización

- **Cambiar las teclas**: edita las constantes `TECLA_VERDE`, `TECLA_ROJA`, `TECLA_AZUL` en `dj_server.py`. Si las cambias, recuerda actualizar también el mapeo en el perfil de RPCS3.
- **Sensibilidad del scratch**: en `dj_server.py`, la línea `raton.move(0, scratch)` puedes multiplicarla (ej. `scratch * 2`) si el giro del turntable se siente muy lento en el juego.
- **Puerto de red**: si el `5005` está ocupado, cámbialo tanto en `main.gd` (variable `puerto`) como en `dj_server.py` (variable `PUERTO`).

---

## 🩺 Problemas comunes

- **No conecta / no pasa nada al tocar los botones**: verifica que la PC y el celular estén en la misma red (el hotspot del celular) y que el servidor Python esté corriendo *antes* de tocar la pantalla.
- **La IP cambia cada vez**: es normal, el hotspot puede asignar IPs distintas. Repite el paso 2 (`ipconfig`) cada vez que reinicies el hotspot.
- **RPCS3 no reacciona**: confirma que el handler de mando en RPCS3 esté puesto en **Keyboard** y que la ventana del emulador tenga el foco mientras juegas.
- **El antivirus/firewall bloquea el puerto**: permite conexiones entrantes UDP en el puerto `5005` para `python.exe` en el Firewall de Windows.

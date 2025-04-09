# Hex-IA

Un juego de Hex implementado en Python con capacidades de IA.

## Descripción

Hex es un juego de estrategia para dos jugadores que se juega en un tablero hexagonal. El objetivo es crear un camino continuo que conecte los lados opuestos del tablero con fichas del mismo color.

- Jugador 1 (🔴): Conecta el lado superior con el inferior
- Jugador 2 (🔵): Conecta el lado izquierdo con el derecho

## Características

- Tablero de tamaño personalizable
- Tres modos de juego:
  1. Humano vs Humano
  2. Humano vs IA
  3. IA vs IA
- Interfaz de consola intuitiva
- Visualización clara del tablero

## Requisitos

- Python 3.x

## Estructura del Proyecto

```
Hex-IA/
├── main.py         # Punto de entrada del juego
├── hex_board.py    # Implementación del tablero
├── player.py       # Clases de jugadores
└── utils.py        # Funciones de utilidad
```

## Cómo Jugar

1. Ejecuta el juego:
```bash
python main.py
```

2. Sigue las instrucciones en pantalla para:
   - Seleccionar el tamaño del tablero
   - Elegir el modo de juego
   - Realizar movimientos ingresando coordenadas (fila columna)

## Controles

- Para realizar un movimiento, ingresa las coordenadas en el formato: "fila columna"
- Ejemplo: "2 3" colocará una pieza en la fila 2, columna 3

## Reglas del Juego

1. Los jugadores se turnan para colocar piezas en el tablero
2. Una vez colocada una pieza, no se puede mover ni eliminar
3. Gana el primer jugador que forme un camino continuo entre sus lados correspondientes
4. No puede haber empate (excepto si el tablero se llena, lo cual es teóricamente imposible en un juego óptimo)
# Connect-4 con IA (Minimax y Expectimax)

Implementación completa del juego Connect-4 con inteligencia artificial usando los algoritmos **Minimax** con poda alfa-beta y **Expectimax**.

## 📁 Estructura del Proyecto

```
Connect-4/
  src/
    ├── __init__.py              # Paquete Python
    ├── config.py                # Constantes del juego (tamaño tablero, símbolos)
    ├── board.py                 # Lógica del tablero (movimientos, detección ganador)
    ├── evaluation.py            # Función heurística de evaluación
    ├── minimax_search.py        # Algoritmo Minimax con poda alfa-beta
    ├── expectimax_search.py     # Algoritmo Expectimax (oponente estocástico)
    ├── agents.py                # Agentes: Minimax, Expectimax, Random
    ├── experiments.py           # Scripts para experimentos IA vs IA
    ├── main_cli.py              # Interfaz por consola
    └── main_gui.py              # Interfaz gráfica (Tkinter)
```

## 🎮 Cómo Jugar

### Opción 1: Interfaz Gráfica (Recomendado) 🖱️

```bash
python -m src.main_gui
```

**Características de la GUI:**
- ✨ Interfaz visual intuitiva con colores
- 🎯 Selección de tipo de IA (Minimax o Expectimax)
- 📊 Nivel de dificultad ajustable (profundidad 2-6)
- 🎨 Elige tu símbolo (O rojo o X amarillo)
- 🖱️ Juega con clics del mouse
- 💡 Resaltado de columnas válidas

### Opción 2: Interfaz de Consola 💻

```bash
python -m src.main_cli
```

Interfaz basada en texto para jugar desde la terminal.

## 🧪 Experimentos (IA vs IA)

Para ejecutar experimentos automáticos y obtener estadísticas:

```bash
python -m src.experiments
```

Esto ejecutará:
- **Minimax vs Random**: 20 partidas
- **Expectimax vs Random**: 20 partidas
- Mostrará victorias, derrotas y empates

## 🤖 Tipos de IA

### 1. Minimax con Poda Alfa-Beta
- Asume oponente **perfecto** (siempre elige el mejor movimiento)
- Explora el árbol de juego completo hasta cierta profundidad
- **Poda alfa-beta**: optimización que elimina ramas innecesarias
- Ideal para juego competitivo

### 2. Expectimax
- Modela oponente **estocástico** (elige movimientos aleatoriamente)
- Calcula valor **esperado** de las posiciones
- Útil cuando el oponente no es perfectamente racional
- Bueno contra jugadores impredecibles

### 3. Random
- Elige movimientos completamente al azar
- Usado para pruebas y comparaciones

## 🎯 Función Heurística

La evaluación del tablero considera:

1. **Ventanas de 4 casillas**:
   - 4 fichas propias: +1000 puntos (victoria)
   - 3 fichas + 1 vacía: +10 puntos (amenaza)
   - 2 fichas + 2 vacías: +5 puntos (potencial)
   - 3 fichas del oponente + 1 vacía: -80 puntos (bloquear)

2. **Control del centro**: +3 puntos por ficha en columna central

3. **Direcciones evaluadas**:
   - Horizontales
   - Verticales
   - Diagonales (\ y /)

## ⚙️ Configuración

Puedes modificar los parámetros en `src/config.py`:

```python
ROWS = 6          # Filas del tablero
COLS = 7          # Columnas del tablero
EMPTY = "."       # Símbolo casilla vacía
MAX_PLAYER = "O"  # Jugador MAX
MIN_PLAYER = "X"  # Jugador MIN
```

## 📊 Ajustar Dificultad

En la **interfaz gráfica**, usa el slider de dificultad.

Para modificar en código:

```python
# En main_gui.py o main_cli.py
agent = MinimaxAgent(depth=6)  # Más profundo = más difícil (y lento)
agent = ExpectimaxAgent(depth=4)  # Profundidad recomendada: 4-5
```

**Nota**: Profundidad mayor = IA más fuerte pero movimientos más lentos.

## 🛠️ Requisitos

- **Python 3.7+**
- **Tkinter** (incluido con Python en la mayoría de instalaciones)

Si no tienes Tkinter:
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora**: `sudo dnf install python3-tkinter`
- **macOS/Windows**: Ya viene incluido

## 🚀 Ejemplo de Uso Rápido

```bash
# 1. Jugar con interfaz gráfica
python -m src.main_gui

# 2. Jugar en consola
python -m src.main_cli

# 3. Ejecutar experimentos
python -m src.experiments
```

## 🎓 Propósito Académico

Este proyecto implementa conceptos de:
- Teoría de juegos
- Búsqueda adversarial
- Algoritmos Minimax y Expectimax
- Funciones heurísticas
- Optimización con poda alfa-beta

Ideal para proyectos de Inteligencia Artificial y Ciencias de la Computación.

## 📝 Notas

- El jugador **O (rojo)** siempre empieza primero
- La IA puede tardar unos segundos en profundidades altas (5-6)
- Puedes interrumpir los experimentos con `Ctrl+C`

---

¡Disfruta jugando contra la IA! 🎮🤖


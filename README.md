# Cuenta Gotas - PySide6

Aplicación de escritorio  en **Python** usando **PySide6** que funciona como un temporizador estilo “Cuenta Gotas” con sonidos de alerta .

## Características

- Temporizador con horas y minutos configurables.
- Sonidos de alerta cada intervalo definido.
- Interfaz gráfica  semi transparente.
- Botón de play/pause con cambio de color según estado.
- Ventana flotante y sin bordes, siempre visible encima de otras ventanas.
- Inputs con validación de números (minutos y horas).

## Tecnologías

- Python 3.x  
- PySide6 (Qt for Python)  

## Instalación y uso

1. Clonar el repositorio:  
   ```bash
   git clone https://github.com/Ashienty/CuentaGotas.git
Instalar dependencias:
pip install PySide6
Ejecutar la aplicación:
python main.py
Nota
Funciona en Windows debido a la dependencia winsound. Para otros sistemas, se debería reemplazar por otra librería de sonido compatible.

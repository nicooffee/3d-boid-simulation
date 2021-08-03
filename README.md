# Información y requerimientos

Script en python para la simulación del comportamiento flocking en 3D. Para ejecutar correctamente la aplicación se requieren la librerías `PyOpenGL` y `PyOpenGL_accelerate` de OpenGL en python. La librería se instala mediante `pip`:

```bash
    pip install PyOpenGL PyOpenGL_accelerate
```
# Ejecución

Para ejecutra el script de la simulación, existen dos opciones. Para ejecutar la simulación con parámetros definidos por el usuario ejecutar la siguiente línea en la raíz de la aplicación

- `CANT_FLOCK`  : Cantidad de flocks en la simulación
- `LARGO_FLOCK` : Cantidad de boids por flock.
- `RADIO_VISION`: Radio de visión de cada boid.

```bash 
    python3 main.py [CANT_FLOCK] [LARGO_FLOCK] [RADIO_VISION]
```

Para ejecutar con los valores predeterminados, ejecutar la siguiente línea. Los valores predeterminados son `CANT_FLOCK = 5`, `LARGO_FLOCK = 30`, `RADIO_VISION = 150`

```bash 
    python3 main.py
```
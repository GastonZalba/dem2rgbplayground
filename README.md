# demtorgb
Script para poder evaluar evaluar codificaciones RGB de modelos de terreno (DEM) [mapbox](https://docs.mapbox.com/data/tilesets/guides/access-elevation-data/) y [terrarium](https://www.mapzen.com/blog/terrain-tile-service/) y/o posibilitar la creación de ecuaciones customizadas. Está armado principalmente para testear los rangos de valores aceptados y resolución de cada una de éstas (a falta de una documentación clara), chequeando en prints valores de entrada y salida (tras codificación/decodificación). 

También permite procesar rápidamente un geotiff DEM a formato RGB usando esas codificaciones.

## Requerimientos
- rasterio, gdal y numpy

## Uso
- Testeo de valor de entrada y salida:
    - Modificar la variable `TEST_VALUE` para evaluar X valor de entrada y salida
    - Desde consola: `python demtorgb.py mapbox|terrarium` para obtener prints con la entrada/salida del valor de testeo. 
    - El proceso también genera un tif con un gradiente predefinido para poder verificar visualmente la escala de colores.

- Procesar DEM:
    - Para hacer una previsualización rápida de cómo se vería un DEM: `python demtorgb.py mapbox|terrarium [INPUT_FILE]`, lo cual generará un archivo output.tif con la codificación seleccionada.

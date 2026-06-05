# Taller 4 - Disney API, MongoDB y EDA

 El objetivo es simular un flujo basico de ciencia de datos: consumir una API pública, almacenar los datos crudos en MongoDB y luego analizarlos con un archivo `.ipynb`.

## API utilizada

Se utilizó la Disney API:

https://api.disneyapi.dev/character

Esta API entrega información de personajes de Disney. Cada registro incluye campos como nombre, peliculas, cortos, series de television, videojuegos, atracciones de parques, aliados, enemigos e imagen del personaje.

## Objetivo 

Se busca analizar 100 personajes de Disney para identificar en que tipos de medios aparecen con mayor frecuencia. Para esto se descargaron los datos desde la API, se guardaron sin modificar en MongoDB y luego se procesaron en un DataFrame de Pandas para calcular estadisticas y crear visualizaciones.

## Estructura del repositorio

- `ingesta.py`: script encargado de consumir la API y guardar los datos crudos en MongoDB.
- `analisis.ipynb`: notebook donde se leen los datos desde MongoDB, se transforman y se realiza el analisis exploratorio.
- `requirements.txt`: lista de librerias necesarias para ejecutar el proyecto.
- `.gitignore`: archivo para excluir el entorno virtual, variables de entorno y archivos temporales.

## Base de datos utilizada

- Base de datos: `taller4_db`
- Coleccion: `raw_data`

La colección almacena los documentos crudos de personajes tal como llegan dentro de la respuesta de la API. La información de paginación se usa solo para navegar entre páginas, pero los registros guardados son los personajes.

## Como ejecutar el proyecto

1. Clonar el repositorio.
2. Crear y activar un entorno virtual.
3. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

4. Verificar que MongoDB este activo localmente en:

```text
mongodb://localhost:27017/
```

5. Ejecutar la ingesta:

```bash
python ingesta.py
```

6. Abrir y ejecutar el notebook:

```bash
jupyter notebook analisis.ipynb
```

## Explicacion de `ingesta.py`

El archivo `ingesta.py` define las constantes principales del proyecto: la URL de la API, la conexion local a MongoDB, el nombre de la base de datos, el nombre de la colección y la cantidad mínima de registros requerida.

La funcion `descargar_personajes()` hace peticiones a la Disney API usando `requests`. Como la API entrega los personajes por páginas, el script usa el campo `info.nextPage` para avanzar a la siguiente página hasta reunir al menos 100 personajes. Cada personaje se agrega a una lista sin modificar su estructura original.

La funcion `guardar_en_mongodb()` se conecta a MongoDB con `MongoClient`, selecciona la base de datos `taller4_db` y la coleccion `raw_data`. Luego limpia la coleccion con `delete_many({})` para evitar duplicados y guarda los 100 documentos con `insert_many()`.

La funcion `main()` coordina todo el proceso: descarga los personajes, los inserta en MongoDB y muestra en consola cuántos documentos fueron descargados, insertados y almacenados.

## Explicacion de `analisis.ipynb`

El notebook empieza importando las librerias necesarias: `pymongo` para conectarse a MongoDB, `pandas` para construir el DataFrame, y `matplotlib`/`seaborn` para las gráficas.

Despues se conecta a la base de datos `taller4_db` y a la coleccion `raw_data`. Con `count_documents({})` se verifica que existan 100 documentos almacenados.

Luego se leen los documentos con `collection.find()` y se convierten en un DataFrame llamado `df_raw`. Este DataFrame contiene los datos crudos. A partir de el se crea un segundo DataFrame llamado `df`, donde se seleccionan y transforman variables utiles para el análisis.

Como varios campos de la API son listas, se creo la función `contar_lista()`. Esta función cuenta cuántos elementos tiene cada lista. Por ejemplo, permite saber cuántas peliculas, series, videojuegos o atracciones tiene registrado cada personaje.

Las variables analizadas fueron:

- `name`: nombre del personaje.
- `films_count`: cantidad de peliculas registradas.
- `short_films_count`: cantidad de cortos registrados.
- `tv_shows_count`: cantidad de series de television registradas.
- `video_games_count`: cantidad de videojuegos registrados.
- `park_attractions_count`: cantidad de atracciones de parques registradas.
- `allies_count`: cantidad de aliados registrados.
- `enemies_count`: cantidad de enemigos registrados.
- `has_image`: indica si el personaje tiene imagen.
- `total_appearances`: suma de apariciones en peliculas, cortos, series, videojuegos y atracciones.
- `has_films`: clasifica si el personaje tiene o no peliculas registradas.

Después se realiza la inspeccion basica del DataFrame con `head()`, `info()` y `isnull().sum()`. Esto permite revisar las primeras filas, los tipos de datos y si hay valores nulos.

## Insights calculados

En el notebook se calcularon cinco datos relevantes:

1. Promedio de peliculas por personaje.
2. Personaje con más videojuegos registrados.
3. Personaje con más apariciones registradas en total.
4. Cantidad de personajes que no aparecen en ninguna pelicula.
5. Personaje con más peliculas registradas.

Tambien se calculo el total de apariciones por tipo de medio para comparar peliculas, series, videojuegos, cortos y atracciones.

## Visualizaciones realizadas

El notebook incluye tres graficos:

1. Grafico de torta: muestra el porcentaje de apariciones por tipo de medio.
2. Grafico de barras: muestra el top 10 de personajes con más apariciones en videojuegos.
3. Histograma: muestra la distribucion del total de apariciones por personaje.

## Conclusiones generales

El análisis permite observar que los personajes de Disney no aparecen con la misma frecuencia en todos los tipos de medios. En los 100 personajes analizados, las series de television y las peliculas concentran una parte importante de las apariciones registradas. Tambián se encontro que algunos personajes, como Baloo, tienen una presencia destacada en videojuegos y en el total de apariciones. Ademas, una cantidad considerable de personajes no tiene peliculas registradas, lo que muestra que la API contiene personajes asociados a otros medios como series, videojuegos o atracciones de parques.

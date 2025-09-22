# 🧬 Proyecto conversión ADN a Música 🎵

Este proyecto es un script de Python que transforma una secuencia de ADN en un archivo de música MIDI. El programa identifica un "Marco de Lectura Abierto" (ORF) en la secuencia y mapea los nucleótidos a notas y duraciones musicales, creando una melodía única basada en la información genética.

# ⚙️ Requisitos

Para ejecutar este script, necesitas tener instalado Python y la biblioteca pretty_midi. Puedes instalarla usando pip:

```
pip install pretty_midi

```

# 🚀 Cómo Usar

Guarda el código fuente en un archivo llamado adn_a_musica.py.

Abre una terminal o línea de comandos.

Ejecuta el script de la siguiente manera:

```
python adn_a_musica.py
```

El programa te pedirá que introduzcas la secuencia de ADN, la nota tónica, el modo (mayor o menor) y el tempo. Sigue las instrucciones para generar tu canción.

Ejemplo de entrada:

Secuencia de ADN: atgacgctacgctag

Nota Tónica: C

Modo: mayor

Tempo: 120

Una vez completado el proceso, se creará un archivo llamado cancion_adn.mid en la misma carpeta, que podrás reproducir con cualquier reproductor de archivos MIDI.

# 🧠 Lógica del Script


1. Búsqueda del Marco de Lectura Abierto (ORF)
El programa busca el primer codón de inicio (ATG) y el primer codón de parada (TAA, TGA o TAG) para delimitar el ORF. Esto asegura que solo se transcribe una porción biológicamente relevante del ADN. Si no encuentra un ORF válido, muestra un error.

2. Mapeo de Nucleótidos a Música
Los nucleótidos (A, G, C, T) dentro del ORF se mapean a elementos musicales específicos: 

    * A se mapea a la nota tónica del acorde.

    * G se mapea a la tercera del acorde.

    * C se mapea a la quinta del acorde.

    * T se mapea a la quinta del acorde (para completar la triada).

La duración de cada nota también se determina por los nucleótidos, siguiendo un patrón de equivalencias (por ejemplo, A = blanca, G = negra, etc.).


3. Generación del Archivo MIDI
Finalmente, los datos musicales generados se utilizan para crear un archivo .mid usando la biblioteca pretty_midi. Se establece el tempo y se añaden las notas con su tono y duración correspondientes para que puedan ser interpretadas por un instrumento (en este caso, un piano).
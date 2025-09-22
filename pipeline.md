# Pipeline de Conversión de Secuencias de ADN a Música

El pipeline desarrollado para la conversión de secuencias de ADN en representaciones musicales sigue varios pasos lógicos que permiten transformar la información genética en una pieza musical. A continuación, se describe el flujo de trabajo en detalle:

## 1. Entrada de Datos por el Usuario

El proceso comienza con la entrada de la secuencia de ADN por parte del usuario. El programa acepta secuencias de ADN con una longitud máxima de 5000 nucleótidos (nt). Posteriormente, el usuario selecciona los parámetros musicales para la conversión:

- **Nota tónica**: la raíz de la tonalidad
- **Modo**: mayor o menor
- **Tempo**: la velocidad de la música

## 2. Detección del Marco de Lectura

Una vez ingresada la secuencia de ADN, el algoritmo localiza el primer codón de inicio (ATG) y avanza a través de la secuencia de tres en tres nucleótidos (en marco de lectura) para encontrar un codón de parada (TAA, TGA o TAG). Si no se detecta ningún codón de parada en el marco de lectura correcto, se muestra un mensaje de error.

## 3. Verificación del ORF

Si la longitud del marco de lectura abierto (ORF) entre el codón de inicio (ATG) y el primer codón de parada es menor a 10 codones, se arroja un mensaje de error. Este paso asegura que la secuencia de ADN sea lo suficientemente larga para generar una representación musical adecuada.

## 4. Conversión Musical de los Codones

Una vez validada la secuencia, cada codón de inicio y codón de parada se traduce a un acorde musical basado en la tónica seleccionada por el usuario.

El acorde de tónica se utiliza tanto para el codón de inicio como para el de parada, y se toca durante un compás completo.

A continuación, se analiza cada codón intermedio. Cada codón es traducido a un aminoácido específico, que se busca en una tabla de correspondencias, y luego se asigna a un grado musical dentro del modo elegido (mayor o menor). La tabla de correspondencias de aminoácidos a grados es la siguiente:

| Tipo de Aminoácido | Grado en Modo Mayor | Grado en Modo Menor |
|--------------------|---------------------|---------------------|
| No polares         | I                   | I                   |
| Positivos          | VI                  | IVm                 |
| Polares            | V                   | Vm                  |
| Negativos          | IIIm                | VI                  |
| Aromáticos         | IIm                 | III                 |

Por ejemplo, si el codón TAA corresponde a un aminoácido polar como la serina, en el modo menor la nota correspondiente será Vm. Esto se traduce a la tetrada de La menor (Mi-Sol-Si-Re).

## 5. Reglas Melódicas y Armónicas

### Reglas de la Melodía:

Cada letra del codón (A, G, C, T) determina una característica de la nota musical:

- **A**: Primera nota de la tetrada (tónica)
- **G**: Tercera del acorde
- **C**: Quinta del acorde
- **T**: Séptima del acorde

De acuerdo con el ejemplo anterior (TAA → Mi-Sol-Si-Re), la letra "T" indicará que la séptima (Re) se debe tocar.

### Reglas de la Duración de las Notas:

La duración de cada nota se asigna según la letra del codón de la siguiente manera:

- **A**: blanca (2 tiempos)
- **G**: negra (1 tiempo)
- **C**: corchea (0.5 tiempos)
- **T**: dependerá de la letra anterior (A: silencio de blanca, G: silencio de negra, C: silencio de corchea, T: nota prolongada hasta completar el compás).

## 6. Estructura de la Melodía y Armonía

### Secuencia Melódica:

Para cada codón, la melodía se construye siguiendo las reglas mencionadas, y se asegura de que la duración total de las notas en un compás sea exactamente 4 tiempos.

### Cambio de Acorde:

Cuando se cambia de codón, el acorde correspondiente a la tónica se toca solo cuando se complete un compás de 4 tiempos. El acorde no se repite inmediatamente hasta que se llegue al siguiente codón.

### Finalización del Componente Musical:

Una vez que se llega al codón de parada, el acorde de tónica se toca de nuevo para cerrar la pieza musical, independientemente de si la melodía ha completado o no el compás.

## 7. Cierre del Componente Musical

Finalmente, el código toca el acorde de tónica por un compás completo (4 tiempos) al llegar al codón de parada, asegurando que la pieza musical se cierre correctamente.

import pretty_midi

# --- Mapeo y Lógica Musical ---

def mapear_letras_a_notas(letra, acorde):
    """
    Mapea la letra a una nota del acorde (triada).
    A: 1ra (tónica), G: 3ra, C: 5ta.
    T: Se mapea a la 5ta nota para ser funcional en triadas.
    """
    if letra == 'A':
        return acorde[0]  # Raíz (1er elemento)
    elif letra == 'G':
        return acorde[1]  # Tercera (2do elemento)
    elif letra == 'C':
        return acorde[2]  # Quinta (3er elemento)
    elif letra == 'T':
        return acorde[2]  # Mapeado a la quinta para evitar errores de índice
    
    return None

def mapear_letras_a_duracion(letra_duracion, letra_movimiento):
   
    """
    Mapea la letra a una duración o silencio.
    A: blanca (2), G: negra (1), C: corchea (0.5), T: variable
    """
    if letra_duracion == 'A':
        return 2.0  # Blanca
    elif letra_duracion == 'G':
        return 1.0  # Negra
    elif letra_duracion == 'C':
        return 0.5 # Corchea
    elif letra_duracion == 'T':
        if letra_movimiento == 'A':
            return -2.0  # Silencio de blanca
        elif letra_movimiento == 'G':
            return -1.0  # Silencio de negra
        elif letra_movimiento == 'C':
            return -0.5  # Silencio de corchea
        elif letra_movimiento == 'T':
            return 4.0 # Dejar sonando hasta completar el compás
    return 0

def nota_a_numero_midi(nota_str):
    """
    Convierte una nota musical (ej. 'C4') a un número MIDI.
    Esto es una implementación simplificada.
    """
    notas = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octava = int(nota_str[-1])
    nombre_nota = nota_str[:-1]
    
    if len(nombre_nota) > 1: # Para notas con sostenido como G#
        semitono = 1
        nombre_nota = nombre_nota[0]
    else:
        semitono = 0

    nota_base = notas.index(nombre_nota)
    return 12 * (octava + 1) + nota_base + semitono

def generar_cancion(cancion_data, tempo):
    """
    Crea un archivo MIDI a partir de la lista de notas y acordes.
    """
    midi_file = pretty_midi.PrettyMIDI(initial_tempo=tempo)
    piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    piano = pretty_midi.Instrument(program=piano_program)

    tiempo_actual = 0

    # Calcular la duración de una negra en segundos según el tempo
    duracion_negra = 60.0 / tempo

    for elemento in cancion_data:
        if elemento['tipo'] == 'acorde':
            for nota_str in elemento['notas']:
                # Asignamos una octava por defecto para que suene
                nota_midi = nota_a_numero_midi(f"{nota_str}4")

                # Ajustamos la duración de la nota acorde según el tempo
                duracion_nota = elemento['duracion'] * duracion_negra

                note = pretty_midi.Note(
                    velocity=100,
                    pitch=nota_midi,
                    start=tiempo_actual,
                    end=tiempo_actual + duracion_nota
                )
                piano.notes.append(note)
            if elemento['duracion'] > 0:
                tiempo_actual += duracion_nota
        
        elif elemento['tipo'] == 'nota':
            # Asignamos una octava por defecto para la melodía
            nota_midi = nota_a_numero_midi(f"{elemento['nota']}5")

            # Ajustamos la duración de la nota según el tempo
            duracion_nota = elemento['duracion'] * duracion_negra

            note = pretty_midi.Note(
                velocity=100,
                pitch=nota_midi,
                start=tiempo_actual,
                end=tiempo_actual + duracion_nota
            )
            piano.notes.append(note)
            tiempo_actual += duracion_nota

    midi_file.instruments.append(piano)
    midi_file.write('cancion_adn.mid')
    print("Archivo MIDI 'cancion_adn.mid' creado con éxito.")


# --- Lógica Principal del Pipeline ---

def procesar_adn(secuencia, nota_tonica, modo, tempo):
    """
    Procesa la secuencia de ADN y genera una canción basada en las reglas.
    """
    # 1. Validar la longitud de la secuencia
    if len(secuencia) > 5000:
        return "Error: La secuencia de ADN no debe ser mayor a 5000 nucleótidos."

    # 2. Encontrar el ORF
    secuencia_upper = secuencia.upper()
    start_codon = "ATG"
    stop_codons = ["TAA", "TGA", "TAG"]

    try:
        start_index = secuencia_upper.index(start_codon)
        end_index = -1
        for i in range(start_index, len(secuencia_upper), 3):
            codon = secuencia_upper[i:i+3]
            if codon in stop_codons:
                end_index = i
                break
        
        if end_index == -1:
            return "Error: No se encontró un codón de stop en el marco de lectura."

        orf = secuencia_upper[start_index:end_index + 3]
        if len(orf) < 30:
            return "Error: El ORF es menor a 10 codones."

    except ValueError:
        return "Error: No se encontró el codón de inicio (ATG)."

    # 3. Definir acordes y mapeos
    acordes_mayores = {
        'C': ['C', 'E', 'G'], 'G': ['G', 'B', 'D'], 'A': ['A', 'C#', 'E'],
        'D': ['D', 'F#', 'A'], 'E': ['E', 'G#', 'B'], 'F': ['F', 'A', 'C'],
        'B': ['B', 'D#', 'F#']
    }
    
    acordes_menores = {
        'C': ['C', 'D#', 'G'], 'A': ['A', 'C', 'E'], 'G': ['G', 'A#', 'D'],
        'D': ['D', 'F', 'A'], 'E': ['E', 'G', 'B'], 'F': ['F', 'G#', 'C'],
        'B': ['B', 'D', 'F#']
    }
    
    aminoacidos_a_grados = {
        'Nopolars': {'mayor': 'I', 'menor': 'Im'},
        'Positives': {'mayor': 'VI', 'menor': 'IVm'},
        'Polars': {'mayor': 'V', 'menor': 'Vm'},
        'Negatives': {'mayor': 'IIIm', 'menor': 'VI'},
        'Aromatics': {'mayor': 'IIm', 'menor': 'III'},
    }
    
    # 4. Iniciar la canción con el acorde tónica
    cancion_data = []
    
    if modo == 'mayor':
        acorde_tonica = acordes_mayores[nota_tonica]
    else:
        acorde_tonica = acordes_menores[nota_tonica]
        
    cancion_data.append({'tipo': 'acorde', 'notas': acorde_tonica, 'duracion': 4.0})

    # Mapeo simplificado de codones a tipos de aminoácidos (debería ser más completo)
    codon_a_aminoacido_tipo = {
        'GCT': 'Nopolars', 'GCA': 'Nopolars', 'GCG': 'Nopolars', 'GCC': 'Nopolars', 
        'CGT': 'Positives', 'CGC': 'Positives', 'CGA': 'Positives', 'CGG': 'Positives',
        'AGT': 'Polars', 'AGC': 'Polars', 'TCT': 'Polars', 'TCC': 'Polars',
        'GAT': 'Negatives', 'GAC': 'Negatives', 'GAA': 'Negatives', 'GAG': 'Negatives',
        'TGG': 'Aromatics', 'TTT': 'Aromatics', 'TTC': 'Aromatics', 'TAT': 'Aromatics',
        'TAC': 'Aromatics'
    }

    # 5. Iterar a través de los codones del ORF
    tiempo_compas = 0.0
    
    for i in range(0, len(orf) - 3, 3):
        codon = orf[i:i+3]
        
        # Determinar el tipo de aminoácido del codón
        aminoacido_tipo = codon_a_aminoacido_tipo.get(codon, 'Nopolars')
        
        # Mapear el grado musical y el acorde correspondiente
        grado_musical = aminoacidos_a_grados[aminoacido_tipo][modo]
        
        # Aquí se necesita un mapeo más detallado de grados a acordes
        # Para simplificar, usamos la tónica como base para todos los acordes
        acorde_actual = acordes_mayores[nota_tonica] if modo == 'mayor' else acordes_menores[nota_tonica]
        
        # Lógica para la melodía y el compás
        letra_1 = codon[0]
        letra_2 = codon[1]
        letra_3 = codon[2]
        
        nota_melodica = mapear_letras_a_notas(letra_1, acorde_actual)
        duracion_nota = mapear_letras_a_duracion(letra_3, letra_2)

        # Si el compás está lleno, empezar un nuevo compás con el acorde
        if tiempo_compas >= 4.0:
            cancion_data.append({'tipo': 'acorde', 'notas': acorde_actual, 'duracion': 0})
            tiempo_compas = 0.0
        
        # Lógica para la duración de la nota
        if duracion_nota < 0:
            # Es un silencio
            cancion_data.append({'tipo': 'silencio', 'duracion': abs(duracion_nota)})
            tiempo_compas += abs(duracion_nota)
        else:
            # Es una nota, añadirla a la lista
            cancion_data.append({'tipo': 'nota', 'nota': nota_melodica, 'duracion': duracion_nota})
            tiempo_compas += duracion_nota

    # 6. Finalizar la canción con el acorde tónica
    cancion_data.append({'tipo': 'acorde', 'notas': acorde_tonica, 'duracion': 4.0})
    
    # Generar el archivo MIDI
    generar_cancion(cancion_data, tempo)

    return "La canción ha sido generada con éxito."


# --- Interfaz de Usuario (Main) ---

if __name__ == '__main__':
    print("🎵 ¡Bienvenido al generador de música de ADN! 🧬")
    print("------------------------------------------")

    secuencia_adn = input("Introduce la secuencia de ADN (máximo 5000 nt): ")
    nota_tonica = input("Elige la nota tónica (ej. A, C, G): ").upper()
    modo = input("Elige el modo (mayor o menor): ").lower()
    tempo_str = input("Elige el tempo (ej. 120): ")
    
    try:
        tempo = int(tempo_str)
        resultado = procesar_adn(secuencia_adn, nota_tonica, modo, tempo)
        print(f"\nResultado del proceso: {resultado}")
    except ValueError:
        print("Error: El tempo debe ser un número entero.")

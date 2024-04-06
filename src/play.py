from scamp import *
import reproducer_notes



def playSession(tempo: int, semitones_scale: list, times: list, octave:int, midi_init:str):

    # Verificar si todos los elementos en semitones_scale son números
    if not all(isinstance(x, (int, float)) for x in semitones_scale):
        raise ValueError("La escala debe contener solo números.")

    # Verificar si todos los elementos en times son números
    if not all(isinstance(x, (int, float)) for x in times):
        raise ValueError("Los tiempos deben contener solo números.")
    
    #Verificar si la octava esta dentro de rango
    if octave > 8 or octave < 1:
        raise ValueError("Octava fuera de rango (1-8)")
    
    #* Se establecen variables
    session = Session()    #Se crea la nueva sesion de trabajo
    session.tempo = tempo  #Se establece el tempo de la sesion
    semitones_scale = [0] + semitones_scale #Se le suma una nota vaciaa la  escala para comenzar desde la tonalidad
    piano1 = session.new_part("Piano")
    midi_notes = {
        "do": 12,
        "do♯": 13, "re♭": 13,
        "re": 14,
        "re♯": 15, "mi♭": 15,
        "mi": 16,
        "fa": 17,
        "fa♯": 18, "sol♭": 18,
        "sol": 19,
        "sol♯": 20, "la♭": 20,
        "la": 21,
        "la♯": 22, "si♭": 22,
        "si": 23,
    } #Se establecen las notas de la primer octava segun el estandar MIDI
    
    for note in midi_notes:
        # if octave == 1:
        #     continue
        midi_notes[note]+= (octave * 12) #Se le ajusta la primera octava de `midi_notes` segun `octave`
    #**
    

    reproducer_notes.piano_part(piano1, midi_notes[midi_init], semitones_scale, times)
    wait(.3) #Cooldown de 0.3 segundos para no cortar la ultima nota 
    
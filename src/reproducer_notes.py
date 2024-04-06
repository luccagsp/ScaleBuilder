
def midi_to_note(midi_value):
    notes = ["do", "do♯/re♭", "re", "re♯/mi♭", "mi", "fa", "fa♯/sol♭", "sol", "sol♯/la♭", "la", "la♯/si♭", "si"]
    note_index = (midi_value - 12) % 12
    return notes[note_index]


def piano_part(which_piano, initial_pitch, semitones_scale, times):
  
  # which_piano.play_note(initial_pitch, 1.0, times[0])
  pitch = initial_pitch
  
  for index, (semitone, time) in enumerate(zip(semitones_scale, times)):
    pitch+= semitone
    ##* Emulador de escala menor natural (?)
    # if index == 2 or index == 5 or index == 6: 
    #   which_piano.play_note(pitch -1 , 1.0, time)
    #   continue

    print(midi_to_note(pitch))
    which_piano.play_note(pitch, 1.0, time)
    # for index, semitone in enumerate(reversed(semitones_scale)):
    #   if index == 0: continue
    #   pitch-= semitone
    #   which_piano.play_note(pitch, 1.0, 0.5)

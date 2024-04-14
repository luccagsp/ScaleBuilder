def midi_to_note(midi_value):
    notes = ["do", "do♯/re♭", "re", "re♯/mi♭", "mi", "fa", "fa♯/sol♭", "sol", "sol♯/la♭", "la", "la♯/si♭", "si"]
    note_index = (midi_value - 12) % 12
    return notes[note_index]

def play_notes(which_piano, followingNotes, stdscr):
  volume = 1.0

  for note in followingNotes:
    stdscr.addstr(note['note'] + " ")
    stdscr.refresh()
    which_piano.play_note(note['midi'], volume, note['time'])

def calculate_notes(initial_pitch, semitones_scale, times):
  followingNotes = []
  pitch = initial_pitch
  
  # followingNotes.append({
  #   "midi": pitch,
  #   "note": midi_to_note(pitch)
  #   "time": time
  # })
  for semitone, time in zip(semitones_scale, times):
    followingNotes.append({
      "midi": pitch,
      "note": midi_to_note(pitch),
      "time": time
    })
    pitch+= semitone
    

  return followingNotes
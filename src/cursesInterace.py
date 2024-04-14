import threading
import time
import curses

import play
import notes_reproducer
from curses import wrapper

global cursor_now
cursor_now = -2

midi_notes = {
    "do": 12,
    "do♯": 13, "re♭": 13,"do#": 13, "reb": 13,
    "re": 14,
    "re♯": 15, "mi♭": 15,"re#": 15, "mib": 15,
    "mi": 16,
    "fa": 17,
    "fa♯": 18, "sol♭": 18,"fa#": 18, "solb": 18,
    "sol": 19,
    "sol♯": 20, "la♭": 20,"sol#": 20, "lab": 20,
    "la": 21,
    "la♯": 22, "si♭": 22,"la#": 22, "sib": 22,
    "si": 23,
} #Se establecen las notas de la primer octava segun el estandar MIDI

class askQuestion:
  def __init__(self, typeExpected:int|str|float, question:str ,placeholder:str, defaultReturnValue:list|str) -> None:
    global cursor_now
    cursor_now+=2
    
    self.wrkscr = curses.newwin(2, curses.COLS, cursor_now, 0)
    
    self.question = "• " + question
    self.toReturn: list = []
    self.typeExpected = typeExpected
    self.defaultReturnValue = defaultReturnValue
    self.placeholder = placeholder
    self.PLACEHOLDER = curses.color_pair(1)
    
    self.returnedValue = self.keyLoop()
  def keyLoop(self):
    wrkscr = self.wrkscr

    wrkscr.addstr(0, 0, self.question)
    wrkscr.move(1,12)

    while True:
      toReturn = self.toReturn
      if toReturn == []:
        wrkscr.addstr(1,0,self.placeholder, self.PLACEHOLDER)

      key = wrkscr.getkey() #Event locker
      
      #Basic re-builder
      wrkscr.clear()
      wrkscr.addstr(self.question)
      wrkscr.move(1,0)


      isFinished = self.isFinishedKey(key)
      if isFinished[0] == "Returned":
        if self.typeExpected == str: #String handler
          finalText = ""
          for semitone in isFinished[1]:
            finalText+= semitone
          return finalText
        
        return isFinished[1] #Default hander
      
      for index, semitone in enumerate(toReturn): #Se actualizan los caracteres en pantalla
        if index != 0 and index != len(toReturn) and self.typeExpected != str:
          wrkscr.addstr("-")
        elif index == 0 and self.typeExpected == int:
          wrkscr.addstr("0-")


        if type(semitone) == list and semitone[1] == 'to-point':
          semitone[1] == 'pointing'
          wrkscr.addstr( str( int(semitone[0]) ) + ".")
          continue

        wrkscr.addstr(str(semitone))
  def isFinishedKey(self, key):

    if key in ('\x00'): #Si key es null
      return ["Skipped"]
      
    if key in ("KEY_ENTER", '\r', '\n'): #Si codigos ASCII de Enter/Intro coincien...
      if self.toReturn == []:
        return ["Returned",self.defaultReturnValue]
      else:
        return ["Returned",self.toReturn]
    
    if key in ("KEY_BACKSPACE", '\b', '\x7f', '\x08'): 
        if len(self.toReturn) > 0 and type(self.toReturn[-1]) == list: #Compatibilidad con decimales
          self.toReturn[-1] = self.toReturn[-1][0]
          return ["Skipped"]
        if self.toReturn != []:
          self.toReturn.pop()
        return ["Skipped"]
    
    if len(self.toReturn) > 0 and  type(self.toReturn[-1]) == list and self.toReturn[-1][1] == "to-point" and ord(key) != 46:
      self.toReturn[-1] = (self.toReturn[-1][0] + (int(key) /10))
      return ["Skipped"]

    if key in ('.') and self.typeExpected == float:
      if type(self.toReturn[-1]) != list:
        self.toReturn[-1] = [self.toReturn[-1], "to-point"]
      return ["Skipped"]
    
    self.appendToReturnValue(key)
    return ["Skipped"]
  def appendToReturnValue(self, key):
    try:
      typeExpected = self.typeExpected
      if typeExpected == str and key.isnumeric() == True:
        return
      self.toReturn.append(typeExpected(key))
      # if isinstance(key, type(typeExpected)):

    except:
      pass

def draw_result(wrkscr, notes):
  finished = False
  while finished == False:
    for note in notes:
      noteName = note["note"] 
      noteTime = note["time"]
      wrkscr.addstr(10, 10, str(noteName))
      wrkscr.refresh()
      time.sleep(noteTime)
    finished = True
  
def main(stdscr): #stdscr: abreviacion comun en la libreria Curses para 'standard screen'
  curses.use_default_colors()
  curses.init_pair(1, 244, -1)
  octave = 4

  semitones_question = askQuestion(int, "What is your scale?", "3-2-1-1-3-2", [3,2,1,1,3,2])
  tonality_question  = askQuestion(str, "What is the tonality of the scale?", "La", "la")
  times_question     = askQuestion(float, "What are the times of each note?", "1.0-1-0-0.8-0.5-0.4", [1.0,1.0,1.0,0.5,0.4])
  
  semitones = semitones_question.returnedValue
  tonality = tonality_question.returnedValue.lower()
  times = times_question.returnedValue

  result_scr = curses.newwin(2, 60,6,0)

  initialPitch = int(midi_notes[tonality])+(12*octave-12)

  notes = notes_reproducer.calculate_notes(initialPitch, semitones, times)

  play.playSession(110, octave, notes, result_scr)
  
  print(
    "\n"
    f"semitones: {str(semitones)}\n"
    f"tonality:  {str(tonality)}\n"
    f"times:     {str(times)}\n"
    )
  
  result_scr.getkey()
  stdscr.refresh()

if __name__ == "__main__":
  wrapper(main)
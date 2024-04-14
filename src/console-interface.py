import play
import os
def note_converter():
  os.system("cls")
  print("Ingrese una escala:")
  print("Ejemplo: 3-2-1-1-3-2")

  escala = str(input())
  escala_final = []


  for index, letter in enumerate(escala):
    if index == 0 and not (letter.isdigit()):
      raise ValueError("Invalid scale")
    if index % 2 != 0 and letter != "-":
      raise ValueError("Invalid scale") 
    if index % 2 == 0 and not (letter.isdigit()):
      raise ValueError("Invalid scale") 
    
    if index % 2 == 0:
      escala_final.append(int(letter))
  if escala == "":
      escala_final = [3,2,1,1,3,2]

  print("\nIngrese una tonalidad (en minusculas):")
  print("Ejemplo: do")

  tonalidad = str(input())
  
  tonalidad_final = tonalidad
  if tonalidad == "":
    tonalidad_final = "la"
  

  print("\nIngrese los tiempos de cada nota (opcional, por defecto: 0.5 para todas las notas):")
  print("Ejemplo: 1-1-1-0.5-0.5")
  tiempos = str(input())

  tiempos_final = tiempos.split("-")



  if tiempos == "":
    tiempos_final = []
    for nota in escala_final:
      tiempos_final.append(0.5)
  
  for index, tiempo in enumerate(tiempos_final):
    tiempos_final[index] = float(tiempo)
  
  print("Escala ---->", escala_final)
  print("Tonalidad ->", tonalidad_final)
  print("Tiempos: -->", tiempos_final)


  play.playSession(90, escala_final, tiempos_final, 3, tonalidad_final)
  input("Presione cualquier tecla para reiniciar el programa ")
  return
while True:
  note_converter()
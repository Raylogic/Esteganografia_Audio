import wave
from tkinter import *
import tkinter as tk

class Proyecto(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.parent = master
        self.grid()
        self.createWidgets()
    
    def createWidgets(self):
        # Row 1 & 2
        self.display = Label(self, font=("Arial", 13), borderwidth=0, justify="center", text="Introduce el nombre de archivo a crear")
        self.display.grid(row=0, column=0, columnspan=10, sticky="nsew")

        fileName = Entry(self, font=("Arial", 18), borderwidth=0, justify="center")
        self.display = fileName
        self.display.grid(row=1, column=0, columnspan=10, sticky="nsew")
        
        # Column 1
        self.display = Label(self, font=("Arial", 13), borderwidth=0, justify="center", text="Introduce el nombre de archivo de audio (sin extensión)")
        self.display.grid(row=2, column=0, columnspan=1, sticky="nsew")

        userInput = Entry(self, font=("Arial", 18), borderwidth=0, justify="center")
        self.display = userInput
        self.display.grid(row=3, column=0, columnspan=1, sticky="nsew")

        self.display = Label(self, font=("Arial", 13), borderwidth=0, justify="center", text="Introduce el mensaje a ocultar")
        self.display.grid(row=4, column=0, columnspan=1, sticky="nsew")

        message = Text(self, font=("Arial", 13), borderwidth=0)
        self.display = message
        self.display.grid(row=5, column=0, columnspan=1, sticky="nsew")
        
        self.ceButton = Button(self, font=("Arial", 13), fg='black', text="Ocultar", command = lambda: self.ocultamiento(userInput, message, fileName))
        self.ceButton.grid(row=6, column=0, sticky="nsew")

        # Column 2
        self.display = Label(self, font=("Arial", 13), borderwidth=0, justify="center", text="Introduce el nombre de archivo con el mensaje oculto (sin extensión)", bg="black", fg="white")
        self.display.grid(row=2, column=2, columnspan=1, sticky="nsew")

        userInput2 = Entry(self, font=("Arial", 18), borderwidth=0, justify="center", bg="grey", fg="white")
        self.display = userInput2
        self.display.grid(row=3, column=2, columnspan=1, sticky="nsew")

        self.display = Label(self, font=("Arial", 13), borderwidth=0, justify="center", text="Mensaje recuperado", bg="black", fg="white")
        self.display.grid(row=4, column=2, columnspan=1, sticky="nsew")

        recoveredMessage = Text(self, font=("Arial", 13), borderwidth=0, bg="grey", fg="white")
        self.display = recoveredMessage
        self.display.grid(row=5, column=2, columnspan=1, sticky="nsew")

        self.inverseButton = Button(self, font=("Arial", 13), fg='black', text="Recuperar", command = lambda: self.recuperacion(recoveredMessage, userInput2))
        self.inverseButton.grid(row=6, column=2, sticky="nsew")
    
    def ocultamiento(self, userInput, message, fileName):
        # Obtener el nombre del archivo de audio
        titulo = userInput.get()
        # Abre el archivo de audio
        audio = wave.open(titulo + ".wav", 'rb')

        # Lee y guarda los bytes del audio en un bytearray
        frame = bytearray(list(audio.readframes(audio.getnframes())))

        # Escribe el mensaje
        mensaje = message.get("1.0",'end-1c')

        # Agrega información basura para llenar los bytes restantes
        mensaje = mensaje + int((len(frame) - (len(mensaje) * 8 * 8)) / 8) * '#'

        # Convierte el mensaje en una lista de bits
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in mensaje])))

        # Realiza la esteganografía mediante codificación por LSB
        # Reemplaza el último bit de cada byte con uno del mensaje
        for i, bit in enumerate(bits):
            frame[i] = (frame[i] & 254) | bit

        # Reconvierte el audio modificado a bytes
        new_frame = bytes(frame)

        # Asigna un nombre al archivo de audio modificado
        steg = fileName.get()

        # Guarda el audio modificado en un nuevo archivo
        with wave.open(steg + '.wav', 'wb') as new_audio:
            new_audio.setparams(audio.getparams())
            new_audio.writeframes(new_frame)

        # Cierra el audio original
        audio.close()
        
    def recuperacion(self, recoveredMessage, userInput2):
        # Obtener el nombre del archivo de audio
        titulo = userInput2.get()
        
        # Abre el archivo de audio
        audio = wave.open(titulo + ".wav", 'rb')

        # Lee y guarda los bytes del audio en un bytearray
        frame = bytearray(list(audio.readframes(audio.getnframes())))

        # Extrae el LSB de cada byte
        extracted = [frame[i] & 1 for i in range(len(frame))]

        # Convierte la lista de bits extraídos en un string
        mensaje = "".join(chr(int("".join(map(str,extracted[i:i+8])), 2)) for i in range(0, len(extracted), 8))

        # Elimina la información basura
        recover = mensaje.split("#")[0]

        # Cierra el audio modificado
        audio.close()

        # Mostrar mensaje en GUI
        recoveredMessage.delete(1.0, "end-1c")
        recoveredMessage.insert("end-1c", recover)

ui = Tk()
ui.title("Esteganografia de audio")
ui.config(bg="#000000", cursor="cross", height="100", width="100", relief="groove")
ui.resizable(False, False)
root = Proyecto(ui).grid()
ui.mainloop()
import socket, struct, pickle, threading
from tkinter import *

# IP y puerto para la comunicación multicast
MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

# Establezco el socket para multicast
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
ttl = struct.pack('b',1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
sock.bind(('',MCAST_PORT))
  
  
# Clase donde se define todo lo relacionado con la GUI
class GUI:
    # Constructor
    def __init__(self):
        
        # Ventana del chat que está actualmente oculta
        self.Window = Tk()
        self.Window.withdraw()
          
        # Ventana para introducir el nombre de usuario
        self.start = Toplevel()
        # Ponemos titulo y cambio ajustes de tamaño
        self.start.title("Bienvenido")
        self.start.resizable(width = False, 
                             height = False)
        self.start.configure(width = 600,
                             height = 400)
        # Creamos label para pantalla
        self.labelStart = Label(self.start, 
                       text = "Introduzca su nombre para empezar",
                       justify = CENTER, 
                       font = "Helvetica 14 bold")
          
        self.labelStart.place(relheight = 0.15,
                       relx = 0.2, 
                       rely = 0.07)
        # Label para el txtbox
        self.labelNombre = Label(self.start,
                               text = "Nombre: ",
                               font = "Helvetica 12")
          
        self.labelNombre.place(relheight = 0.2,
                             relx = 0.1, 
                             rely = 0.2)
          
        # Creamos el txtbox para introducir el nombre 
        self.txtBoxNombre = Entry(self.start, 
                             font = "Helvetica 14")
          
        self.txtBoxNombre.place(relwidth = 0.4, 
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.2)
          
        # El focus está en el txtbox
        self.txtBoxNombre.focus()
          
        # Creo botón para unirse al chat
        # defino acciones del boton
        self.btnUnirse = Button(self.start,
                         text = "Unirse", 
                         font = "Helvetica 14 bold", 
                         command = lambda: self.btnUnirseAhead(self.txtBoxNombre.get()))
          
        self.btnUnirse.place(relx = 0.4,rely = 0.55)
        self.Window.mainloop()
  
    def btnUnirseAhead(self, name):
        self.start.destroy()
        self.chat(name)
          
        # Defino y levanto thread para la recepción
        rcv = threading.Thread(target=self.recibir)
        rcv.start()
  
    # The main chat of the chat
    def chat(self,name):
        
        self.name = name
        # Muestro la ventana
        self.Window.deiconify()
        self.Window.title("Chat")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 470,
                              height = 550,
                              bg = "#777777")
        self.labelNombre = Label(self.Window,
                             bg = "#398fe6", 
                              fg = "#EAECEE",
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5)
          
        self.labelNombre.place(relwidth = 1)
        self.separador = Label(self.Window,
                          width = 450,
                          bg = "#ABB2B9")
          
        self.separador.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
        # TXTBOX donde salen los mensajes enviados y recibidos
        self.txtBoxMensajes = Text(self.Window,
                             width = 20, 
                             height = 2,
                             bg = "#777777",
                             fg = "#EAECEE",
                             font = "Helvetica 14", 
                             padx = 5,
                             pady = 5)
          
        self.txtBoxMensajes.place(relheight = 0.745,
                            relwidth = 1, 
                            rely = 0.08)
          
        self.labelBoton = Label(self.Window,
                                 bg = "#ABB2B9",
                                 height = 80)
          
        self.labelBoton.place(relwidth = 1,
                               rely = 0.825)

        # Creo el txtbox donde se escribe 
        self.txtBoxEntrada = Entry(self.labelBoton,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
          
        self.txtBoxEntrada.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
          
        self.txtBoxEntrada.focus()
          
        # Botón para enviar
        self.btnEnviar = Button(self.labelBoton,
                                text = "Enviar",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.enviarBoton(self.txtBoxEntrada.get()))
          
        self.btnEnviar.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.06, 
                             relwidth = 0.22)
          
        self.txtBoxMensajes.config(cursor = "arrow")
          
        # Creo scrollbar para ver mas mensajes
        scrollbar = Scrollbar(self.txtBoxMensajes)
          
        # Se coloca sobre el txtboxmensajes
        scrollbar.place(relheight = 1,
                        relx = 0.974)
        # Se configura para moverse en el eje y
        scrollbar.config(command = self.txtBoxMensajes.yview)
          
        self.txtBoxMensajes.config(state = DISABLED)
  
    # AQUI SE DEFINEN FUNCIONALIDADES
    def enviarBoton(self, msg):
        self.txtBoxMensajes.config(state = DISABLED)
        self.msg=msg
        self.txtBoxEntrada.delete(0, END)
        self.txtBoxMensajes.config(state=DISABLED)
        while True:
            message = (self.name, self.msg)
            sock.sendto(pickle.dumps(message), (MCAST_GRP,MCAST_PORT))
            break    
        #snd= threading.Thread(target = self.sendMessage)
        #snd.start()
  
    # funcion para recibir mensajes
    def recibir(self):
        while True:
            try:
                data = sock.recv(1024)
                unwrapped = pickle.loads(data)
                if self.name != unwrapped[0]:
                    message = "RX de "+unwrapped[0]+"> "+unwrapped[1]
                else:
                    message = "TX> "+unwrapped[1]
                # insert messages to text box
                self.txtBoxMensajes.config(state = NORMAL)
                self.txtBoxMensajes.insert(END,
                                        message+"\n")
                    
                self.txtBoxMensajes.config(state = DISABLED)
                self.txtBoxMensajes.see(END)
            except:
                # Se muestra mensaje de error por consola
                print("Ha ocurrido un error o ha finalizado la ejecución correctamente.")
                sock.close()
                break 
          
    # funcion para mandar mensajes
    def sendMessage(self):
        self.txtBoxMensajes.config(state=DISABLED)
        while True:
            message = (self.name, self.msg)
            sock.sendto(pickle.dumps(message), (MCAST_GRP,MCAST_PORT))
            break    
  
# Creo GUI para iniciar
g = GUI()
sock.close()
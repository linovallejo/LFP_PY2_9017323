from tkinter import *
import tkinter.messagebox
import pyttsx3
import threading
import time


def InterfazUsuario():
    from laligabot import Bot, GenerarTablaTokens

    saved_username = ["Lino"]
    # ans=["PyBot"]
    window_size = "1500x400"

    class ChatInterface(Frame):
        def __init__(self, master=None):
            Frame.__init__(self, master)
            self.master = master

            # sets default bg for top level windows
            self.tl_bg = "#EEEEEE"
            self.tl_bg2 = "#EEEEEE"
            self.tl_fg = "#000000"
            self.font = "Verdana 10"

            menu = Menu(self.master)
            self.master.config(menu=menu, bd=5)
        # Menu bar

        # File
            file = Menu(menu, tearoff=0)
            menu.add_cascade(label="File", menu=file)
        # file.add_command(label="Save Chat Log", command=self.save_chat)
            file.add_command(label="Clear Chat", command=self.clear_chat)
        #  file.add_separator()
            file.add_command(label="Exit", command=self.chatexit)

        # Options
            options = Menu(menu, tearoff=0)
            menu.add_cascade(label="Options", menu=options)

            # username

            # font
            font = Menu(options, tearoff=0)
            options.add_cascade(label="Font", menu=font)
            font.add_command(label="Default", command=self.font_change_default)

            # color theme
            color_theme = Menu(options, tearoff=0)
            options.add_cascade(label="Color Theme", menu=color_theme)
            color_theme.add_command(
                label="Default", command=self.color_theme_default)

            help_option = Menu(menu, tearoff=0)
            menu.add_cascade(label="Help", menu=help_option)
            # help_option.add_command(label="Features", command=self.features_msg)
            help_option.add_command(label="About PyBot", command=self.msg)
            help_option.add_command(label="Develpoers", command=self.about)

            self.text_frame = Frame(self.master, bd=6)
            self.text_frame.pack(expand=True, fill=BOTH)

            # scrollbar for text box
            self.text_box_scrollbar = Scrollbar(self.text_frame, bd=0)
            self.text_box_scrollbar.pack(fill=Y, side=RIGHT)

            # contains messages
            self.text_box = Text(self.text_frame, yscrollcommand=self.text_box_scrollbar.set, state=DISABLED,
                                 bd=1, padx=6, pady=6, spacing3=8, wrap=WORD, bg=None, font="Verdana 10", relief=GROOVE,
                                 width=10, height=1)
            self.text_box.pack(expand=True, fill=BOTH)
            self.text_box_scrollbar.config(command=self.text_box.yview)

            # frame containing user entry field
            self.entry_frame = Frame(self.master, bd=1)
            self.entry_frame.pack(side=LEFT, fill=BOTH, expand=True)

            # entry field
            self.entry_field = Entry(self.entry_frame, bd=1, justify=LEFT)
            self.entry_field.pack(fill=X, padx=6, pady=6, ipady=3)
            # self.users_message = self.entry_field.get()

            # frame containing send button and emoji button
            self.send_button_frame = Frame(self.master, bd=0)
            self.send_button_frame.pack(fill=BOTH)

            # send button
            self.send_button = Button(self.send_button_frame, text="Send", width=5, relief=GROOVE, bg='white',
                                      bd=1, command=lambda: self.send_message_insert(None), activebackground="#FFFFFF",
                                      activeforeground="#000000")
            self.send_button.pack(side=LEFT, ipady=8)
            self.master.bind("<Return>", self.send_message_insert)

            self.last_sent_label(date="Mensajes no enviados aún.")
            # t2 = threading.Thread(target=self.send_message_insert(, name='t1')
            # t2.start()

            self.reporteErrores_button = Button(self.send_button_frame, text="Reporte de errores", width=15, relief=GROOVE, bg='white',
                                                bd=1, command=lambda: self.abrir_reporte_errores())
            self.reporteErrores_button.pack(side=LEFT, ipady=16)

            self.limpiarLogErrores_button = Button(self.send_button_frame, text="Limpiar log de errores", width=15, relief=GROOVE, bg='white',
                                                   bd=1, command=lambda: self.limpiar_log__errores(), activebackground="#FFFFFF",
                                                   activeforeground="#000000")
            self.limpiarLogErrores_button.pack(side=LEFT, ipady=16)

            self.reporteTokens_button = Button(self.send_button_frame, text="Reporte de tokens", width=10, relief=GROOVE, bg='white',
                                               bd=1, command=lambda: self.abrir_reporte_tokens(), activebackground="#FFFFFF",
                                               activeforeground="#000000")
            self.reporteTokens_button.pack(side=LEFT, ipady=16)

            self.limpiarLogTokens_button = Button(self.send_button_frame, text="Limpiar log de tokens", width=15, relief=GROOVE, bg='white',
                                                  bd=1, command=lambda: self.limpiar_log__tokens(), activebackground="#FFFFFF",
                                                  activeforeground="#000000")
            self.limpiarLogTokens_button.pack(side=LEFT, ipady=16)

            self.manualUsuario_button = Button(self.send_button_frame, text="Manual de usuario", width=10, relief=GROOVE, bg='white',
                                               bd=1, command=lambda: self.abrir_manual_usuario(), activebackground="#FFFFFF",
                                               activeforeground="#000000")
            self.manualUsuario_button.pack(side=LEFT, ipady=16)

            self.manualTecnico_button = Button(self.send_button_frame, text="Manual Técnico", width=10, relief=GROOVE, bg='white',
                                               bd=1, command=lambda: self.abrir_manual_tecnico(), activebackground="#FFFFFF",
                                               activeforeground="#000000")
            self.manualTecnico_button.pack(side=LEFT, ipady=16)

        def clear_chat(self):
            self.text_box.config(state=NORMAL)
            self.last_sent_label(date="Mensajes no enviados aún.")
            self.text_box.delete(1.0, END)
            self.text_box.delete(1.0, END)
            self.text_box.config(state=DISABLED)

        def chatexit(self):
            exit()

        def font_change_default(self):
            self.text_box.config(font="Verdana 10")
            self.entry_field.config(font="Verdana 10")
            self.font = "Verdana 10"

        def color_theme_default(self):
            self.master.config(bg="#EEEEEE")
            self.text_frame.config(bg="#EEEEEE")
            self.entry_frame.config(bg="#EEEEEE")
            self.text_box.config(bg="#FFFFFF", fg="#000000")
            self.entry_field.config(
                bg="#FFFFFF", fg="#000000", insertbackground="#000000")
            self.send_button_frame.config(bg="#EEEEEE")
            self.send_button.config(
                bg="#FFFFFF", fg="#000000", activebackground="#FFFFFF", activeforeground="#000000")
            # self.emoji_button.config(bg="#FFFFFF", fg="#000000", activebackground="#FFFFFF", activeforeground="#000000")
            self.sent_label.config(bg="#EEEEEE", fg="#000000")

            self.tl_bg = "#FFFFFF"
            self.tl_bg2 = "#EEEEEE"
            self.tl_fg = "#000000"

        def msg(self):
            tkinter.messagebox.showinfo(
                "PyBOT v1.0", 'PyBOT is a chatbot for answering python queries\nIt is based on retrival-based NLP using pythons NLTK tool-kit module\nGUI is based on Tkinter\nIt can answer questions regarding python language for new learners')

        def about(self):
            tkinter.messagebox.showinfo(
                "PyBOT Developers", "1.Abhishek Ezhava\n2.Mayur Kadam\n3.Monis Khot\n4.Raj Vishwakarma")

        def playResponce(self, responce):
            x = pyttsx3.init()
            # print(responce)
            li = []
            if len(responce) > 100:
                if responce.find('--') == -1:
                    b = responce.split('--')
                    # print(b)

            x.setProperty('rate', 120)
            x.setProperty('volume', 100)
            x.say(responce)
            x.runAndWait()
            # print("Played Successfully......")

        def last_sent_label(self, date):

            try:
                self.sent_label.destroy()
            except AttributeError:
                pass

            self.sent_label = Label(
                self.entry_frame, font="Verdana 7", text=date, bg=self.tl_bg2, fg=self.tl_fg)
            self.sent_label.pack(side=LEFT, fill=X, padx=3)

        def abrir_reporte_errores(self):
            tkinter.messagebox.showinfo('LaLigaBot', 'Reporte errores')

        def limpiar_log__errores(self):
            tkinter.messagebox.showinfo('LaLigaBot', 'Limpiar log de errores')

        def abrir_reporte_tokens(self):
            tkinter.messagebox.showinfo('LaLigaBot', 'Reporte tokens')
            Bot('tokens')

        def limpiar_log__tokens(self):
            tkinter.messagebox.showinfo('LaLigaBot', 'Limpiar log de tokens')
            Bot('limpiar_tokens')

        def abrir_manual_usuario(self):
            # tkinter.messagebox.showinfo('LaLigaBot', 'Manual de Usuario')
            import os

            carpetaDocs = 'docs'
            fullPathDocs = f'{os.getcwd()}/{carpetaDocs}/'
            nombreArchivoManualTecnico = 'Proyecto2ManualUsuario.pdf'
            nombreArchivoManualTecnico = fullPathDocs + nombreArchivoManualTecnico

            os.system("open /Applications/Safari.app " +
                      nombreArchivoManualTecnico)

        def abrir_manual_tecnico(self):
            # tkinter.messagebox.showinfo('LaLigaBot', 'Manual Técnico')
            import os

            carpetaDocs = 'docs'
            fullPathDocs = f'{os.getcwd()}/{carpetaDocs}/'
            nombreArchivoManualTecnico = 'Proyecto2ManualTecnico.pdf'
            nombreArchivoManualTecnico = fullPathDocs + nombreArchivoManualTecnico

            os.system("open /Applications/Safari.app " +
                      nombreArchivoManualTecnico)

        def send_message_insert(self, message):
            user_input = self.entry_field.get()
            if (user_input.strip() != ''):
                pr1 = "Humano : " + user_input + "\n"
                self.text_box.configure(state=NORMAL)
                self.text_box.insert(END, pr1)
                self.text_box.configure(state=DISABLED)
                self.text_box.see(END)
                # t1 = threading.Thread(target=self.playResponce, args=(user_input,))
                # t1.start()
                # time.sleep(1)
                # ob = "Hello Lino"
                tkinter.messagebox.showinfo(
                    "Mensaje", str(user_input))

                ob = Bot(user_input)
                tkinter.messagebox.showinfo(
                    "Respuesta", str(ob))
                pr = "LaLigaBot : " + str(ob) + "\n"
                self.text_box.configure(state=NORMAL)
                self.text_box.insert(END, pr)
                self.text_box.configure(state=DISABLED)
                self.text_box.see(END)
                self.last_sent_label(
                    str(time.strftime("Ultimo mensaje enviado: " + '%B %d, %Y' + ' at ' + '%I:%M %p')))
                self.entry_field.delete(0, END)
                time.sleep(0)
                # t2 = threading.Thread(target=self.playResponce, args=(ob,))
                # t2.start()
                # return ob
            else:
                tkinter.messagebox.showerror(
                    "Error", "El comando es una cadena vacía!")

    root = Tk()

    a = ChatInterface(root)
    root.geometry(window_size)
    root.title("LaLiga Bot")
    root.mainloop()


InterfazUsuario()

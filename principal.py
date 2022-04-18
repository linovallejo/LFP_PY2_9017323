from __future__ import print_function
import tokens
from sqlite3 import connect
from tkinter import *
from tkinter import messagebox

from clases import TablaDeErrores, ErrorLexico
from clases import TablaDeTokens, Token

#import utils

# Globales
tt = []
te = []
tt = TablaDeTokens()
te = TablaDeErrores()
lMenu = None
menu = None
variable = None,

comandoActual = ''
lexemaActual = ''

comandoResultado = False
comandoVersus = False
comandoTemporada = False
primerEquipo = None
segundoEquipo = None
anio1 = 0
anio2 = 0
temporada = ''


def inicioValido(c):
    if (c.isalpha()):
        return True
    return False


def estadoCero():
    global comandoActual
    comandoActual = 'RESULTADO "Real Madrid" VS "Villarreal" TEMPORADA <2018-2019>'


def estadoUno(lexema):
    global comandoResultado, comandoVersus, comandoTemporada
    if (lexema == tokens.tr_RESULTADO):
        comandoResultado = True
    elif (lexema == tokens.tr_VERSUS):
        comandoVersus = True
    elif (lexema == tokens.tr_TEMPORADA):
        comandoTemporada = True


def estadoDos(lexema):
    return


def estadoTres(lexema):
    global primerEquipo, segundoEquipo
    lexema = lexema.replace(tokens.t_COMILLA, "")
    if (primerEquipo is None):
        primerEquipo = lexema
    elif (segundoEquipo is None):
        segundoEquipo = lexema
    return


def estadoCuatro(lexema):
    global anio1, anio2, temporada
    lexema = lexema.replace(tokens.t_MENORQUE, "")
    lexema = lexema.replace(tokens.t_MAYORQUE, "")
    anios = lexema.split("-")
    anio1 = int(anios[0])
    anio2 = int(anios[1])
    temporada = str(anio1) + '-' + str(anio2)


def estado1Valido(lexema):
    valido = False
    for i in range(1, len(lexema), 1):
        if (lexema[i].isupper()):
            valido = True
        else:
            valido = False
    return valido


def estado2Valido(caracter):
    valido = False
    if caracter.isdigit():
        valido = True
    # for i in range(1, len(lexema), 1):
    #     if (lexema[i].isdigit()):
    #         valido = True
    #     else:
    #         valido = False
    return valido


def estado3Valido(lexema):
    valido = False
    if (lexema[0] == tokens.t_COMILLA and lexema[len(lexema)-1] == tokens.t_COMILLA):
        for i in range(1, len(lexema), 1):
            if (lexema[i].isalpha() or lexema[i].strip() == '' or lexema[i] == tokens.t_COMILLA):
                valido = True
            else:
                valido = False
    return valido


def estado4Valido(lexema):
    valido = False
    if (lexema[0] == tokens.t_MENORQUE and lexema[len(lexema)-1] == tokens.t_MAYORQUE):
        for i in range(1, len(lexema), 1):
            if (lexema[i].isdigit() or lexema[i] == '-' or lexema[i].strip() == '' or lexema[i] == tokens.t_MENORQUE or lexema[i] == tokens.t_MAYORQUE):
                valido = True
            else:
                valido = False
    return valido


def resultados():
    global temporada, primerEquipo, segundoEquipo
    sql = "SELECT fecha, temporada, jornada, equipo1, equipo2, goles1, goles2 FROM laliga "
    sql = sql + f"WHERE equipo1 = '{primerEquipo}' "
    sql = sql + f"AND equipo2 = '{segundoEquipo}' "
    sql = sql + f"AND temporada = '{temporada}' "

    filas = ConsultaBaseDatos(sql)

    # print(filas)

    golesPrimerEquipo = filas[0][5]
    golesSegundoEquipo = filas[0][6]

    print(
        f'El resultado de este partido fue: {primerEquipo} {golesPrimerEquipo} - {segundoEquipo} {golesSegundoEquipo}')


def AnalizarProyecto2():
    global comandoActual, lexemaActual
    estadoTresInicio = False
    estadoTresFinal = False
    estadoCuatroInicio = False
    estadoCuatroFinal = False

    for i in range(0, len(comandoActual), 1):
        if (comandoActual[i] == tokens.t_COMILLA) and estadoTresInicio == False:
            lexemaActual = lexemaActual + comandoActual[i]
            estadoTresInicio = True
        else:
            if estadoTresInicio:
                lexemaActual = lexemaActual + comandoActual[i]
                if (comandoActual[i] == tokens.t_COMILLA):
                    estadoTresFinal = True
                if estadoTresFinal:
                    if estado3Valido(lexemaActual):
                        estadoTres(lexemaActual)
                        estadoTresInicio = False
                        estadoTresFinal = False
                        lexemaActual = ''

        if (comandoActual[i] == tokens.t_MENORQUE) and estadoCuatroInicio == False:
            lexemaActual = lexemaActual + comandoActual[i]
            estadoCuatroInicio = True
        else:
            if estadoCuatroInicio:
                lexemaActual = lexemaActual + comandoActual[i]
                if (comandoActual[i] == tokens.t_MAYORQUE):
                    estadoCuatroFinal = True
                if estadoCuatroFinal:
                    if estado4Valido(lexemaActual):
                        estadoCuatro(lexemaActual)
                        estadoCuatroInicio = False
                        estadoCuatroFinal = False

        if not estadoTresInicio and not estadoCuatroInicio:
            if (comandoActual[i].strip() != ''):
                lexemaActual = lexemaActual + comandoActual[i]
            else:
                if (lexemaActual.strip() != ''):
                    caracterInicial = lexemaActual[0]
                    if caracterInicial.isupper():
                        if estado1Valido(lexemaActual):
                            estadoUno(lexemaActual)
                    elif caracterInicial.isdigit():
                        if estado2Valido(lexemaActual):
                            estadoDos(lexemaActual)
                    lexemaActual = ''

    if (comandoResultado and comandoVersus and comandoTemporada):
        resultados()


def ConsultaBaseDatos(sql):
    conn = connect('./laliga.db')
    curs = conn.cursor()

    curs.execute(sql)
    rows = curs.fetchall()
    conn.close()
    return rows


def TestBaseDatos():
    conn = connect('./laliga.db')
    curs = conn.cursor()

    curs.execute(
        "SELECT equipo1, equipo2, goles1, goles2 FROM laliga WHERE equipo1 = 'Real Madrid';")
    for equipo1, equipo2, goles1, goles2 in curs.fetchall():
        print(equipo1, goles1, equipo2, goles2)

    conn.close()


def estado2Valido(lexema):
    valido = False
    for i in range(0, len(lexema), 1):
        if (lexema[i].isalnum()):
            valido = True
        elif lexema[i] == '\"':
            valido = False
        else:
            valido = False
    return valido


def estados3y4Validos(lexema):
    import tokens
    tipoToken = ''
    if lexema == tokens.t_INICIOFORMULARIO:
        tipoToken = 'SimboloInicio'
    elif lexema in tokens.operadores or lexema in tokens.delimitadores:
        tipoToken = 'Simbolo'
    return tipoToken


def dfaValidoParaId(lexema):
    if inicioValido(lexema[0]):
        if estado1Valido(lexema):
            return True
    return False


def dfaValidoParaCadena(lexema):
    if estado2Valido(lexema):
        return True
    return False


def Analizar1():
    global archivoDatosCargado, tt, codigoEntrada
    codigoEntrada = txtCodigo.get("1.0", "end-1c")
    if (archivoDatosCargado or codigoEntrada.strip() != ''):
        Analizar(tt)
    else:
        if (codigoEntrada == '' or txtCodigo.strip() == ''):
            messagebox.showerror(
                'Error', 'Código de Entrada no puede estar en blanco')
        elif (archivoDatosCargado == False):
            messagebox.showerror(
                'Error', 'Aún no se ha cargado un archivo .form')


def Analizar(tt):
    global archivoAnalizado, te

    caracter = ''
    cadena = ''
    lineaActual = 1
    valorActual = ''
    comillaAbrir = False
    listaAbrir = False
    listaValores = ''
    valor = ''

    import tokens

    lexema = ''
    lexemaIdentificador = ''

    elementos = []
    numeroElemento = 1
    elementoActual = Elemento(numeroElemento, '')

    te = TablaDeErrores()

    indiceColumna = 0

    for i in range(0, len(codigoEntrada), 1):
        try:
            caracter = codigoEntrada[i]

            indiceColumna = indiceColumna + 1

            if (lexema == tokens.t_MAYORQUECOMA):
                numeroElemento = numeroElemento + 1
                elementos.append(elementoActual)
                elementoActual = Elemento(numeroElemento, '')

            if (caracter.isspace() and not comillaAbrir):
                lexema = cadena
                if len(lexema) > 0 and lexema[0].isalpha():
                    if lexema in tokens.reservadas:
                        if dfaValidoParaId(lexema):
                            token = Token('Id', lexema, lineaActual,
                                          indiceColumna-len(lexema))
                            tt.agregar(token)
                            lexemaIdentificador = lexema
                else:
                    tipoToken = ''
                    tipoToken = estados3y4Validos(lexema)
                    if tipoToken != '':
                        token = Token(tipoToken, lexema,
                                      lineaActual, indiceColumna-len(lexema))
                        tt.agregar(token)
                cadena = ''
            elif caracter in tokens.delimitadoresValores:
                if not comillaAbrir:
                    comillaAbrir = True
                else:
                    comillaCerrar = True
                valorActual = cadena.replace("""""", "")
                if (not valorActual == ''):
                    # if (dfaValidoParaCadena(valor)): ====> NO ESTA FUNCIONANDO EN ESTE CASO :(
                    token = Token('Cadena', valorActual, lineaActual,
                                  indiceColumna-len(valorActual))
                    tt.agregar(token)
                    comillaAbrir = False
                    comillaCerrar = False
                    cadena = ''
                    crearElemento(elementoActual, lexemaIdentificador,
                                  valorActual, lineaActual, indiceColumna-len(valorActual))
                    valorActual = ''
            else:
                cadena += codigoEntrada[i]

            if cadena in tokens.reservadas:
                lexema = cadena
                if dfaValidoParaId(lexema):
                    columna = indiceColumna - len(lexema) + 1
                    token = Token('Id', lexema, lineaActual,  columna)
                    tt.agregar(token)
                    lexemaIdentificador = lexema
                    cadena = ''
                    crearElemento(elementoActual, lexemaIdentificador,
                                  valorActual, lineaActual, columna)

            if cadena in tokens.delimitadoresListaValores:
                if not listaAbrir:
                    listaAbrir = True

            if cadena[-2:] in tokens.delimitadoresListaValores and len(cadena) > 2 and listaAbrir:
                listaValores = cadena.replace("[", "").replace("]", "")
                valores = []
                valoresValidosParaCadena = True
                for valor in listaValores.split(","):
                    valor = valor.replace("'", "")
                    if (dfaValidoParaCadena(valor)):
                        columna = indiceColumna - \
                            len(listaValores)+listaValores.index(valor)
                        token = Token('Cadena', valor, lineaActual, columna)
                        tt.agregar(token)
                        valores.append(valor)
                    else:
                        valoresValidosParaCadena = False
                        break
                if (valoresValidosParaCadena):
                    listaAbrir = False
                    cadena = ''
                    crearElemento(elementoActual, lexemaIdentificador,
                                  valores, lineaActual, indiceColumna-len(valor))

            if ord(caracter) == 10:
                lineaActual = lineaActual+1
                indiceColumna = 0

        except BaseException as err:
            messagebox.showerror(f"Error inesperado {err=}, {type(err)=}")
            raise

    if (elementos is not None and len(elementos) > 0):
        codigoHTML = ''
        codigoHTML = generarHTML(elementos)
        GenerarFormularioHtml(codigoHTML)

        archivoAnalizado = True
    else:
        messagebox.showerror(
            'Error', 'El formulario no pudo ser generado. Contacte a soporte técnico :-).')
        return


def GenerarReporteErrores(te):
    import uuid
    import os

    inicioFilaColumna = '<tr><td>'
    inicioFila = '<tr>'
    inicioColumna = '<td>'
    finalColumna = '</td>'
    finalFila = '</tr>'
    finalFilaColumna = '</tr></td>'

    codigoHTML = ''
    codigoHTML += '<html><head>'
    codigoHTML += '<style>'
    codigoHTML += 'table, th, td {'
    codigoHTML += 'border: 1px solid black;'
    codigoHTML += 'border-collapse: collapse; }'
    codigoHTML += 'tr:nth-child(even) {background-color: #f2f2f2;}'
    codigoHTML += '</style>'
    codigoHTML += '</head>'
    codigoHTML += '<body>'
    codigoHTML += '<table border=1 width=100%>'
    codigoHTML += inicioFila
    codigoHTML += '<th>No.</th>'
    codigoHTML += '<th>Token</th>'
    codigoHTML += '<th>Valor</th>'
    codigoHTML += '<th>Fila</th>'
    codigoHTML += '<th>Columna</th>'
    codigoHTML += '<th>Descripcion</th>'
    codigoHTML += finalFila

    i = 1
    for er in te.errores:
        codigoHTML += inicioFilaColumna
        codigoHTML += str(i)
        codigoHTML += finalColumna
        codigoHTML += inicioColumna
        codigoHTML += er.token
        codigoHTML += finalColumna
        codigoHTML += inicioColumna
        codigoHTML += er.valor
        codigoHTML += finalColumna
        codigoHTML += inicioColumna
        codigoHTML += str(er.fila)
        codigoHTML += finalColumna
        codigoHTML += inicioColumna
        codigoHTML += str(er.columna)
        codigoHTML += finalColumna
        codigoHTML += inicioColumna
        codigoHTML += str(er.descripcion)
        codigoHTML += finalFilaColumna
        i = i + 1

    codigoHTML += '</table>'
    codigoHTML += '</body></html>'

    carpetaReportesErrores = 'reporteserrores'
    fullPathReportesErrores = f'{os.getcwd()}/{carpetaReportesErrores}/'
    nombreArchivoReporteErroresActual = str(uuid.uuid4())
    nombreArchivoReporteErroresActual = fullPathReportesErrores + \
        nombreArchivoReporteErroresActual + ".html"
    if (os.path.exists(nombreArchivoReporteErroresActual)):
        os.remove(nombreArchivoReporteErroresActual)

    with open(nombreArchivoReporteErroresActual, 'w') as rep:
        try:
            rep.write(codigoHTML)
        except:
            print(
                mensaje='No se pudo crear el Reporte de Errores. Contacte a soporte técnico :-).')

    os.system("open /Applications/Safari.app " +
              nombreArchivoReporteErroresActual)


def GenerarFormularioHtml(codigoHTML):
    import uuid
    import os

    carpetaHtml = 'html'
    fullPathHtml = f'{os.getcwd()}/{carpetaHtml}/'
    nombreArchivoHtmlActual = str(uuid.uuid4())
    archivoHtmlActual = fullPathHtml + nombreArchivoHtmlActual + ".html"
    if (os.path.exists(archivoHtmlActual)):
        os.remove(archivoHtmlActual)

    with open(archivoHtmlActual, 'w') as rep:
        try:
            rep.write(codigoHTML)
        except:
            print(
                mensaje='No se pudo crear el formulario. Contacte a soporte técnico :-).')

    os.system("open /Applications/Safari.app " + archivoHtmlActual)


def GenerarTablaTokens(tt):
    import uuid
    import os

    inicioFilaColumna = '<tr><td>'
    inicioFila = '<tr>'
    inicioColumna = '<td>'
    finalColumna = '</td>'
    finalFila = '</tr>'
    finalFilaColumna = '</tr></td>'

    codigoHTML = ''
    codigoHTML += '<html><head>'
    codigoHTML += '<style>'
    codigoHTML += 'table, th, td {'
    codigoHTML += 'border: 1px solid black;'
    codigoHTML += 'border-collapse: collapse; }'
    codigoHTML += 'tr:nth-child(even) {background-color: #f2f2f2;}'
    codigoHTML += '</style>'
    codigoHTML += '</head>'
    codigoHTML += '<body>'
    codigoHTML += '<table border=1 width=100%>'
    codigoHTML += inicioFila
    codigoHTML += '<th>No.</th>'
    codigoHTML += '<th>Tipo</th>'
    codigoHTML += '<th>Lexema</th>'
    codigoHTML += '<th>Fila</th>'
    codigoHTML += '<th>Columna</th>'
    codigoHTML += finalFila

    i = 1
    for to in tt:
        codigoHTML += inicioFilaColumna
        codigoHTML += str(i)
        codigoHTML += finalColumna
        codigoHTML += inicioColumna
        codigoHTML += to.id
        codigoHTML += finalColumna
        codigoHTML += inicioColumna
        codigoHTML += to.lexema
        codigoHTML += finalColumna
        codigoHTML += inicioColumna
        codigoHTML += str(to.fila)
        codigoHTML += finalColumna
        codigoHTML += inicioColumna
        codigoHTML += str(to.columna)
        codigoHTML += finalFilaColumna
        i = i + 1

    codigoHTML += '</table>'
    codigoHTML += '</body></html>'

    carpetaTts = 'tts'
    fullPathTts = f'{os.getcwd()}/{carpetaTts}/'
    nombreArchivoTtsActual = str(uuid.uuid4())
    nombreArchivoTtsActual = fullPathTts + nombreArchivoTtsActual + ".html"
    if (os.path.exists(nombreArchivoTtsActual)):
        os.remove(nombreArchivoTtsActual)

    with open(nombreArchivoTtsActual, 'w') as rep:
        try:
            rep.write(codigoHTML)
        except:
            print(
                mensaje='No se pudo crear la Tabla de Tokens. Contacte a soporte técnico :-).')

    os.system("open /Applications/Safari.app " + nombreArchivoTtsActual)


estadoCero()

AnalizarProyecto2()

# TestBaseDatos()


# Analizar(tt)

# UI

def opcionMenuSeleccionada(opcion):
    global archivoAnalizado, tt, te
    opcion = variable.get()
    if (opcion == "---Seleccione-------"):
        messagebox.showerror(
            'Error', 'Debe seleccionar alguna de las otras opciones')
    elif (opcion == "Reporte de tokens"):
        if (archivoAnalizado):
            GenerarTablaTokens(tt.tokens)
        else:
            messagebox.showerror(
                'Error', 'Aún no se ha analizado un archivo .form')
    elif (opcion == 'Reporte de errores'):
        if (archivoAnalizado):
            GenerarReporteErrores(te)
        else:
            messagebox.showerror(
                'Error', 'Aún no se ha analizado un archivo .form')
    elif (opcion == 'Manual de Usuario'):
        AbrirManualUsuario()
    elif (opcion == 'Manual Técnico'):
        AbrirManualTecnico()


def CrearInterfazUsuario():
    global txtCodigo, archivoDatosCargado, lMenu, menu, variable

    root = Tk()
    root.geometry("800x700")
    root.title(" Generador de Formularios ")

    lCodigo = Label(text="Código: ")
    txtCodigo = Text(root, height=40,
                     width=70,
                     bg="light yellow")

    botonCargarArchivo = Button(root, height=2,
                                width=30,
                                text="Cargar Archivo .form",
                                command=lambda: CargarArchivo())

    botonAnalizar = Button(root, height=4,
                           width=20,
                           text="Analizar",
                           command=lambda: Analizar1())

    MENUOPTIONS = [
        "---Seleccione-------",
        "Reporte de tokens",
        "Reporte de errores",
        "Manual de Usuario",
        "Manual Técnico"
    ]

    variable = StringVar(root)
    variable.set(MENUOPTIONS[0])  # default value

    menu = OptionMenu(root, variable, *MENUOPTIONS,
                      command=opcionMenuSeleccionada)

    lMenu = Label(text="Reportes")
    lMenu.grid(column=0, row=0)
    lMenu.grid

    menu.grid(column=1, row=0)
    menu.config(bg='light blue')

    lCodigo.grid(column=0, row=1, columnspan=2)
    txtCodigo.grid(column=0, row=2, columnspan=2)
    txtCodigo.focus()

    botonCargarArchivo.grid(column=0, row=3, columnspan=2)

    botonAnalizar.grid(column=0, row=4, columnspan=2)

    root.columnconfigure(index=0, weight=1)
    root.columnconfigure(index=1, weight=3)

    mainloop()

# CrearInterfazUsuario()

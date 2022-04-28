from __future__ import print_function
from lib2to3.pgen2 import token
import tokens
from sqlite3 import connect
from tkinter import *
from tkinter import messagebox

from clases import TablaDeErrores, ErrorLexico
from clases import TablaDeTokens, Token

# import utils

# Globales
tt = []
te = []
tt = TablaDeTokens()
te = TablaDeErrores()
lMenu = None
menu = None
variable = None
inicioSesion = False
finSesion = False
numeroComando = 0

comandoActual = ''
lexemaActual = ''

nombrePorDefectoArchivo = 'reporte'

comandoResultado = False
comandoVersus = False
comandoTemporada = False
comandoJornada = False
valorJornada = 0
comandoGoles = False
comandoLocal = False
comandoVisitante = False
comandoTotal = False
comandoTabla = False
comandoPartidos = False
comandoTop = False
comandoSuperior = False
comandoInferior = False
comandoAdios = False
primerEquipo = False
segundoEquipo = False
anio1 = False
anio2 = False
temporada = False
banderaArchivo = False
banderaN = False
banderaJi = False
banderaJf = False
valorArchivo = ''
valorDefectoN = 5
valorBanderaN = 0
valorBanderaJi = 0
valorBanderaJf = 0

primerEquipo = None
segundoEquipo = None
anio1 = 0
anio2 = 0
temporada = ''
# banderaArchivo = ''
# banderaN = 0
# banderaJi = 0
# banderaJf = 0

inicioFilaColumna = '<tr><td>'
inicioFila = '<tr>'
inicioColumna = '<td>'
finalColumna = '</td>'
finalFila = '</tr>'
finalFilaColumna = '</tr></td>'


def estadoCero():
    global comandoActual
    comandoActual = 'RESULTADO "Real Madrid" VS "Villarreal" TEMPORADA <2018-2019>'  # PASSED
    comandoActual = 'JORNADA 1 TEMPORADA <2018-2019>'  # PASSED
    comandoActual = 'JORNADA 2 TEMPORADA <2017-2018> -f reporteJornada2'  # PASSED
    comandoActual = 'GOLES LOCAL "Real Madrid" TEMPORADA <2017-2018>'  # PASSED
    comandoActual = 'GOLES VISITANTE "Real Madrid" TEMPORADA <2017-2018>'  # PASSED
    comandoActual = 'GOLES TOTAL "Real Madrid" TEMPORADA <2017-2018>'  # PASSED
    comandoActual = 'GOLES VISITANTE "Valencia" TEMPORADA <2018-2019>'  # PASSED
    comandoActual = 'GOLES TOTAL "Valencia" TEMPORADA <2018-2019>'  # PASSED
    comandoActual = 'TABLA TEMPORADA <2017-2018> -f reporteTemporada'  # PASSED
    # comandoActual = 'PARTIDOS "Real Madrid" TEMPORADA <2017-2018> -f RealMadrid20172018'  # PASSED
    # comandoActual = 'PARTIDOS "Real Madrid" TEMPORADA <2017-2018> -f RealMadrid20172018 -ji 37 -jf 38'  # PASSED
    # comandoActual = 'TOP SUPERIOR TEMPORADA <2017-2018> -n 5'  # PASSED
    # comandoActual = 'ADIOS'  # not working :thinker


def estadoUno(lexema):
    global comandoResultado, comandoVersus, comandoTemporada
    if (lexema == tokens.tr_RESULTADO):
        comandoResultado = True
    elif (lexema == tokens.tr_VERSUS):
        comandoVersus = True
    elif (lexema == tokens.tr_TEMPORADA):
        comandoTemporada = True


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
    for i in range(0, len(lexema), 1):
        if (lexema[i].isupper()):
            valido = True
        else:
            valido = False
    return valido


def estado7Valido(lexema):
    valido = False
    for i in range(0, len(lexema), 1):
        if (lexema[i].isdigit()):
            valido = True
        else:
            valido = False
    return valido


def estado3Valido(lexema):
    valido = False
    if (lexema[0] == tokens.t_COMILLA and lexema[len(lexema)-1] == tokens.t_COMILLA):
        for i in range(0, len(lexema), 1):
            if (lexema[i].isalpha() or lexema[i].strip() == '' or lexema[i] == tokens.t_COMILLA):
                valido = True
            else:
                valido = False
    return valido


def estado4Valido(lexema):
    valido = False
    if (lexema[0] == tokens.t_MENORQUE and lexema[len(lexema)-1] == tokens.t_MAYORQUE):
        for i in range(0, len(lexema), 1):
            if (lexema[i].isdigit() or lexema[i] == '-' or lexema[i].strip() == '' or lexema[i] == tokens.t_MENORQUE or lexema[i] == tokens.t_MAYORQUE):
                valido = True
            else:
                valido = False
    return valido


def estado5Valido(lexema):
    valido = False
    for i in range(0, len(lexema), 1):
        if (lexema[i] == tokens.t_GUION or lexema[i] in tokens.t_BANDERAS):
            valido = True
        else:
            valido = False
    return valido


def estado6ValidoTokenArchivo(lexema):
    valido = False
    for i in range(0, len(lexema), 1):
        if (lexema[i].isalnum() or lexema[i] == tokens.t_GUIONBAJO):
            valido = True
        else:
            valido = False
    return valido


def estado6ValidoTokenEntero(lexema):
    valido = False
    for i in range(0, len(lexema), 1):
        if (lexema[i].isdigit()):
            valido = True
        else:
            break
    return valido


def ProcesarJornada(filas):
    import os
    global inicioFila, finalFila
    global inicioFilaColumna, inicioColumna, finalColumna, finalFilaColumna
    global banderaArchivo, banderaN, banderaJi, banderaJf
    global valorArchivo, valorBanderaN, valorBanderaJi, valorBanderaJf

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
    codigoHTML += f'<h1>Partidos de la temporada {temporada} - Jornada {valorJornada}</h1>'
    codigoHTML += '<table border=1 width=100%>'
    codigoHTML += inicioFila
    codigoHTML += '<th></th>'
    codigoHTML += '<th></th>'
    codigoHTML += '<th></th>'
    codigoHTML += '<th></th>'
    codigoHTML += '<th></th>'
    codigoHTML += finalFila

    i = 1
    for fila in filas:
        codigoHTML += inicioFilaColumna
        codigoHTML += str(i)
        codigoHTML += finalColumna
        codigoHTML += inicioColumna
        codigoHTML += fila[3]
        codigoHTML += finalColumna
        codigoHTML += inicioColumna
        codigoHTML += str(fila[5])
        codigoHTML += finalColumna
        codigoHTML += inicioColumna
        codigoHTML += fila[4]
        codigoHTML += finalColumna
        codigoHTML += inicioColumna
        codigoHTML += str(fila[6])
        codigoHTML += finalFilaColumna
        i = i + 1

    codigoHTML += '</table>'
    codigoHTML += '</body></html>'

    carpetaReportes = 'reportes'
    fullPathReportes = f'{os.getcwd()}/{carpetaReportes}/'
    if (banderaArchivo and valorArchivo.strip() != ''):
        nombreArchivoReporte = fullPathReportes + valorArchivo + ".html"
    else:
        nombreArchivoReporte = fullPathReportes + nombrePorDefectoArchivo + ".html"
    if (os.path.exists(nombreArchivoReporte)):
        os.remove(nombreArchivoReporte)

    with open(nombreArchivoReporte, 'w') as rep:
        try:
            rep.write(codigoHTML)
        except:
            print(
                mensaje='No se pudo crear el Reporte. Contacte a soporte técnico :-).')

    os.system("open /Applications/Safari.app " + nombreArchivoReporte)


class Equipo(object):
    def __init__(self, nombre='', puntos=0):
        self.nombre = nombre
        self.puntos = puntos


def crearEquipo(nombre, puntos):
    return Equipo(nombre, puntos)


def ProcesarTabla(filas1, filas2):
    import os
    global inicioFila, finalFila
    global inicioFilaColumna, inicioColumna, finalColumna, finalFilaColumna
    global banderaArchivo, banderaN, banderaJi, banderaJf
    global valorArchivo, valorBanderaN, valorBanderaJi, valorBanderaJf

    equipos = []
    equipoQuePuntea1 = ''
    equipoQuePuntea2 = ''
    puntos = 0
    for equipo in filas1:
        equipos.append(crearEquipo(equipo, 0))

    for partido in filas2:
        equipoQuePuntea1 = ''
        equipoQuePuntea2 = ''
        puntos = 0
        if int(partido[5]) > int(partido[6]):  # Gana Local
            equipoQuePuntea1 = partido[3]
            puntos = 3
        elif int(partido[5]) < int(partido[6]):  # Gana Visitante
            equipoQuePuntea1 = partido[4]
            puntos = 3
        elif int(partido[5]) == int(partido[6]):  # Empate
            equipoQuePuntea1 = partido[3]
            equipoQuePuntea2 = partido[4]
            puntos = 1

        if (equipoQuePuntea2.strip() == ''):
            for index, item in enumerate(equipos):
                if item.nombre == equipoQuePuntea1:
                    item.puntos += puntos
        else:
            for index, item in enumerate(equipos):
                if item.nombre == equipoQuePuntea1:
                    item.puntos += puntos
            for index, item in enumerate(equipos):
                if item.nombre == equipoQuePuntea2:
                    item.puntos += puntos

    codigoHTML = ''
    for eq in equipos:
        print(f'{eq.nombre} - {eq.puntos}')

    # codigoHTML += '<html><head>'
    # codigoHTML += '<style>'
    # codigoHTML += 'table, th, td {'
    # codigoHTML += 'border: 1px solid black;'
    # codigoHTML += 'border-collapse: collapse; }'
    # codigoHTML += 'tr:nth-child(even) {background-color: #f2f2f2;}'
    # codigoHTML += '</style>'
    # codigoHTML += '</head>'
    # codigoHTML += '<body>'
    # codigoHTML += f'<h1>Partidos de la temporada {temporada} - Jornada {valorJornada}</h1>'
    # codigoHTML += '<table border=1 width=100%>'
    # codigoHTML += inicioFila
    # codigoHTML += '<th></th>'
    # codigoHTML += '<th></th>'
    # codigoHTML += '<th></th>'
    # codigoHTML += '<th></th>'
    # codigoHTML += '<th></th>'
    # codigoHTML += finalFila

    # i = 1
    # for fila in filas:
    #     codigoHTML += inicioFilaColumna
    #     codigoHTML += str(i)
    #     codigoHTML += finalColumna
    #     codigoHTML += inicioColumna
    #     codigoHTML += fila[3]
    #     codigoHTML += finalColumna
    #     codigoHTML += inicioColumna
    #     codigoHTML += str(fila[5])
    #     codigoHTML += finalColumna
    #     codigoHTML += inicioColumna
    #     codigoHTML += fila[4]
    #     codigoHTML += finalColumna
    #     codigoHTML += inicioColumna
    #     codigoHTML += str(fila[6])
    #     codigoHTML += finalFilaColumna
    #     i = i + 1

    # codigoHTML += '</table>'
    # codigoHTML += '</body></html>'

    # carpetaReportes = 'reportes'
    # fullPathReportes = f'{os.getcwd()}/{carpetaReportes}/'
    # if (banderaArchivo and valorArchivo.strip() != ''):
    #     nombreArchivoReporte = fullPathReportes + valorArchivo + ".html"
    # else:
    #     nombreArchivoReporte = fullPathReportes + nombrePorDefectoArchivo + ".html"
    # if (os.path.exists(nombreArchivoReporte)):
    #     os.remove(nombreArchivoReporte)

    # with open(nombreArchivoReporte, 'w') as rep:
    #     try:
    #         rep.write(codigoHTML)
    #     except:
    #         print(
    #             mensaje='No se pudo crear el Reporte. Contacte a soporte técnico :-).')

    # os.system("open /Applications/Safari.app " + nombreArchivoReporte)


def Resultados():
    global comandoResultado, comandoVersus, comandoTemporada
    global comandoJornada, valorJornada
    global comandoGoles, comandoLocal, comandoVisitante, comandoTotal
    global comandoTabla
    global comandoPartidos
    global comandoTop, comandoSuperior, comandoInferior
    global comandoAdios
    global primerEquipo, segundoEquipo
    global anio1, anio2, temporada
    global banderaArchivo, banderaN, banderaJi, banderaJf
    global valorArchivo, valorBanderaN, valorBanderaJi, valorBanderaJf
    sql = ''
    sql1 = ''
    sql2 = ''

    if (comandoResultado):
        sql = "SELECT fecha, temporada, jornada, equipo1, equipo2, goles1, goles2 FROM laliga "
        sql = sql + f"WHERE equipo1 = '{primerEquipo}' "
        sql = sql + f"AND equipo2 = '{segundoEquipo}' "
        sql = sql + f"AND temporada = '{temporada}' "
    elif (comandoJornada):
        sql = "SELECT fecha, temporada, jornada, equipo1, equipo2, goles1, goles2 FROM laliga "
        sql = sql + f"WHERE temporada = '{temporada}' "
        sql = sql + f"AND jornada = '{valorJornada}' "
    elif (comandoGoles):
        if (comandoLocal or comandoTotal):
            sql1 = "SELECT SUM(goles1) as TotalGoles FROM laliga "
            sql1 = sql1 + f"WHERE equipo1 = '{primerEquipo}' "
            sql1 = sql1 + f"AND temporada = '{temporada}' "
        if (comandoVisitante or comandoTotal):
            sql2 = "SELECT SUM(goles2) as TotalGoles FROM laliga "
            sql2 = sql2 + f"WHERE equipo2 = '{primerEquipo}' "
            sql2 = sql2 + f"AND temporada = '{temporada}' "
    elif (comandoTabla):
        sql1 = f"SELECT DISTINCT(equipo1) FROM laliga WHERE temporada = '{temporada}'"

        sql2 = "SELECT fecha, temporada, jornada, equipo1, equipo2, goles1, goles2 FROM laliga "
        sql2 = sql2 + f"WHERE temporada = '{temporada}' "
        sql2 = sql2 + f"ORDER BY jornada = '{valorJornada}' "
        # La función que calcule puntos debe usarse también para comandoTop
    elif (comandoPartidos):
        sql = "SELECT fecha, temporada, jornada, equipo1, equipo2, goles1, goles2 FROM laliga "
        sql = sql + \
            f"WHERE (equipo1 = '{primerEquipo}' OR equipo2 = '{primerEquipo}') "
        sql = sql + f"AND temporada = '{temporada}' "
        if (banderaJi):
            sql = sql + f"AND jornada >= {valorBanderaJi} "
        if (banderaJf):
            sql = sql + f"AND jornada <= {valorBanderaJf} "
        sql = sql + f"ORDER BY jornada "
    elif (comandoTop):
        sql = "SELECT fecha, temporada, jornada, equipo1, equipo2, goles1, goles2 FROM laliga "
        sql = sql + f"WHERE temporada = '{temporada}' "
        sql = sql + f"ORDER BY jornada = '{valorJornada}' "
        # La función que calcule puntos debe usarse también para comandoTop. Ya teniendo la tabla se escogen los TOP SUPERIOR O INFERIOR.

    if (comandoGoles):
        print(sql1)
        print(sql2)
        filas1 = ConsultaBaseDatos(sql1)
        filas2 = ConsultaBaseDatos(sql2)
    else:
        filas = ConsultaBaseDatos(sql)
        print(sql)

    if (comandoResultado):
        golesPrimerEquipo = filas[0][5]
        golesSegundoEquipo = filas[0][6]

        print(
            f'El resultado de este partido fue: {primerEquipo} {golesPrimerEquipo} - {segundoEquipo} {golesSegundoEquipo}')

    elif (comandoJornada):
        print(filas)

        ProcesarJornada(filas)

    elif (comandoTabla):

        filas1 = ConsultaBaseDatos(sql1)
        filas2 = ConsultaBaseDatos(sql2)
        print(filas1)
        # print(filas2)

        ProcesarTabla(filas1, filas2)

    elif (comandoGoles):
        totalGoles = 0
        expresion = ''
        if (comandoLocal or comandoTotal):
            print(filas1)
            if (comandoLocal):
                expresion = ' como local '
            if (comandoTotal):
                expresion = ' en total '
            totalGoles += int(filas1[0][0])
        if (comandoVisitante or comandoTotal):
            print(filas2)
            if (comandoVisitante):
                expresion = ' como visitante '
            if (comandoTotal):
                expresion = ' en total '
            totalGoles += int(filas2[0][0])

        print(
            f'Los goles anotados por el {primerEquipo} {expresion} en la temporada {temporada} fueron {totalGoles}')

    elif (comandoTabla):
        print(filas)
    elif (comandoPartidos):
        print(filas)
        print(
            f'Generando archivo de resultados de temporada {temporada} del {primerEquipo}')

    elif (comandoTop):
        print(filas)

    print('______________________________________________________________________________________________________________')
    print(comandoActual)


def AnalisisLexico():
    global comandoActual, lexemaActual, inicioSesion, finSesion, numeroComando

    inicioSesion = True
    numeroComando += 1

    estadoTresInicio = False
    estadoTresFinal = False
    estadoCuatroInicio = False
    estadoCuatroFinal = False
    estadoCincoInicio = False
    estadoCincoFinal = False

    i = 0
    j = 0
    columna = 0
    posicion = 0
    lexemaActual = ''

    while i < len(comandoActual):
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
                        # estadoTres(lexemaActual)
                        token = Token('Cadena', lexemaActual,
                                      numeroComando, i-len(lexemaActual)+1)
                        tt.agregar(token)
                        estadoTresInicio = False
                        estadoTresFinal = False
                        lexemaActual = ''
                    else:
                        te.agregar(error=ErrorLexico(
                            'Undefined', lexemaActual, numeroComando, i, 'Lexema inválido'))

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
                        # estadoCuatro(lexemaActual)
                        token = Token('Temporada', lexemaActual,
                                      numeroComando, i-len(lexemaActual)+1)
                        tt.agregar(token)
                        estadoCuatroInicio = False
                        estadoCuatroFinal = False
                    else:
                        te.agregar(error=ErrorLexico(
                            'Undefined', lexemaActual, numeroComando, i, 'Lexema inválido'))

        if (comandoActual[i] == tokens.t_GUION) and estadoCincoInicio == False and not estadoCuatroInicio:
            lexemaActual = lexemaActual + comandoActual[i]
            estadoCincoInicio = True
        else:
            if estadoCincoInicio:
                if (comandoActual[i].strip() != ''):
                    lexemaActual = lexemaActual + comandoActual[i]
                else:
                    estadoCincoFinal = True
                if estadoCincoFinal:
                    if estado5Valido(lexemaActual):
                        token = Token('Bandera', lexemaActual,
                                      numeroComando, i-len(lexemaActual))
                        tt.agregar(token)

                        remainingComandoActual = (comandoActual[i:]).lstrip()
                        if (remainingComandoActual.strip() != ''):
                            j = i + 1
                            lexemaActual = ''
                            posicion = 0
                            tipoToken = ''
                            columna = 0
                            while posicion < len(remainingComandoActual):
                                if (remainingComandoActual[posicion].isalnum() or remainingComandoActual[posicion] == tokens.t_GUIONBAJO):
                                    lexemaActual = lexemaActual + \
                                        remainingComandoActual[posicion]
                                elif (remainingComandoActual[posicion] == tokens.t_GUION):
                                    lexemaActual = lexemaActual + \
                                        remainingComandoActual[posicion]

                                if (remainingComandoActual[posicion].strip() == '' or (posicion == len(remainingComandoActual)-1)):
                                    if estado5Valido(lexemaActual):
                                        tipoToken = 'Bandera'
                                    elif estado6ValidoTokenEntero(lexemaActual):
                                        tipoToken = 'Entero'
                                    elif estado6ValidoTokenArchivo(lexemaActual):
                                        tipoToken = 'Archivo'
                                    else:
                                        tipoToken = 'Indefinido'

                                    columna = j+posicion-len(lexemaActual)
                                    if (posicion == len(remainingComandoActual)-1):
                                        columna += 1

                                    token = Token(tipoToken, lexemaActual,
                                                  numeroComando, columna)
                                    tt.agregar(token)
                                    lexemaActual = ''

                                posicion += 1

                            i += posicion

                        estadoCincoInicio = False
                        estadoCincoFinal = False
                    else:
                        te.agregar(error=ErrorLexico(
                            'Undefined', lexemaActual, numeroComando, i, 'Lexema inválido'))

        if (i < len(comandoActual)):
            if (not estadoTresInicio and not estadoCuatroInicio and not estadoCincoInicio and comandoActual[i].strip() != tokens.t_COMILLA and comandoActual[i].strip() != tokens.t_MAYORQUE):
                if (comandoActual[i].strip() != ''):
                    lexemaActual = lexemaActual + comandoActual[i]
                else:
                    if (lexemaActual.strip() != ''):
                        caracterInicial = lexemaActual[0]
                        if caracterInicial.isupper():
                            if estado1Valido(lexemaActual):
                                # estadoUno(lexemaActual)
                                token = Token('Id', lexemaActual, numeroComando,
                                              i-len(lexemaActual))
                                tt.agregar(token)
                            else:
                                te.agregar(error=ErrorLexico(
                                    'Undefined', lexemaActual, numeroComando, i, 'Lexema inválido'))
                        elif caracterInicial.isdigit():
                            if estado7Valido(lexemaActual):
                                # estadoSeis(lexemaActual)
                                token = Token('Entero', lexemaActual,
                                              numeroComando, i-len(lexemaActual))
                                tt.agregar(token)
                            else:
                                te.agregar(error=ErrorLexico(
                                    'Undefined', lexemaActual, numeroComando, i, 'Lexema inválido'))
                        lexemaActual = ''

        i += 1

    ImprimirTablaTokens(tt)
    AnalisisSintactico(tt)


def ImprimirTablaTokens(tt):
    for to in tt.tokens:
        print(f'{to.id} - {to.lexema} - {to.fila} - {to.columna}')


def AnalisisSintactico(tt):
    global comandoResultado, comandoVersus, comandoTemporada
    global comandoJornada, valorJornada
    global comandoGoles, comandoLocal, comandoVisitante, comandoTotal
    global comandoTabla
    global comandoPartidos
    global comandoTop, comandoSuperior, comandoInferior
    global comandoAdios
    global primerEquipo, segundoEquipo
    global anio1, anio2, temporada
    global banderaArchivo, banderaN, banderaJi, banderaJf
    global valorArchivo, valorBanderaN, valorBanderaJi, valorBanderaJf

    lexema = ''
    i = 0
    for to in tt.tokens:
        lexema = to.lexema
        if (to.id == 'Id'):
            if (lexema == tokens.tr_RESULTADO):
                comandoResultado = True
            elif (lexema == tokens.tr_VERSUS):
                comandoVersus = True
            elif (lexema == tokens.tr_TEMPORADA):
                comandoTemporada = True
            elif (lexema == tokens.tr_JORNADA):
                comandoJornada = True
                if (i < len(tt.tokens)):
                    proximoToken = tt.tokens[tt.tokens.index(to)+1]
                    if (proximoToken.id == 'Entero'):
                        if (proximoToken.lexema).isnumeric():
                            valorJornada = proximoToken.lexema
                        # else: ERROR
                    # else: ERROR

            elif (lexema == tokens.tr_GOLES):
                comandoGoles = True
            elif (lexema == tokens.tr_LOCAL):
                comandoLocal = True
            elif (lexema == tokens.tr_VISITANTE):
                comandoVisitante = True
            elif (lexema == tokens.tr_TOTAL):
                comandoTotal = True
            elif (lexema == tokens.tr_TABLA):
                comandoTabla = True
            elif (lexema == tokens.tr_PARTIDOS):
                comandoPartidos = True
            elif (lexema == tokens.tr_TOP):
                comandoTop = True
            elif (lexema == tokens.tr_SUPERIOR):
                comandoSuperior = True
            elif (lexema == tokens.tr_INFERIOR):
                comandoInferior = True
            elif (lexema == tokens.tr_ADIOS):
                comandoAdios = True
        elif (to.id == 'Cadena'):
            lexema = to.lexema.replace(tokens.t_COMILLA, "")
            if (primerEquipo is None):
                primerEquipo = lexema
            elif (segundoEquipo is None):
                segundoEquipo = lexema
        elif (to.id == 'Temporada'):
            lexema = lexema.replace(tokens.t_MENORQUE, "")
            lexema = lexema.replace(tokens.t_MAYORQUE, "")
            anios = lexema.split("-")
            anio1 = int(anios[0])
            anio2 = int(anios[1])
            temporada = str(anio1) + '-' + str(anio2)
        elif (to.id == 'Bandera'):
            if (i < len(tt.tokens)):
                proximoToken = tt.tokens[tt.tokens.index(to)+1]
                if (lexema == tokens.t_EFE):
                    # and proximoToken.linea == to.linea):
                    if (proximoToken.id == 'Archivo'):
                        banderaArchivo = True
                        valorArchivo = proximoToken.lexema
                    # else: ERROR
                elif (lexema == tokens.t_ENE):
                    # and proximoToken.linea == to.linea):
                    if (proximoToken.id == 'Entero'):
                        banderaN = True
                        valorBanderaN = proximoToken.lexema
                    # else: ERROR
                elif (lexema == tokens.t_JOTAI):
                    # and proximoToken.linea == to.linea):
                    if (proximoToken.id == 'Entero'):
                        banderaJi = True
                        valorBanderaJi = proximoToken.lexema
                    # else: ERROR
                elif (lexema == tokens.t_JOTAF):
                    # and proximoToken.linea == to.linea):
                    if (proximoToken.id == 'Entero'):
                        banderaJf = True
                        valorBanderaJf = proximoToken.lexema
                    # else: ERROR
            # else: ERROR

    # if (comandoResultado and comandoVersus and comandoTemporada):
    #     Resultados()
    Resultados()


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

AnalisisLexico()


# TestBaseDatos()


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
    from gui import InterfazUsuario

    InterfazUsuario()


# CrearInterfazUsuario()

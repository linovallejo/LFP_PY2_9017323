class Token:
    def __init__(self, id, lexema, fila, columna):
        self.id = id
        self.lexema = lexema
        self.fila = fila
        self.columna = columna

class ErrorLexico:
    def __init__(self, token, valor, fila, columna, descripcion):
        self.token = token
        self.valor = valor
        self.fila = fila
        self.columna = columna
        self.descripcion = descripcion

class TablaDeTokens:
    # Esta clase representa la tabla de tokens

    def __init__(self, tokens = []) :
        self.tokens = tokens

    def agregar(self, token) :
        self.tokens.append(token)
    
    def obtener(self, id) :
        if not id in self.tokens :
            print('Error: token ', id, ' no definido.')

        return self.tokens[id]

    def actualizar(self, token) :
        if not token.id in self.tokens :
            print('Error: token ', token.id, ' no definido.')
        else :
            self.tokens[token.id] = token

class TablaDeErrores:
    # Esta clase representa la tabla de errores

    def __init__(self, errores = []) :
        self.errores = errores

    def agregar(self, error) :
        self.errores.append(error)

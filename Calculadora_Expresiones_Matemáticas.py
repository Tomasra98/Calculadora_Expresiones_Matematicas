class Nodo:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class Arbol_Binario:
    def __init__(self):
        self.root = None

    def imprimir_arbol(self, nodo, prefix="", is_left=True):
        if not nodo:
            print("Arbol Vacio")
            return
        if nodo.right:
            self.imprimir_arbol(nodo.right, prefix + ("│   " if is_left else "    "), False)
        print(prefix + ("└── " if is_left else "┌── ") + str(nodo.value))
        if nodo.left:
            self.imprimir_arbol(nodo.left, prefix + ("    " if is_left else "│   "), True)

class Calculadora:
    def __init__(self):
        pass

    def crear_arbol(self):
        arbol = Arbol_Binario()
        return arbol

    def separar_expresion(self, expresion):
        lista_datos = []
        for digito in expresion:
            lista_datos.append(digito)

        digitos = []
        i = 0
        while i < len(lista_datos):
            if lista_datos[i].isdigit():
                numero = lista_datos[i]
                while (i + 1 < len(lista_datos) and lista_datos[i + 1].isdigit()):
                    i += 1
                    numero += lista_datos[i]
                digitos.append(numero)
            elif lista_datos[i] == " " and lista_datos[i+1]:
                if lista_datos[i+1] != " ":
                    digitos.append(" ")
            else:
                elemento = lista_datos[i]
                if lista_datos[i] == "*" and lista_datos[i+1] == "*":
                    elemento += lista_datos[i+1]
                    i += 1
                digitos.append(elemento)
            i += 1
        print(digitos)
        return digitos
    
    def quitar_espacios(self, lista_datos):
        digitos = []
        for dato in lista_datos:
            if dato != " ":
                digitos.append(dato)
        return digitos

    def infija_a_postfija(self, digitos):
        importancia = {'+': 1, '-': 1, '*': 2, '/': 2, '**': 3, '* *': 3, 'd': 4}
        postfija = []
        operadores = []
        
        for digito in digitos:
            if (digito.isdigit()):
                postfija.append(digito)

            elif (digito in importancia):
                while (operadores and operadores[-1] in importancia and
                    importancia[operadores[-1]] >= importancia[digito]):
                    postfija.append(operadores.pop())
                operadores.append(digito)
            elif digito == '(':
                operadores.append(digito)
            elif digito == ')':
                while operadores and operadores[-1] != '(':
                    postfija.append(operadores.pop())
                operadores.pop()

        while operadores:
            postfija.append(operadores.pop())

        return postfija

    def cargar_arbol(self, postfija, arbol):
        pila = []
        
        for digito in postfija:
            if digito.isdigit():
                pila.append(Nodo(digito))

            else:                                                       
                nodo = Nodo(digito)                                        
                nodo.right = pila.pop()
                nodo.left = pila.pop()
                pila.append(nodo)
        
        arbol.root = pila[0]
        return

    def calcular_arbol(self, nodo):
        if nodo.value.isdigit():
            return int(nodo.value)
        
        nodo_izquierdo = self.calcular_arbol(nodo.left)
        nodo_derecho = self.calcular_arbol(nodo.right)
        
        if nodo.value == '+':
            return nodo_izquierdo + nodo_derecho
        elif nodo.value == '-':
            return nodo_izquierdo - nodo_derecho
        elif nodo.value == '*':
            return nodo_izquierdo * nodo_derecho
        elif nodo.value == '/':
            return nodo_izquierdo / nodo_derecho
        elif nodo.value == '**' or nodo.value == "* *":
            return nodo_izquierdo ** nodo_derecho
        elif nodo.value == 'd':
            if nodo_izquierdo < nodo_derecho:
                return nodo_izquierdo + nodo_derecho
            if nodo_izquierdo > nodo_derecho:
                return nodo_izquierdo - nodo_derecho

    def verificar(self, digitos):
        LISTA_OPERACIONES = ["*", "/", "+", "-", "d"]

        operandos = 0
        operadores = 0
        lista_datos = digitos
        for digito in range(len(lista_datos)):
            if lista_datos[digito] == " ":
                if lista_datos[digito-1].isdigit() and lista_datos[digito+1].isdigit():
                    return "Error: faltan operadores"
                elif lista_datos[digito-1] == "(" and lista_datos[digito+1] in LISTA_OPERACIONES or lista_datos[digito-1] in LISTA_OPERACIONES and lista_datos[digito+1] == ")":  
                    return "Error: faltan operandos"
                elif lista_datos[digito-1].isdigit() and lista_datos[digito+1] == "(" or lista_datos[digito-1] == ")" and lista_datos[digito+1].isdigit():    
                    return "Error: faltan operadores"
                elif lista_datos[digito-1] == ")" and lista_datos[digito+1] == "(":    
                    return "Error: faltan operadores"
                else:
                    pass

            # if lista_datos[-1] == ")":
            #     pass
            if lista_datos[digito] != lista_datos[-1]:
                if lista_datos[digito] == ")" and lista_datos[digito+1] == "(":
                        return "Error: faltan operadores"
            if lista_datos[digito].isdigit():
                operandos += 1
            if lista_datos[digito] in LISTA_OPERACIONES:
                operadores += 1
        if operandos - operadores < 1:
            return "Error: faltan operandos"

        balance_parentesis = 0
        for parentesis in digitos:
            if parentesis == '(':
                balance_parentesis += 1
            elif parentesis == ')':
                balance_parentesis -= 1
            if balance_parentesis < 0:
                return "Error: paréntesis desbalanceados"    
        if balance_parentesis != 0:
            return "Error: paréntesis desbalanceados"
            
        lista_combinaciones = []
        for i in range(len(LISTA_OPERACIONES)):
            for j in range(len(LISTA_OPERACIONES)):
                combinacion = ""
                combinacion += LISTA_OPERACIONES[i]
                combinacion += " "
                combinacion += LISTA_OPERACIONES[j]
                if combinacion != "* *":
                    lista_combinaciones.append(combinacion)
        for combinacion in lista_combinaciones:
            if combinacion in digitos:
                return "Error: operadores consecutivos"
            
        lista_combinaciones = []
        for i in range(len(LISTA_OPERACIONES)):
            for j in range(len(LISTA_OPERACIONES)):
                combinacion = ""
                combinacion += LISTA_OPERACIONES[i]
                combinacion += LISTA_OPERACIONES[j]
                if combinacion != "**":
                    lista_combinaciones.append(combinacion)
        for combinacion in lista_combinaciones:
            if combinacion in digitos:
                return "Error: operadores consecutivos"
        
        return None


    def calculadora(self, expresion):
        lista_datos = self.separar_expresion(expresion)
        error = self.verificar(lista_datos)
        if error:
            return error
        
        try:
            arbol = self.crear_arbol()
            digitos = self.quitar_espacios(lista_datos)
            postfija = self.infija_a_postfija(digitos)
            self.cargar_arbol(postfija, arbol)
            print("Árbol de Expresión:")
            arbol.imprimir_arbol(arbol.root)
            result = self.calcular_arbol(arbol.root)
            return f"Resultado: {result}"
        except Exception as e:
            return f"Error: {str(e)}"

calc = Calculadora()
print(calc.calculadora("4d8d5+(58-23+3)"))
print()



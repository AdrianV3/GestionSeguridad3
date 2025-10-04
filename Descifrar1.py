import re
import itertools

from operator import truediv

mensaje = """RIJ AZKKZHC PIKCE XT ACKCUXJHX SZX, E NZ PEJXKE, PXGIK XFDKXNEQE RIPI RIPQEHCK ET OENRCNPI AXNAX ZJ RKCHXKCI AX CJAXDXJAXJRCE
AX RTENX, E ACOXKXJRCE AXT RITEQIKERCIJCNPI OKXJHXDIDZTCNHE AX TE ACKXRRCIJ EJEKSZCNHE.
AZKKZHC OZX ZJ OERHIK AX DKCPXK IKAXJ XJ XT DEDXT AX TE RTENX IQKXKE XJ REHETZJVE XJ GZTCI AX 1936. DXKI AZKKZHC, RIPI IRZKKX RIJ
TEN DXKNIJETCAEAXN XJ TE MCNHIKCE, JI REVI AXT RCXTI. DXKNIJCOCREQE TE HKEACRCIJ KXVITZRCIJEKCE AX TE RTENX IQKXKE. NZ XJIKPX
DIDZTEKCAEA XJHKX TE RTENX HKEQEGEAIKE, KXOTXGEAE XJ XT XJHCXKKI PZTHCHZACJEKCI XJ QEKRXTIJE XT 22 AX JIVCXPQKX AX 1936,
PZXNHKE XNE CAXJHCOCRERCIJ. NZ PZXKHX OZX NCJ AZAE ZJ UITDX IQGXHCVI ET DKIRXNI KXVITZRCIJEKCI XJ PEKRME. NCJ AZKKZHC SZXAI PEN
TCQKX XT REPCJI DEKE SZX XT XNHETCJCNPI, RIJ TE RIPDTCRCAEA AXT UIQCXKJI AXT OKXJHX DIDZTEK V AX TE ACKXRRCIJ EJEKSZCNHE,
HXKPCJEKE XJ PEVI AX 1937 TE HEKXE AX TCSZCAEK TE KXVITZRCIJ, AXNPIKETCLEJAI E TE RTENX IQKXKE V OERCTCHEJAI RIJ XTTI XT DINHXKCIK
HKCZJOI OKEJSZCNHE."""

frecs = {c: 0 for c in "ABCDEFGHIJKLNMÑOPQRSTUVWXYZ"}
espFrecs = {c: 0 for c in "ABCDEFGHIJKLNMÑOPQRSTUVWXYZ"}
espValores = [11.96,0.92,2.92,6.87,16.78,0.52,0.73,0.89,4.15,0.3,0,8.37,7.01,2.12,0.29,0.73,2.776,1.53,4.94,7.88,3.31,4.8,0.39,0,0.06,1.54,0.15]

for i,c in enumerate ("ABCDEFGHIJKLNMÑOPQRSTUVWXYZ"):
    espFrecs[c] = espValores[i]

for c in mensaje:
    if re.match(r'[A-Z]', c):
        frecs[c] = frecs[c] + 1


#key = lambda x: x[1] para que se fije en el segundo valor del diccionario, que son los números
#reverse para ordenar de mayor a menor
frecsOrdenadas = sorted(frecs.items(), key = lambda x: x[1], reverse = True)
espFrecsOrdenadas = sorted(espFrecs.items(), key = lambda x: x[1], reverse = True)
descifrado = {}

for letra, valor in frecsOrdenadas:
    print(letra, valor)

print('\n')

for letra, valor in espFrecsOrdenadas:
    print(letra, valor)

print('\n')

for (letra, _), (letraDescifrada, _) in zip (frecsOrdenadas, espFrecsOrdenadas):
    descifrado[letra] = letraDescifrada
    print(letra, letraDescifrada)


print('\n')


def  descifrar(msg, diccionario):
    mensajeDescifrado = ""
    for c in msg:
        if re.match(r'[A-Z]', c):
            mensajeDescifrado = mensajeDescifrado + diccionario[c]
        else:
            mensajeDescifrado = mensajeDescifrado + c
    return mensajeDescifrado

DescMsg = descifrar(mensaje, descifrado)

print(DescMsg)

#Fijandose en las palabras repetidas: AX del texto cifrado, justo antes de una fecha, y palabras como: XT, E, NZ, V, XJ
cambiosPosibles = {

    "A": ["D"],
    "X": ["E"],
    "E": ["A"],
    "V": ["Y"],
    "T": ["L"],
    "Z": ["U"],
    "N": ["S"],
    "S": ["Q"],
    "K": ["R"],
    "J": ["N"],
    "H": ["T"],
    "R": ["C"],
    "G": ["J"],
    "I": ["O"],
    "O": ["F"],
    "D": ["P"],
    "L": ["Z"],
    "F": ["X"],
    "M": ["H"]

}

# Para testear que se hagan las combinaciones bien
test = {

    "A": ["B"],
    "B": ["C"]
}

# Intercambiar valores entre dos letras (ej. inicialmente: X -> E, E -> A, despues: X -> A , E -> E)
def swap(diccionario, letra, nueva):

    dic = diccionario.copy()
    aux = dic[letra]

    for indice in diccionario:

        if diccionario[indice] == nueva:
            dic[indice] = aux
            dic[letra] = nueva
            break

    return dic

# ******************* ESTA PARTE LA HICE PARA BUSCAR POSIBILIDADES PERO NO ME SIRVIÓ ********************************
# Generar todas las combinaciones posibles de sustituciones de letras cifradas
def aplicar_cambios(descifrado_base, cambios):

    #Obtener array de las letras cifradas que sustituiremos
    letras = list(cambios.keys())
    opciones = []

    #Obtener array de arrays de las letras por las que sustituiremos las cifradas
    #Añadimos la posibilidad de no sustituir (con None) la letra cifrada por otra letra descifrada, y así poder tener todas las combinaciones
    for letra in letras:
        ops = list(cambios[letra])
        ops.append(None)
        opciones.append(ops)

    # Producto cartesiano: todas las combinaciones de elecciones
    for combinacion in itertools.product(*opciones):

        #Si no se sustituye nada, no lo ponemos por pantalla
        if all (o is None for o in combinacion):
            continue

        dic = descifrado_base.copy()
        #Combinamos el array de letras cifradas que vamos a sustituir por las posibles letras descifradas
        #Repetimos esto con cada combinación posible
        for letra, nueva_letra in zip(letras, combinacion):
            #Para cada sustitución, intercambiamos las letras para que no haya repetidas
            if nueva_letra is not None:
                dic = swap(dic, letra, nueva_letra)
            #Yield permite ir devolviendo todos los distintos diccionarios que nos van saliendo con todas las posibles sutituciones
        yield dic


def cambiar_sustitucion(dic, letra_cifrada, nueva_letra):
    """
    Cambia el mapeo de 'letra_cifrada' → 'nueva_letra' en el diccionario 'dic',
    asegurando que no se repitan letras (swap si es necesario).
    """
    conflicto = None
    for k, v in dic.items():
        if v == nueva_letra:
            conflicto = k
            break

    anterior = dic[letra_cifrada]
    dic[letra_cifrada] = nueva_letra
    if conflicto and conflicto != letra_cifrada:
        dic[conflicto] = anterior


# Generar combinaciones

for i, dic in enumerate(aplicar_cambios(descifrado, cambiosPosibles), 1):
    print(f"\n--- Combinación {i} ---")
    print(dic)
    DescMsg = descifrar(mensaje,dic)
    print(DescMsg)
    input("Pulsa ENTER para continuar")

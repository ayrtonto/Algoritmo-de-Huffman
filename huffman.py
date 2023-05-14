from collections import Counter
import os

class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

def construir_arbol_huffman(frecuencias):
    frecuencias_ordenadas = sorted(frecuencias.items(), key=lambda x: x[1])
    
    nodos = [NodoHuffman(caracter, frecuencia) for caracter, frecuencia in frecuencias_ordenadas]
    
    while len(nodos) > 1:
        nodo1 = nodos.pop(0)
        nodo2 = nodos.pop(0)
        i = 0

        nodo_combinado = NodoHuffman(None, nodo1.frecuencia + nodo2.frecuencia)
        nodo_combinado.izquierda = nodo1
        nodo_combinado.derecha = nodo2
        
        while i < len(nodos) and nodos[i].frecuencia < nodo_combinado.frecuencia:
            i += 1
        
        nodos.insert(i, nodo_combinado)
    
    return nodos[0]

def generar_codigos_huffman(arbol, codigo_actual, codigos):
    if arbol.caracter is not None:
        codigos[arbol.caracter] = codigo_actual
    else:
        generar_codigos_huffman(arbol.izquierda, codigo_actual + '0', codigos)
        generar_codigos_huffman(arbol.derecha, codigo_actual + '1', codigos)

def mostrar_tabla_huffman(codigos):
    print("Letra\tFrecuencia\tCódigo Huffman")
    for letra, codigo in codigos.items():
        frecuencia = frecuencias[letra]
        print(f"{letra}\t{frecuencia}\t\t{codigo}")

def codificar_huffman(texto, arbol):
    codigos = {}
    generar_codigos_huffman(arbol, '', codigos)
    
    texto_codificado = ''
    for caracter in texto:
        texto_codificado += codigos[caracter]
    
    return texto_codificado

def decodificar_huffman(texto_codificado, arbol):
    texto_decodificado = ''
    nodo_actual = arbol
    
    for bit in texto_codificado:
        if bit == '0':
            nodo_actual = nodo_actual.izquierda
        else:
            nodo_actual = nodo_actual.derecha
        
        if nodo_actual.caracter is not None:
            texto_decodificado += nodo_actual.caracter
            nodo_actual = arbol
    
    return texto_decodificado

archivo_entrada = "entrada.txt"
if not os.path.isfile(archivo_entrada):
    texto_inicial = "tres tristes tigres comian trigo en tres tristes platos, sentados en un trigal. sentados en un trigal, en tres tristes platos, comian trigo tres tristes tigres."
    with open(archivo_entrada, "w") as archivo:
        archivo.write(texto_inicial)

with open(archivo_entrada, "r") as archivo:
    texto = archivo.read()

frecuencias = dict(Counter(texto))
arbol = construir_arbol_huffman(frecuencias)
codigos = {}
generar_codigos_huffman(arbol, '', codigos)

print("\nTexto original:", texto)

print("\nTabla Huffman:")
mostrar_tabla_huffman(codigos)

texto_codificado = codificar_huffman(texto, arbol)
texto_decodificado = decodificar_huffman(texto_codificado, arbol)

print("\nTexto codificado:", texto_codificado)
print("Texto decodificado:", texto_decodificado)

print("\nCantidad de bytes que usa el texto original:\t", len(texto)*8)
print("Cantidad de bytes que usa el texto codificado:\t", len(texto_codificado))
print("El numero de bits utilizados se ha reducido a:\t", round(len(texto_codificado)/(len(texto)*8)*100, 2),"%")

archivo_salida = "salida.txt"
with open(archivo_salida, "w") as archivo:
    archivo.write(texto_codificado)
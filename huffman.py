import tkinter as tk
from tkinter import messagebox, filedialog
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

def codificar_huffman(texto, arbol):
    codigos = {}
    generar_codigos_huffman(arbol, '', codigos)
    
    texto_codificado = ''
    for caracter in texto:
        texto_codificado += codigos[caracter]
    
    return texto_codificado

def calcular_bytes(texto):
    return len(texto.encode())

def calcular_porcentaje_reduccion(texto_original, texto_codificado):
    bytes_originales = calcular_bytes(texto_original)
    bytes_codificados = calcular_bytes(texto_codificado)
    porcentaje_reduccion = round((bytes_codificados / (bytes_originales * 8)) * 100, 2)
    return porcentaje_reduccion

def abrir_ventana_codificar_texto():
    def codificar_texto():
        texto_original = texto_entrada.get("1.0", "end-1c")

        frecuencias = dict(Counter(texto_original))
        arbol = construir_arbol_huffman(frecuencias)
        codigos = {}
        generar_codigos_huffman(arbol, '', codigos)

        texto_codificado = codificar_huffman(texto_original, arbol)

        salida_texto.delete("1.0", "end")
        salida_texto.insert("1.0", texto_codificado)

        tabla_huffman_texto.delete("1.0", "end")
        tabla_huffman_texto.insert("1.0", "Letra\tFrecuencia\t\tCódigo Huffman\n")
        for letra, codigo in codigos.items():
            frecuencia = frecuencias[letra]
            tabla_huffman_texto.insert("end", f"{letra}\t{frecuencia}\t\t{codigo}\n")

        bytes_originales_label["text"] = f"Cantidad de bytes que usa el texto original: {len(texto_original) * 8}"
        bytes_codificados_label["text"] = f"Cantidad de bytes que usa el texto codificado: {len(texto_codificado)}"
        porcentaje_reduccion_label["text"] = f"El número de bits utilizados se ha reducido a: {round(len(texto_codificado) / (len(texto_original) * 8) * 100, 2)}%"

    ventana_codificar_texto = tk.Toplevel(ventana_principal)
    ventana_codificar_texto.title("Codificar Texto")

    etiqueta_entrada = tk.Label(ventana_codificar_texto, text="Texto a codificar:")
    etiqueta_entrada.pack()

    texto_entrada = tk.Text(ventana_codificar_texto, height=5, width=40)
    texto_entrada.pack()

    boton_codificar = tk.Button(ventana_codificar_texto, text="Codificar", command=codificar_texto)
    boton_codificar.pack()

    etiqueta_salida = tk.Label(ventana_codificar_texto, text="Texto codificado:")
    etiqueta_salida.pack()

    salida_texto = tk.Text(ventana_codificar_texto, height=5, width=40)
    salida_texto.pack()

    etiqueta_tabla_huffman = tk.Label(ventana_codificar_texto, text="Tabla de Huffman:")
    etiqueta_tabla_huffman.pack()

    tabla_huffman_texto = tk.Text(ventana_codificar_texto, height=10, width=40)
    tabla_huffman_texto.pack()

    bytes_originales_label = tk.Label(ventana_codificar_texto, text="Cantidad de bytes que usa el texto original:")
    bytes_originales_label.pack()

    bytes_codificados_label = tk.Label(ventana_codificar_texto, text="Cantidad de bytes que usa el texto codificado:")
    bytes_codificados_label.pack()

    porcentaje_reduccion_label = tk.Label(ventana_codificar_texto, text="El número de bits utilizados se ha reducido a:")
    porcentaje_reduccion_label.pack()

def abrir_ventana_codificar_archivo():
    def codificar_archivo():
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])

        if archivo:
            ruta_entrada = os.path.abspath(archivo)
            ruta_carpeta = os.path.dirname(archivo)
            nombre_archivo = os.path.splitext(os.path.basename(ruta_entrada))[0]

            with open(archivo, "r") as archivo_entrada:
                texto_original = archivo_entrada.read()

            frecuencias = dict(Counter(texto_original))
            arbol = construir_arbol_huffman(frecuencias)
            codigos = {}
            generar_codigos_huffman(arbol, '', codigos)

            texto_codificado = codificar_huffman(texto_original, arbol)

            texto_codificado_texto.delete("1.0", "end")
            texto_codificado_texto.insert("1.0", texto_codificado)

            tabla_huffman_texto.delete("1.0", "end")
            tabla_huffman_texto.insert("1.0", "Letra\tFrecuencia\t\tCódigo Huffman\n")
            for letra, codigo in codigos.items():
                frecuencia = frecuencias[letra]
                tabla_huffman_texto.insert("end", f"{letra}\t{frecuencia}\t\t{codigo}\n")

            bytes_originales_label["text"] = f"Cantidad de bytes que usa el texto original: {len(texto_original) * 8}"
            bytes_codificados_label["text"] = f"Cantidad de bytes que usa el texto codificado: {len(texto_codificado)}"
            porcentaje_reduccion_label["text"] = f"El número de bits utilizados se ha reducido a: {round(len(texto_codificado) / (len(texto_original) * 8) * 100, 2)}%"

            archivo_salida = f"{nombre_archivo}_codificado.txt"
            ruta_salida = os.path.join(ruta_carpeta, archivo_salida)
            with open(ruta_salida, "w") as archivo:
                archivo.write(texto_codificado)

            messagebox.showinfo("Codificación Completada", "El archivo ha sido codificado y guardado como \""+ archivo_salida+"\"")

    ventana_codificar_archivo = tk.Toplevel(ventana_principal)
    ventana_codificar_archivo.title("Codificar Archivo")

    etiqueta_titulo = tk.Label(ventana_codificar_archivo, text="Codificar Archivo", font=("Helvetica", 16))
    etiqueta_titulo.pack(pady=20)

    boton_seleccionar_archivo = tk.Button(ventana_codificar_archivo, text="Seleccionar Archivo", command=codificar_archivo)
    boton_seleccionar_archivo.pack()

    etiqueta_resultados = tk.Label(ventana_codificar_archivo, text="Resultados:")
    etiqueta_resultados.pack()

    etiqueta_texto_codificado = tk.Label(ventana_codificar_archivo, text="Texto Codificado:")
    etiqueta_texto_codificado.pack()

    texto_codificado_texto = tk.Text(ventana_codificar_archivo, width=50, height=10)
    texto_codificado_texto.pack()

    etiqueta_tabla_huffman = tk.Label(ventana_codificar_archivo, text="Tabla Huffman:")
    etiqueta_tabla_huffman.pack()

    tabla_huffman_texto = tk.Text(ventana_codificar_archivo, width=50, height=10)
    tabla_huffman_texto.pack()

    bytes_originales_label = tk.Label(ventana_codificar_archivo, text="")
    bytes_originales_label.pack()

    bytes_codificados_label = tk.Label(ventana_codificar_archivo, text="")
    bytes_codificados_label.pack()

    porcentaje_reduccion_label = tk.Label(ventana_codificar_archivo, text="")
    porcentaje_reduccion_label.pack()

    ventana_codificar_archivo.mainloop()

def salir():
    ventana_principal.destroy()

ventana_principal = tk.Tk()
ventana_principal.title("Menú Principal")

ventana_principal.geometry("400x300")

etiqueta_titulo = tk.Label(ventana_principal, text="Menú Principal", font=("Helvetica", 16))
etiqueta_titulo.pack(pady=20)

boton_codificar_texto = tk.Button(ventana_principal, text="Codificar Texto", command=abrir_ventana_codificar_texto)
boton_codificar_texto.pack()

boton_codificar_archivo = tk.Button(ventana_principal, text="Codificar Archivo", command=abrir_ventana_codificar_archivo)
boton_codificar_archivo.pack()

boton_salir = tk.Button(ventana_principal, text="Salir", command=salir)
boton_salir.pack()

ventana_principal.mainloop()
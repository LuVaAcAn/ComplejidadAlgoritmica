from flask import Flask, render_template, request, jsonify
import csv
import io
import random
import networkx as nx
import matplotlib.pyplot as plt
from difflib import SequenceMatcher
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grafo', methods=['POST'])
def generar_grafo():
    # Obtener la cantidad de nodos ingresada por el usuario
    cantidad_nodos = int(request.form['cantidad-nodos'])
    nombre_padre = request.form['nombre-padre']
    nombre_evitar = request.form['nombre-evitar']
    genero = request.form['genero']

    # Leer el archivo CSV
    with open('NationalNames.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)

        # Crear el grafo y añadir los nodos
        grafo = nx.Graph()
        contador_nodos = 0
        for fila in csv_reader:
            nombre = fila[1]
            año = int(fila[2])
            cant_apariciones = int(fila[4])
            genero_nombre = fila[3]
            
            if genero == 'ambos' or (genero == 'hombre' and genero_nombre == 'M') or (genero == 'mujer' and genero_nombre == 'F'):
                if nombre_padre[-3:] in nombre and nombre_evitar[-3:] not in nombre:
                    grafo.add_node(nombre, año=año, cant_apariciones=cant_apariciones)
                    contador_nodos += 1
            if contador_nodos == cantidad_nodos:
                break

        # Calcular la similitud entre nodos y añadir aristas
        aristas = []
        for nodo1 in grafo.nodes:
            for nodo2 in grafo.nodes:
                if nodo1 != nodo2:
                    similitud = calcular_similitud(nodo1, nodo2)
                    año1 = grafo.nodes[nodo1]['año']
                    año2 = grafo.nodes[nodo2]['año']
                    cant_apariciones1 = grafo.nodes[nodo1]['cant_apariciones']
                    cant_apariciones2 = grafo.nodes[nodo2]['cant_apariciones']

                    if similitud > 0.28 and abs(año1 - año2) <= 10 and abs(cant_apariciones1 - cant_apariciones2) <= 1500:
                        peso = similitud
                        aristas.append((nodo1, nodo2, peso))

        grafo.add_weighted_edges_from(aristas)

        # Generar el grafo sin puentes
        grafo_sin_puentes = kruskal(grafo)

        # Eliminar el atributo de peso en las aristas
        for edge in grafo_sin_puentes.edges:
            grafo_sin_puentes.edges[edge].pop('weight', None)

        # Obtener nombres más populares
        nombres_populares = sorted(grafo.nodes(data=True), key=lambda x: x[1]['cant_apariciones'], reverse=True)[:10]
        nombres_populares = [(nombre[0], nombre[1]['cant_apariciones']) for nombre in nombres_populares]

        # Obtener nombres menos populares
        nombres_menos_populares = sorted(grafo.nodes(data=True), key=lambda x: x[1]['cant_apariciones'], reverse=False)[:10]
        nombres_menos_populares = [(nombre[0], nombre[1]['cant_apariciones']) for nombre in nombres_menos_populares]

        # Generar la imagen del grafo
        fig, ax = plt.subplots(figsize=(15, 15))
        posiciones = nx.kamada_kawai_layout(grafo_sin_puentes)
        nx.draw_networkx(grafo_sin_puentes, pos=posiciones, with_labels=True,
                         node_size=100, node_color='orange', font_size=8, font_weight='normal',
                         width=0.5, edge_color='gray', style='solid')
        plt.axis('off')
        plt.savefig('static/grafo.png')
        plt.close()

    # Devolver los nombres populares y la ruta de la imagen generada
    respuesta = {'nombres_populares': nombres_populares, 'imagen_grafo': 'static/grafo.png', 'nombres_menos_populares': nombres_menos_populares}
    return jsonify(respuesta)

def calcular_similitud(nombre1, nombre2):
    ultimos_caracteres1 = nombre1[-3:]
    ultimos_caracteres2 = nombre2[-3:]
    return SequenceMatcher(None, ultimos_caracteres1, ultimos_caracteres2).ratio()

def kruskal(grafo):
    aristas_ordenadas = sorted(grafo.edges(data=True), key=lambda x: x[2]['weight'])
    grafo_arbol = nx.Graph()

    for nodo in grafo.nodes:
        grafo_arbol.add_node(nodo)

    for arista in aristas_ordenadas:
        nodo1, nodo2, peso = arista
        if nx.has_path(grafo_arbol, nodo1, nodo2):
            continue
        grafo_arbol.add_edge(nodo1, nodo2, weight=peso)

    return grafo_arbol

if __name__ == '__main__':
    app.run(debug=True)

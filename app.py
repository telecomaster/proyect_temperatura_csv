from flask import Flask, render_template, request
import csv

app = Flask(__name__)

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para la consulta de datos
@app.route('/consulta')
def consulta():
    ciudad = request.args.get('ciudad')
    resultados = []
    with open('datos.csv', 'r') as archivo:
        lector_csv = csv.reader(archivo, delimiter=';')  # Utilizar punto y coma como separador
        next(lector_csv)  # Omitir la primera línea de encabezados
        for fila in lector_csv:
            #print(fila)  # Agregar esta línea para imprimir los datos en la consola del servidor
            if fila[0].lower() == ciudad.lower():
                fecha = fila[3]
                temperatura = float(fila[1])
                probabilidad_lluvia = float(fila[2])
                resultados.append((fecha, temperatura, probabilidad_lluvia))
    
    # Realiza la conversión a float antes de pasar los datos a la plantilla
    resultados = [(fecha, float(temperatura), float(probabilidad_lluvia)) for fecha, temperatura, probabilidad_lluvia in resultados]
    
    return render_template('consulta.html', ciudad=ciudad, resultados=resultados)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

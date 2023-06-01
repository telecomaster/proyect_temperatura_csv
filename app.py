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
        lector_csv = csv.reader(archivo)
        for fila in lector_csv:
            print(fila)  # Agregar esta línea para imprimir los datos en la consola del servidor
            if fila[0].lower() == ciudad.lower():
                fecha = fila[3]
                temperatura = float(fila[1])
                probabilidad_lluvia = float(fila[2])
                resultados.append((fecha, temperatura, probabilidad_lluvia))
    
    return render_template('consulta.html', ciudad=ciudad, resultados=resultados)
if __name__ == '__main__':
   app.run(host= "0.0.0.0", port=5000)

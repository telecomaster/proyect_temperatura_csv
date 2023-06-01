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

@app.route('/consulta_probabilidad', methods=['GET'])
def consulta_probabilidad():
    probabilidad = float(request.args.get('probabilidad'))
    registros = []

    with open('datos.csv', 'r') as archivo:
        lector_csv = csv.reader(archivo, delimiter=';')
        next(lector_csv)  # Omitir la primera línea de encabezados
        for fila in lector_csv:
            ciudad = fila[0]
            temperatura = float(fila[1])
            probabilidad_lluvia = float(fila[2])
            fecha = fila[3]
            registros.append({'Ciudad': ciudad, 'Temperatura': temperatura, 'Probabilidad de lluvia': probabilidad_lluvia, 'Fecha': fecha})

    registros_filtrados = [registro for registro in registros if registro['Probabilidad de lluvia'] >= probabilidad]

    ciudad_max_probabilidad = next((registro['Ciudad'] for registro in registros if registro['Probabilidad de lluvia'] == 100), None)

    return render_template('consulta_probabilidad.html', probabilidad=probabilidad, registros=registros_filtrados, ciudad_max_probabilidad=ciudad_max_probabilidad)
    
@app.route('/consulta_temperatura_baja', methods=['GET'])
def consulta_temperatura_baja():
    registros = []

    with open('datos.csv', 'r') as archivo:
        lector_csv = csv.reader(archivo, delimiter=';')
        next(lector_csv)  # Omitir la primera línea de encabezados
        for fila in lector_csv:
            ciudad = fila[0]
            temperatura = float(fila[1])
            probabilidad_lluvia = float(fila[2])
            fecha = fila[3]
            registros.append({'Ciudad': ciudad, 'Temperatura': temperatura, 'Probabilidad de lluvia': probabilidad_lluvia, 'Fecha': fecha})

    temperatura_minima = min(registros, key=lambda x: x['Temperatura'])
    ciudad_temperatura_minima = temperatura_minima['Ciudad']
    temperatura_minima_valor = temperatura_minima['Temperatura']
    fecha_temperatura_minima = temperatura_minima['Fecha']

    return render_template('consulta_temperatura_baja.html', ciudad_temperatura_minima=ciudad_temperatura_minima, temperatura_minima=temperatura_minima_valor, fecha_temperatura_minima=fecha_temperatura_minima)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api',methods=['GET'])
def api():
    n = int (request.args.get('n',3))
    matriz = []
    contador = 1
    for i in range(n):
        fila=[]
        for j in range(n):
            fila.append(contador)
            contador += 1
        matriz.append(fila)

    return jsonify(matriz)

@app.route('/ejercicio1/<cadena>')
def ejercicio1(cadena):

    for i in range(len(cadena) // 2):
        if cadena[i] != cadena[len(cadena) -1 -i]:
            return "falso"
    return "verdadero" 





if __name__ == '__main__':
    app.run(debug=True)
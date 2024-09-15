from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Base de datos en memoria
pokemons = []
pokemon_id = 1

# Ruta para obtener todos los Pokémon
@app.route('/pokemons', methods=['GET'])
def get_pokemons():
    return jsonify(pokemons), 200

# Ruta para obtener un Pokémon por ID
@app.route('/pokemons/<int:id>', methods=['GET'])
def get_pokemon(id):
    pokemon = next((poke for poke in pokemons if poke['id'] == id), None)
    if pokemon:
        return jsonify(pokemon), 200
    else:
        abort(404, description="Pokémon no encontrado")

# Ruta para crear un nuevo Pokémon
@app.route('/pokemons', methods=['POST'])
def create_pokemon():
    global pokemon_id
    if not request.json or not 'nombre' in request.json:
        abort(400, description="Datos del Pokémon faltantes")

    pokemon = {
        'id': pokemon_id,
        'nombre': request.json['nombre'],
        'imagen': request.json.get('imagen', ''),
        'caracteristicas': {
            'peso': request.json['caracteristicas'].get('peso', 0.0),
            'altura': request.json['caracteristicas'].get('altura', 0.0),
            'fuerza': request.json['caracteristicas'].get('fuerza', 0),
            'edad': request.json['caracteristicas'].get('edad', 0),
        },
        'habilidades': request.json.get('habilidades', []),
        'tipo': request.json.get('tipo', ''),
        'habitat': request.json.get('habitat', '')
    }

    pokemons.append(pokemon)
    pokemon_id += 1
    return jsonify(pokemon), 201

# Ruta para actualizar un Pokémon por ID
@app.route('/pokemons/<int:id>', methods=['PUT'])
def update_pokemon(id):
    pokemon = next((poke for poke in pokemons if poke['id'] == id), None)
    if not pokemon:
        abort(404, description="Pokémon no encontrado")

    if not request.json:
        abort(400, description="Solicitud incorrecta")
    
    pokemon['nombre'] = request.json.get('nombre', pokemon['nombre'])
    pokemon['imagen'] = request.json.get('imagen', pokemon['imagen'])
    pokemon['caracteristicas']['peso'] = request.json['caracteristicas'].get('peso', pokemon['caracteristicas']['peso'])
    pokemon['caracteristicas']['altura'] = request.json['caracteristicas'].get('altura', pokemon['caracteristicas']['altura'])
    pokemon['caracteristicas']['fuerza'] = request.json['caracteristicas'].get('fuerza', pokemon['caracteristicas']['fuerza'])
    pokemon['caracteristicas']['edad'] = request.json['caracteristicas'].get('edad', pokemon['caracteristicas']['edad'])
    pokemon['habilidades'] = request.json.get('habilidades', pokemon['habilidades'])
    pokemon['tipo'] = request.json.get('tipo', pokemon['tipo'])
    pokemon['habitat'] = request.json.get('habitat', pokemon['habitat'])

    return jsonify(pokemon), 200

@app.route('/pokemons/<int:id>', methods=['DELETE'])
def delete_pokemon(id):
    global pokemons
    pokemon = next((poke for poke in pokemons if poke['id'] == id), None)
    if not pokemon:
        abort(404, description="Pokémon no encontrado")
    
    pokemons = [poke for poke in pokemons if poke['id'] != id]
    return jsonify({'mensaje': 'Pokémon eliminado'}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': str(error)}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error)}), 400

if __name__ == '__main__':
    app.run(debug=True)

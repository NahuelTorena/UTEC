from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/character', methods=['POST'])
def get_character():
    data = request.get_json()

    if 'character_id' not in data:
        return jsonify({"error": "Character not found"}), 400

    character_id = data['character_id']
    url = f"https://rickandmortyapi.com/api/character/{character_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        
        character_data = response.json()
        return jsonify({
            "name": character_data['name'],
            "status": character_data['status']
        }), 200

    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            return jsonify({"error": "Character not found"}), 404
        return jsonify({"error": "Failed to fetch character data", "details": str(err)}), response.status_code

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

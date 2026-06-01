import requests
import json

# 1. Extract (Extracción)
def extract_pokemon_data(pokemon_name): 
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}" 
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: No se pudo encontrar a {pokemon_name}")
        return None

# 2. Transform (Transformación) - AQUÍ FILTRAMOS LOS DATOS
def transform_pokemon_data(pokemon_data):
    if not pokemon_data:
        return None
    
    # Solo tomamos los campos que pediste
    transformed = {
          "name": pokemon_data["name"],
          "height": pokemon_data["height"],
          "weight": pokemon_data["weight"],
          # Extraemos el primer tipo de la lista
          "type": pokemon_data["types"][0]["type"]["name"],
          "moves_keys":list(pokemon_data["moves"][0].keys()),
          "moves_count":len(pokemon_data["moves"]),
          # Extraemos la URL de la imagen oficial
          "image": pokemon_data["sprites"]["other"]["official-artwork"]["front_default"],
          "moves_keys": list(pokemon_data["moves"][0].keys()) if pokemon_data["moves"] else [],
          "moves_count": len(pokemon_data["moves"]),
          "moves_cl": [move["move"]["name"] for move in pokemon_data["moves"]]
     }
    return transformed

# 3. Load (Carga) - AQUÍ GUARDAMOS EL JSON
def load_pokemon_data(pokemon_data):
    if pokemon_data:
        # Usamos el nombre del pokemon para el nombre del archivo
        pokemon_name = pokemon_data["name"]
        filename = f"{pokemon_name}.json"
        
        with open(filename, 'w') as file:
            json.dump(pokemon_data, file, indent=4)
        print(f"¡Éxito! El archivo {filename} ha sido guardado con los datos transformados.")

# --- EJECUCIÓN PARA DRATINI ---
pokemons=["lapras","dratini","kyogre","corviknight"]

for poke in pokemons:
    raw_data = extract_pokemon_data(poke)
    clean_data = transform_pokemon_data(raw_data)
# Paso 2: Transformar los datos (solo name, height, weight)
    load_pokemon_data(clean_data)

# Paso 3: Guardar el resultado en el archivo dratini.json

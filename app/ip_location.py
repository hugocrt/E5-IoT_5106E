import requests
import folium
import os


def get_location():
    try:
        response = requests.get(f"https://ipinfo.io/")
        data = response.json()
        return {
            'latitude': float(data['loc'].split(',')[0]),
            'longitude': float(data['loc'].split(',')[1]),
            'city': data['city'],
            'postal': data['postal'],
            'country': data['country'],
            'region': data['region'],
            'timezone': data['timezone'],
            'ip_address': data['ip']
        }

    except Exception as e:
        print(f"Error retrieving position: {e}")
        return None


def generate_map(latitude, longitude):
    # Créer un objet carte centré sur les coordonnées latitude et longitude

    my_map = folium.Map(
        location=[latitude, longitude],
        zoom_start=7,
        tiles='cartodb positron',
        max_zoom=18,
        min_zoom=5,
        min_lat=33,
        max_lat=55,
        min_lon=-20,
        max_lon=24,
        max_bounds=True
    )

    # Ajouter un marqueur pour indiquer la position
    folium.Marker([latitude, longitude], popup="You are here!").add_to(my_map)

    # Chemin relatif vers le dossier 'static/maps' dans 'app/static'
    map_folder = os.path.join("app", "static", "maps")
    map_path = os.path.join(map_folder, "my_location_map.html")

    # Vérifier si le dossier 'app/static/maps' existe, sinon le créer
    if not os.path.exists(map_folder):
        os.makedirs(map_folder)

    # Sauvegarder la carte dans le fichier HTML
    my_map.save(map_path)

    # Retourner le chemin relatif pour l'utiliser dans le template
    return os.path.join("static", "maps", "my_location_map.html")

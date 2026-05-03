import os
import folium
from folium.plugins import MarkerCluster

BASE_DIR = os.path.dirname(__file__)
MAPS_DIR = os.path.join(BASE_DIR, 'static', 'maps')
os.makedirs(MAPS_DIR, exist_ok=True)

DEFAULT_LAT = 17.6805
DEFAULT_LNG = 75.9064

def generate_shelter_map(shelters: list, disaster_type: str = 'general') -> str:
    if not shelters:
        return None

    color_map = {
        'flood': 'blue', 'fire': 'red',
        'earthquake': 'purple', 'general': 'green', 'medical': 'orange',
    }
    marker_color = color_map.get(disaster_type, 'green')
    center_lat = shelters[0].get('lat', DEFAULT_LAT)
    center_lng = shelters[0].get('lng', DEFAULT_LNG)

    m = folium.Map(location=[center_lat, center_lng], zoom_start=13, tiles='OpenStreetMap')
    cluster = MarkerCluster().add_to(m)

    for shelter in shelters:
        lat = shelter.get('lat')
        lng = shelter.get('lng')
        name = shelter.get('name', 'Shelter')
        addr = shelter.get('address', '')
        cap = shelter.get('capacity', 'Unknown')
        if lat and lng:
            folium.Marker(
                location=[lat, lng],
                popup=folium.Popup(f"<b>{name}</b><br>{addr}<br>Capacity: {cap}", max_width=200),
                tooltip=name,
                icon=folium.Icon(color=marker_color, icon='home', prefix='fa')
            ).add_to(cluster)

    folium.CircleMarker(
        location=[center_lat, center_lng],
        radius=10, color='red', fill=True,
        fill_color='red', fill_opacity=0.6,
        tooltip='You are here (approx)'
    ).add_to(m)

    filename = f'map_{disaster_type}.html'
    output_path = os.path.join(MAPS_DIR, filename)
    m.save(output_path)
    return output_path

def generate_evacuation_map(shelters: list, disaster_type: str,
                             user_lat: float = DEFAULT_LAT,
                             user_lng: float = DEFAULT_LNG) -> str:
    m = folium.Map(location=[user_lat, user_lng], zoom_start=13, tiles='OpenStreetMap')

    folium.Marker(
        location=[user_lat, user_lng],
        tooltip='Your location',
        icon=folium.Icon(color='red', icon='user', prefix='fa')
    ).add_to(m)

    for shelter in shelters:
        s_lat = shelter.get('lat')
        s_lng = shelter.get('lng')
        name = shelter.get('name', 'Shelter')
        if s_lat and s_lng:
            folium.PolyLine(
                locations=[[user_lat, user_lng], [s_lat, s_lng]],
                color='blue', weight=2.5, opacity=0.7,
                tooltip=f'Route to {name}'
            ).add_to(m)
            folium.Marker(
                location=[s_lat, s_lng],
                tooltip=name,
                popup=folium.Popup(f"<b>{name}</b><br>{shelter.get('address', '')}", max_width=200),
                icon=folium.Icon(color='green', icon='home', prefix='fa')
            ).add_to(m)

    filename = f'evac_map_{disaster_type}.html'
    output_path = os.path.join(MAPS_DIR, filename)
    m.save(output_path)
    return output_path

def get_map_path(disaster_type: str = 'general') -> str:
    filename = f'map_{disaster_type}.html'
    path = os.path.join(MAPS_DIR, filename)
    return path if os.path.exists(path) else None
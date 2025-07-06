"""Distance Server using FastMCP"""
import os
import json
import httpx
from mcp.server.fastmcp import FastMCP
import geopy.distance
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Instructions for the FastMCP server
INSTRUCTIONS = """Find the cab distance of a location:
1. Find latitude and longitude of for both source and destination location.
2. Calculate the distance between the two coordinates.
"""
mcp = FastMCP(name='weather', instructions=INSTRUCTIONS, port=8001, host='0.0.0.0')

@mcp.tool(description="Get latitude and longitude from the given location")
def get_geolocation_lat_long(location: str) -> str:
    """Get the latitude and longitude of a given location."""
    api_key = os.getenv('GEOLOCATION_API_KEY')
    if not api_key:
        raise ValueError("Geolocation API key is not set in the environment variable.")
    response = httpx.get('https://geocode.maps.co/search',
                            params={'q': location, 'api_key': api_key},
                            timeout=10)
    if response.status_code != 200:
        raise ValueError(f"Error fetching geolocation data: {response.status_code}")
    data = response.json()
    if not data:
        raise ValueError("No geolocation data found for the given location.")
    lat = data[0]['lat']
    lon = data[0]['lon']
    display_name = data[0].get('display_name', 'Unknown Location')
    return json.dumps({
        'latitude': lat,
        'longitude': lon,
        'display_name': display_name
    })

@mcp.tool(description="Get distance between two coordinates")
def calculation_distance_by_coordinates(source_latitude: float, source_longitude: float, 
                    destination_latitude: float, destination_longitude: float) -> str:
    """Calculate the distance between two coordinates."""
    if not all([source_latitude, source_longitude, destination_latitude, destination_longitude]):
        raise ValueError("All latitude and longitude values must be provided.")
    source_coords = (source_latitude, source_longitude)
    destination_coords = (destination_latitude, destination_longitude)
    # Calculate the distance in kilometers
    distance = geopy.distance.geodesic(source_coords, destination_coords).km
    return json.dumps({
        'distance_km': distance,
        'source_coordinates': source_coords,
        'destination_coordinates': destination_coords
    })

@mcp.tool(description="Get location from latitude and longitude")
def get_location_from_coordinates(latitude: float, longitude: float) -> str:
    """Get the location name from latitude and longitude."""
    api_key = os.getenv('GEOLOCATION_API_KEY')
    if not api_key:
        raise ValueError("Geolocation API key is not set in the environment variable.")
    response = httpx.get('https://geocode.maps.co/reverse',
                            params={'lat': latitude, 'lon': longitude, 'api_key': api_key},
                            timeout=10)
    if response.status_code != 200:
        raise ValueError(f"Error fetching location data: {response.status_code}")
    data = response.json()
    if not data:
        raise ValueError("No location data found for the given coordinates.")
    return json.dumps(data)

def main():
    """Run the FastMCP server."""
    mcp.run(transport="sse")

if __name__ == '__main__':
    main()

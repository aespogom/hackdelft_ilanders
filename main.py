import googlemaps
from datetime import datetime

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "The file was not found."
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
api_key_file = 'secret.txt'  # Replace with your actual file path
api_key = read_file(api_key_file)

def get_walking_distance(api_key, origin, destination):
    # Initialize the client with the API key
    gmaps = googlemaps.Client(key=api_key)
    
    # Request directions via walking
    directions_result = gmaps.directions(origin,
                                         destination,
                                         mode="bicycling",
                                         departure_time=datetime.now())
    
    # Extract the distance
    if directions_result:
        distance = directions_result[0]['legs'][0]['distance']['text']
        duration = directions_result[0]['legs'][0]['duration']['text']
        return distance, duration
    else:
        return None, None

# Example usage
origin = "1600 Amphitheatre Parkway, Mountain View, CA"
destination = "1 Infinite Loop, Cupertino, CA"

distance, duration = get_walking_distance(api_key, origin, destination)
if distance and duration:
    print(f"Walking distance: {distance}")
    print(f"Walking duration: {duration}")
else:
    print("Could not find walking distance.")


from flask import Flask, render_template, request, jsonify
import googlemaps
from main import API_KEY, final_result  # Import the API key

app = Flask(__name__)
gmaps = googlemaps.Client(key=API_KEY)  # Use the imported API key

@app.route('/')
def index():
    return render_template('index.html', api_key=API_KEY)

@app.route('/get_directions', methods=['GET'])
def get_directions():
    routes = final_result()
    google_routes = []
    for route in routes:
        mode = route[0]
        origin = route[1][0]
        destination = route[1][-1]
        waypoints = []
        waypoints= [{
            "location": r,
            "stopover": True
        } for r in route[1][1:-1]]
        google_routes.append({
            "origin": origin,
            "destination": destination,
            "waypoints": waypoints,
            "method": mode.upper()
        })
        # directions_result = gmaps.directions(origin,
        #                                     destination,
        #                                     waypoints=waypoints,
        #                                     mode=mode,
        #                                     departure_time="now")
        # return jsonify({
        #             origin: origin,
        #             destination: destination,
        #             waypoints: waypoints
        #         })
    return jsonify(google_routes)

if __name__ == '__main__':
    app.run(debug=True)

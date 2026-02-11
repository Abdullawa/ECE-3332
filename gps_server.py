from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
data = {
    "latitude": 0,
    "longitude": 0,
    "timestamp": "00:00:00"
}

@app.route('/')
def home():
    return "Hello from GPS Server!"

@app.route('/map')
def map_page():
    return render_template('map.html')

@app.route('/api/position', methods=['GET'])
def receive_position():
    global data
    try:
        with open(r'C:\ECE-3332\GPSdata.txt', 'r') as file:
                    lines  = file.readlines()
                    if lines :
                        last_line = lines[-1]
                        parts = last_line.strip().split(',')
                        if len(parts) == 3:
                            timestamp, latitude, longitude = parts
                            data = {
                                "timestamp": timestamp,
                                "latitude": float(latitude),
                                "longitude": float(longitude)
                            }
                            
    except Exception as e:
                print(f"Error loading GPS data from file: {e}")
                return []
    return jsonify(data), 200

@app.route('/api/history', methods=['GET'])
def get_history():
    coordinates = []
    try:
        with open(r'C:\ECE-3332\GPSdata.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    timestamp, latitude, longitude = parts
                    coordinates.append({
                        'timestamp': timestamp,
                        'latitude': float(latitude),
                        'longitude': float(longitude)
                    })
    except Exception as e:
        print(f"Error loading GPS history: {e}")
    
    return jsonify(coordinates), 200


if __name__ == '__main__':
    app.run(debug=True)


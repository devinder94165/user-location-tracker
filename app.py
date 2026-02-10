from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os 

app = Flask(__name__)

# Database connection
def get_db():
    conn = sqlite3.connect("locations.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL,
            longitude REAL,
            time TEXT
        )
    """)
    return conn

# Home Page
@app.route("/")
def index():
    return render_template("index.html")

# Save Location
@app.route("/location", methods=["POST"])
def save_location():
    data = request.get_json()
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude is None or longitude is None:
        return jsonify({"error": "Invalid data"}), 400

    conn = get_db()
    conn.execute(
        "INSERT INTO locations (latitude, longitude, time) VALUES (?, ?, ?)",
        (latitude, longitude, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Location saved successfully"})

# API to fetch locations
@app.route("/api/locations")
def api_locations():
    conn = sqlite3.connect("locations.db")
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM locations").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# View template
@app.route("/view")
def view_locations():
    return render_template("view.html")

@app.route("/map")
def map_view():
    return render_template("map.html")
'''
@app.route("/view")
def view_locations():
    conn = sqlite3.connect("locations.db")
    conn.row_factory = sqlite3.Row
    data = conn.execute("SELECT * FROM locations").fetchall()
    conn.close()

    return """
    <h2>Stored User Locations</h2>
    <table border="1" cellpadding="8">
        <tr>
            <th>ID</th>
            <th>Latitude</th>
            <th>Longitude</th>
            <th>Time</th>
        </tr>
        """ + "".join([
            f"<tr><td>{row['id']}</td><td>{row['latitude']}</td><td>{row['longitude']}</td><td>{row['time']}</td></tr>"
            for row in data
        ]) + "</table>"
'''
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
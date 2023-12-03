from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime, timedelta


app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temperature_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a model for temperature data
class TemperatureModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    building = db.Column(db.String(50), nullable=False)
    room = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create the database tables
db.create_all()

@app.route('/api/data', methods=['POST'])
def add_data():
    try:
        # Get data from the request
        data = request.json['data']

        # Create a new data record
        new_data = TemperatureModel(data=data)

        # Add the record to the database
        db.session.add(new_data)
        db.session.commit()

        return jsonify({'message': 'Data added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Generate some example temperature data

@app.route('/api/generate_example_data', methods=['GET'])
def generate_example_data():
    example_data = [
        {'building': 'A', 'room': '101', 'temperature': 22.5},
        {'building': 'A', 'room': '102', 'temperature': 23.0},
        # Add more example data as needed
    ]

    for data in example_data:
        new_data = TemperatureModel(building=data['building'], room=data['room'], temperature=data['temperature'])
        db.session.add(new_data)

    db.session.commit()

# Uncomment the line below to generate example data
# generate_example_data()

@app.route('/api/average_temperature', methods=['GET'])
def get_average_temperature():
    try:
        # Get building and room from the query parameters
        building = request.args.get('building')
        room = request.args.get('room')

        # Calculate the timestamp for 15 minutes ago
        fifteen_minutes_ago = datetime.utcnow() - timedelta(minutes=15)

        # Query temperature data for the specified building and room in the last 15 minutes
        query_result = TemperatureModel.query.filter_by(building=building, room=room).filter(
            TemperatureModel.timestamp >= fifteen_minutes_ago).all()

        if not query_result:
            return jsonify({'message': 'No data available for the specified building and room in the last 15 minutes'})

        # Calculate the average temperature
        total_temperature = sum(record.temperature for record in query_result)
        average_temperature = total_temperature / len(query_result)

        return jsonify({'average_temperature': average_temperature}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

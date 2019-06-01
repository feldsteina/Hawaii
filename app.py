from flask import Flask, Response, jsonify, request, render_template

import json

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Begin SQLite setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite",
                       connect_args={"check_same_thread": False})

Base = automap_base()

Base.prepare(engine, reflect=True)

Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

# Begin Flask routes
app = Flask(__name__)


@app.route("/")
def index():
    message = 'Route info:\
    Daily Precipitation Data: /api/v1.0/precipitation\n\
    Station Data: /api/v1.0/stations\n\
    Total Observations: /api/v1.0/tobs\n\
    Data starting on <date> /api/v1.0/<start>\n\
    Data between two dates: /api/v1.0/2010-01-01/<start>/<end>\n\
    Date format should be YYYY-MM-DD'
    return render_template("index.html", message=message)


@app.route("/api/v1.0/precipitation", methods=["GET"])
def precipitation():
    queryResults = session.query(
        Measurement.date, func.sum(Measurement.prcp))\
        .group_by(Measurement.date).order_by(Measurement.date)

    precipData = []

    for result in queryResults:
        precipData.append({
            "date": result[0],
            "prcp": result[1]
        })

    return jsonify(precipData)


@app.route("/api/v1.0/stations", methods=["GET"])
def stations():
    queryResults = session.query(Station.station, Station.name)

    stationData = []

    for result in queryResults:
        stationData.append({
            "station": result[0],
            "name": result[1]
        })

    return jsonify(stationData)


if __name__ == "__main__":
    app.run()

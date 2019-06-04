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
    Daily Precipitation Data: <a href="/api/v1.0/precipitation">\
        /api/v1.0/precipitation\
    </a><br>\
    Station Data: <a href="/api/v1.0/stations">\
        /api/v1.0/stations\
    </a><br >\
    Temperature Data: <a href="/api/v1.0/tobs">\
        /api/v1.0/tobs\
    </a><br>\
    Data starting on a date: <a href="/api/v1.0/2010-01-01">\
        /api/v1.0/&lt;start&gt;\
    </a><br>\
    Data between two dates: <a href="/api/v1.0/2010-01-01/2017-08-23">\
        /api/v1.0/&lt;start&gt;/&lt;end&gt;\
    </a><br>\
    Date format should be YYYY-MM-DD'
    return message


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


@app.route("/api/v1.0/tobs", methods=["GET"])
def tobs():
    queryResults = session.query(Measurement.date)\
        .order_by(Measurement.date.desc()).limit(1)

    data = queryResults[0][0]

    newYear = data.split("-")

    oldYear = []

    oldYear.append(str(int(newYear[0])-1))
    oldYear.append(newYear[1])
    oldYear.append(newYear[2])

    newYear = "-".join(newYear)

    print(newYear)

    oldYear = "-".join(oldYear)

    print(oldYear)

    queryResults = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.date <= newYear)\
        .filter(Measurement.date > oldYear)\
        .order_by(Measurement.date)\
        .group_by(Measurement.date)

    tobsData = []

    for items in queryResults:
        tobsData.append(items)

    return jsonify(tobsData)

if __name__ == "__main__":
    app.run()

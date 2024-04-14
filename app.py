# Import the dependencies.

import numpy as np
import json
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify, Response



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measure = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)
current_date = session.query(Measure.date).order_by(Measure.date.desc()).first()[0]
prev_year = dt.datetime.strftime(dt.datetime.strptime(current_date,'%Y-%m-%d') - dt.timedelta(days = 365),'%Y-%m-%d')

session.close()
#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Climate App API!<br>"
        f"Use this API if you dare...<br/>"
        f"Here are the available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list """
    # Query all precipitation score
    results = session.query(Measure.date, Measure.prcp).all()

    session.close()

# Create a dictionary from the row data and append to a list 
    all_prcp = []
    for result in results:
        prcp_dict = {}
        prcp_dict["date"] = result[0]
        prcp_dict["prcp"] = result[1]
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations """
    # Query all stations
    results = session.query(func.count(Station.id)).all()

    session.close()

    # Create a list of all_stations
    all_stations = []
    for result in results:
        st_dict = {}
        st_dict["station"] = result[0]
        all_stations.append(st_dict)
        
        return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations """
    # Query all dates and temperature observations of the most active station for the last year of data
    results = session.query(Measure.date, Measure.tobs).filter(Measure.station == 'USC00519281').filter(Measure.date >= prev_year).all()

    session.close()

    # Create a list of all_stations
    active_station = []
    for result in results:
        active_dict = {}
        active_dict["date"] = result[0]
        active_dict["tobs"] = result[1]
        active_station.append(active_dict)
        
        return jsonify(active_station)

@app.route("/api/v1.0/start")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of agg data"""
    # Query TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
    results = session.query(func.min(Measure.tobs), func.max(Measure.tobs),func.avg(Measure.tobs)).filter(Measure.station  == 'USC00519281').all()

    session.close()

    # Create a list of min, max, and avg
    agg_data = []
    for result in results:
        agg_dict = {}
        agg_dict["TMIN"] = result[0]
        agg_dict["TMAX"] = result[1]
        agg_dict["TAVG"] = result[2]
        agg_data.append(agg_dict)
        
        return jsonify(agg_data)

@app.route("/api/v1.0/start/end")
def start_end():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    today = dt.datetime(2016, 8, 23)
    """Return a list of agg data"""
    # Query TMIN, TAVG, and TMAX for all dates between dates
    results = session.query(func.min(Measure.tobs), func.max(Measure.tobs), func.avg(Measure.tobs)).filter(Measure.date >= prev_year).filter(Measure.date <= today).all()

    session.close()

    # Create a list of min, max, and avg
    agg_data = []
    for result in results:
        agg_dict = {}
        agg_dict["TMIN"] = result[0]
        agg_dict["TMAX"] = result[1]
        agg_dict["TAVG"] = result[2]
        agg_data.append(agg_dict)
        
        return jsonify(agg_data)

if __name__ == '__main__':
    app.run(debug=True)   












































        
















        
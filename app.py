import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measure = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
       

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Returns a list of temperatures from 8-24-16 thru 8-24-17"""
    # Query all dates and precipitaion from one year of data
    precip = session.query(Measure.date, Measure.prcp).\
    filter(Measure.date > '2016-08-23').\
    order_by(Measure.date).all() 

    # Create a dictionary from the row data and append to a list precipitaion
    precip_dates = []
    for stuff in precip:
        precip_dic = {}
        precip_dic["date"] = stuff.date
        precip_dic["precipitation"] = stuff.prcp
        precip_dates.append(precip_dic)

    return jsonify(precip_dates)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all the station names"""
    # Query all stations
    station_names = session.query(Station.station).all()

    # Convert list of tuples into normal list
    #stations_list = list(np.ravel(station_names)

    return jsonify(station_names)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a json list of Temperature Observations (tobs) for the previous year"""
    # Query all stations
    tobs = session.query(Measure.station, Measure.date, Measure.tobs).order_by(Measure.date).\
    filter(Measure.date > '2016-08-23').all()

    #Convert #list of tuples into normal list
    #tobs_list = list(np.ravel(tobs))

    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    """Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

    When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

    When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive."""
    
    
    # Query temperature given a start date
    return jsonify (calc_temp_start(start))
def calc_temp_start(start_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
    
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measure.tobs), func.avg(Measure.tobs), func.max(Measure.tobs)).\
    filter(Measure.date >= start_date).all()


    #Convert #list of tuples into normal list
    #tobs_list = list(np.ravel(tobs))

   










if __name__ == '__main__':
    app.run(debug=True)


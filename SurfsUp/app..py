# Dependencies
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
hawaii_measurement = Base.classes.measurement
Station = Base.classes.station

# Create an app
app = Flask(__name__)


def date_prev_year():
    # Create the session
    session = Session(engine)

    
    
    recent_date = session.query(func.max(hawaii_measurement.date)).first()[0]
    first_date = dt.datetime.strptime(recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Close the session                   
    session.close()

   
    return(first_date)


@app.route("/")
def homepage():
    return """ <h1> Hello! Welcome to Honolulu, Hawaii Climate API! </h1>
    <h3> The available routes are: </h3>
    <ul>
    <li><a href = "/api/v1.0/precipitation"> Precipitation</a>: <strong>/api/v1.0/precipitation</strong> </li>
    <li><a href = "/api/v1.0/stations"> Stations </a>: <strong>/api/v1.0/stations</strong></li>
    <li><a href = "/api/v1.0/tobs"> TOBS </a>: <strong>/api/v1.0/tobs</strong></li>
    <li>To retrieve the minimum, average, and maximum temperatures for a specific start date, use <strong>/api/v1.0/&ltstart&gt</strong> (replace start date in yyyy-mm-dd format)</li>
    <li>To retrieve the minimum, average, and maximum temperatures for a specific start-end range, use <strong>/api/v1.0/&ltstart&gt/&ltend&gt</strong> (replace start and end date in yyyy-mm-dd format)</li>
    </ul>
    """


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create the session
    session = Session(engine)

   
    prcp_data = session.query(hawaii_measurement.date, hawaii_measurement.prcp).filter(hawaii_measurement.date >= date_prev_year()).all()
    
    # Close the session                   
    #session.close()
    #prcp = []
    #for date, prcp in prcp_data:
       # prcp_data = {}
        #prcp_data["date"] = date
        #prcp_data["prcp"] = prcp
        #prcp.append(prcp_data)

    precip_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip_results = session.query(hawaii_measurement.date, hawaii_measurement.prcp).filter(hawaii_measurement.date >= precip_year).all()
    precip = {date: prcp for date, prcp in precip_results}
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    # Create the session
    session = Session(engine)

   
    station_1 = session.query(Station.station).all()
    session.close()
    station_2 = list(np.ravel(station_1))
    return jsonify(station_2)
@app.route("/api/v1.0/tobs")
def tobs():
   
    session = Session(engine)

    
    tobs_data = session.query(hawaii_measurement.date, hawaii_measurement.tobs).filter(hawaii_measurement.station == 'USC00519281').\
                        filter(hawaii_measurement.date >= date_prev_year()).all()

    # Close the session                   
    session.close()

   
    list_dict = []
    for date, tobs in tobs_data:
        tob = {}
        tob["date"] = date
        tob["tobs"] = tobs
        list_dict.append(tob)

    # previous 12 months (JSON)
    return jsonify(list_dict)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def cal_temp(start=None, end=None):
    # Create the session
    session = Session(engine)
    
    #( minimum,  average and maximum temperature)
    min_max_avg=[func.min(hawaii_measurement.tobs), func.avg(hawaii_measurement.tobs), func.max(hawaii_measurement.tobs)]
    
    # Check for an end date
    if end == None: 
       
        recent_date = session.query(*min_max_avg).\
                            filter(hawaii_measurement.date >= start).all()
        
        recent_date = list(np.ravel(recent_date))

       
        return jsonify(recent_date)
    else:
        
        start_to_end_date = session.query(*min_max_avg).\
                            filter(hawaii_measurement.date >= start).\
                            filter(hawaii_measurement.date <= end).all()
        
        start_to_end_date = list(np.ravel(start_to_end_date))

      
        return jsonify()

    # Close the session                   
    Session.close()
    
# Define main branch 
if __name__ == "__main__":
    app.run(debug = True)

# Import the dependencies.

import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB

#session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """ Available API Routes."""
    return(
    
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"

        f"_______________________<br/>"
        f"Precipitation Data for last 12 months (2016-08-24 to 2017-08-23):<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"_______________________<br/>"

        f"List of Stations in the dataset:<br/>"
        f"/api/v1.0/stations<br/>"

        f"_______________________<br/>"
        
        f"Date and Temperature observations of the most-active station (USC00519281) for previous year:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"_______________________<br/>"
        
        f"Minimum, Maximum and Average temperature from a given start date to end of dataset:<br/>"
        f"Please enter Start Date in the format: YYYY-MM-DD<br/>"
        f"This api have the data for the date range 2010-01-01 to 2017-08-23<br/>"
        f"/api/v1.0/<start><br/>"
        f"_______________________<br/>"
        
        f"Minimum, Maximum and average temperature from a given start date to a given end date:<br/>"
        f"Please enter Start Date and End Date in the format: YYYY-MM-DD/YYYY-MM-DD<br/>"
        f"This api have the data for the date range 2010-01-01 to 2017-08-23<br/>"
        f"/api/v1.0/<start>/<end>"
        
        
    )
    

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Retrieve last 12 months of data"""
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Calculate the date one year from the last date in data set.
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Perform a query to retrieve the data and precipitation scores
    data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date <= '2017-08-23').\
        filter(Measurement.date >= query_date).\
        order_by(Measurement.date).all()

    # Close the session
    session.close()

    # Create a dictionary using date as the key and prcp as the value
    precipitation_dict = {}
    for date, prcp in data:
        precipitation_dict[date] = prcp
 
 # Return the JSON representation of dictionary.
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
    
def stations():    
    """Get a list of stations"""
      
    
    # Create our session (link) from Python to the DB  
    session = Session(engine)       
 
    # Perform a query to retrieve the station data
    stations_list = session.query(Station.station,Station.name).all()
    
    # Close the session
    session.close()

    #create a list to store stations info 
    station_list = []
    for station, name in stations_list:
        station_info = {'station': station,
                         'name': name}
        station_list.append(station_info) 
 
 # Return a JSON list of stations from the dataset.
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")

def tobs(): 
    """Get temperature data for the most active station for last year"""
# Create our session (link) from Python to the DB
    session = Session(engine)    

# Perform a query to get the dates and temperature observations of the most-active station
# for the previous year of data
    temp = session.query(Measurement.station,Measurement.tobs,Measurement.date).\
    filter(Measurement.date <= '2017-08-23').\
    filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.station == 'USC00519281').all()
 
# Close the session
    session.close()

# Create a list of dictionary containing dates and temperatures observations 
    tobs_list = []
    for station,tobs,date in temp:
        tobs_dict = {'station': station,
                     'tobs': tobs,
                       'date':date }
        tobs_list.append(tobs_dict) 

# Return a JSON list of temperature data of previous year for the most active station (USC00519281)
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
    """Get min, max and average temperature data from start date"""
    session = Session(engine)    
   
    
    # Perform a query to get TMIN, TAVG, and TMAX for all the dates from start date to
    # end date inclusive, taken as parameters from the URL
    
    temp_date = session.query(Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()
    
    # Close the session
    session.close()
     
     # Create a list of dictionary to store date, min, max and avg temperature values
    tobs_date = []
    
    for date,mintemp,maxtemp,avgtemp in temp_date:
            tobs_dict1 = {'Date':date,
                    'MinTemp': mintemp,
                    'MaxTemp': maxtemp,
                    'AvgTemp':avgtemp }
            tobs_date.append(tobs_dict1) 
        
     # Return a JSON list of the minimum temperature, the average temperature, and the
    # maximum temperature calculated from the given start date to the end of the dataset
    return jsonify(tobs_date)
    

# route for Start and End date

@app.route("/api/v1.0/<start>/<end>")

def start_end(start, end):
    """Get min, max and average temperature data from start date and end date"""
    # Create our session (link) from Python to the DB
    session = Session(engine)    
  
  # Perform a query to get TMIN, TAVG, and TMAX for all the dates from start date to
  # end date inclusive, taken as parameters from the URL
    
    temp_start_end = session.query(Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()
    
    # Close the session
    session.close()
     # Create a list of dictionary to store date, min, max and avg temperature values
    tobs_date_list = []
    
    for date1,mintemp1,maxtemp1,avgtemp1 in temp_start_end:
        tobs_dict2 = {'Date':date1,
                    'MinTemp': mintemp1,
                    'MaxTemp': maxtemp1,
                    'AvgTemp':avgtemp1 }
        tobs_date_list.append(tobs_dict2) 
    
    # Return a JSON list of the minimum temperature, the average temperature, and the
    # maximum temperature calculated from the given start date to the given end date    
    return jsonify(tobs_date_list) 


    
#################################################

if __name__ == '__main__':
    app.run(debug=True) 
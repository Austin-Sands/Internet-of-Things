#!/usr/bin/env python
import datetime
import time
import gpiozero
import mysql.connector

from w1thermsensor import W1ThermSensor

#####################################
# Mysql database connection and setup
gardenpidb = mysql.connector.connect(
    host="localhost",
    user="austin-sands",
    password="gardenpi_6551",
    database="gardenpidb",
)

curr_date = datetime.datetime.now()
formatted_date = curr_date.strftime('%Y-%m-%d %H:%M')

dbcursor = gardenpidb.cursor()

#temp sensor variables
temp_sensor = W1ThermSensor()

def get_temp():
    current_temp = temp_sensor.get_temperature()
    current_temp = (current_temp * 9 / 5) + 32

    #sql statement to pass data to proper DB table
    sql_statement = "INSERT INTO temp_data (date_time, reading, manual_read) VALUES (%s, %s, %s)"
    inputs = (formatted_date, current_temp, 1)

    dbcursor.execute(sql_statement, inputs)

    return current_temp

def main():

    get_temp()

    #commit modifications to database and close cursor and connection
    gardenpidb.commit()
    dbcursor.close()
    gardenpidb.close()


if __name__ == "__main__":
    main()
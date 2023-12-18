#!/usr/bin/env python
import datetime
import time
import gpiozero
import mysql.connector

from smbus import SMBus

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

#light resistor variables
bus = SMBus(1)
adc = 0x4b
ldr = 0x84

def get_light():
    bus.write_byte(adc, ldr)
    result = bus.read_byte(adc)

    #sql statement to pass data to proper DB table
    sql_statement = "INSERT INTO light_data (date_time, reading, manual_read) VALUES (%s, %s, %s)"
    inputs = (formatted_date, result, 1)

    dbcursor.execute(sql_statement, inputs)

    return result

def main():
    get_light()

    #commit modifications to database and close cursor and connection
    gardenpidb.commit()
    dbcursor.close()
    gardenpidb.close()


if __name__ == "__main__":
    main()
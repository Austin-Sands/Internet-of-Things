#!/usr/bin/env python
import datetime
import gpiozero
import time
import mysql.connector

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

#time variable
watering_time = 5

#relay variables
# relay2 is pump, relay3 is solenoid valve
relay_pin2 = 20
relay2 = gpiozero.OutputDevice(relay_pin2, active_high=False)
relay_pin3 = 21
relay3 = gpiozero.OutputDevice(relay_pin3, active_high=False)

def give_water():
    #turn on solenoid valve relay
    relay3.on()
    #turn on pump relay to send power to pump
    relay2.on()
    time.sleep(watering_time)
    #turn off relays
    relay2.off()
    relay3.off()

    #sql statement to pass data to proper DB table
    sql_statement = "INSERT INTO watering_log (date_time, manual_call) VALUES (%s, %s)"
    inputs = (formatted_date, 1)

    dbcursor.execute(sql_statement, inputs)

def main():
    give_water()

    #commit modifications to database and close cursor and connection
    gardenpidb.commit()
    dbcursor.close()
    gardenpidb.close()

if __name__ == "__main__":
    main()
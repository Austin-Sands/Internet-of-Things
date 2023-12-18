DROP TABLE IF EXISTS temp_data;
CREATE TABLE temp_data(
    EntryID int NOT NULL AUTO_INCREMENT,
    date_time datetime,
    reading float,
    manual_read boolean,
    PRIMARY KEY (EntryID)
);

DROP TABLE IF EXISTS light_data;
CREATE TABLE light_data(
    EntryID int NOT NULL AUTO_INCREMENT,
    date_time datetime,
    reading float,
    manual_read boolean,
    PRIMARY KEY (EntryID)
);

DROP TABLE IF EXISTS moisture_data;
CREATE TABLE moisture_data(
    EntryID int NOT NULL AUTO_INCREMENT,
    date_time datetime,
    reading float,
    manual_read boolean,
    PRIMARY KEY (EntryID)
);

DROP TABLE IF EXISTS watering_log;
CREATE TABLE watering_log(
    EntryID int NOT NULL AUTO_INCREMENT,
    date_time datetime,
    manual_call boolean,
    PRIMARY KEY (EntryID)
);

COMMIT;
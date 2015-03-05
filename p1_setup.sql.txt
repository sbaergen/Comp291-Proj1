/*
 *  This file is used to create the database schema for Assignment 2
 *  CMPUT291, Winter Term, 2015.
 *  It is the same as the one for Assignment 2, except some comments are added.
 * 
 *  Author: Li-Yan Yuan
 *  University of Alberta
 *  
 */
DROP TABLE owner;
DROP TABLE auto_sale;
DROP TABLE restriction;
DROP TABLE driving_condition;
DROP TABLE ticket;
DROP TABLE ticket_type;
DROP TABLE vehicle;
DROP TABLE vehicle_type;
DROP TABLE drive_licence;
DROP TABLE people;

/*
 *  Table containing all the info for each person
 */
CREATE TABLE  people (
  sin           CHAR(15),  
  name          VARCHAR(40),
  height        number(5,2),
  weight        number(5,2),
  eyecolor      VARCHAR (10),
  haircolor     VARCHAR(10),
  addr          VARCHAR2(50),
  gender        CHAR,
  birthday      DATE,
  PRIMARY KEY (sin),
  CHECK ( gender IN ('m', 'f') )
);

/*
 *  Table containing drive_licence info
 */
CREATE TABLE drive_licence (
  licence_no      CHAR(15),
  sin             char(15),
  class           VARCHAR(10),
  photo           BLOB,
  issuing_date    DATE,
  expiring_date   DATE,
  PRIMARY KEY (licence_no),
  UNIQUE (sin),
  FOREIGN KEY (sin) REFERENCES people
        ON DELETE CASCADE
);

/*
 *  The driving conditions
 */
CREATE TABLE driving_condition (
  c_id        INTEGER,
  description VARCHAR(1024),
  PRIMARY KEY (c_id)
);

/*
 *   to indicate the driving conditions for each drive licence
 */
CREATE TABLE restriction(
  licence_no   CHAR(15),
  r_id         INTEGER,
  PRIMARY KEY (licence_no, r_id),
  FOREIGN KEY (licence_no) REFERENCES drive_licence,
  FOREIGN KEY (r_id) REFERENCES driving_condition
);

/*
 *  to store all the typles of vehicles
 */
CREATE TABLE vehicle_type (
  type_id       integer,
  type          CHAR(10),
  PRIMARY KEY (type_id)
);

/*
 *   Vehicle information
 */
CREATE TABLE vehicle (
  serial_no    CHAR(15),
  maker        VARCHAR(20),	
  model        VARCHAR(20),
  year         number(4,0),
  color        VARCHAR(10),
  type_id      integer,
  PRIMARY KEY (serial_no),
  FOREIGN KEY (type_id) REFERENCES vehicle_type
);

/*
 *   The ownership of each vehicle
 */
CREATE TABLE owner (
  owner_id          CHAR(15),
  vehicle_id        CHAR(15),
  is_primary_owner  CHAR(1),
  PRIMARY KEY (owner_id, vehicle_id),
  FOREIGN KEY (owner_id) REFERENCES people,
  FOREIGN KEY (vehicle_id) REFERENCES vehicle,
  CHECK ( is_primary_owner IN ('y', 'n'))
);

/*
 *  To record auto sales
 */
CREATE TABLE auto_sale (
  transaction_id  int,
  seller_id   CHAR(15),
  buyer_id    CHAR(15),
  vehicle_id  CHAR(15),
  s_date      date,
  price       numeric(9,2),
  PRIMARY KEY (transaction_id),
  FOREIGN KEY (seller_id) REFERENCES people,
  FOREIGN KEY (buyer_id) REFERENCES people,
  FOREIGN KEY (vehicle_id) REFERENCES vehicle
);

/*
 *  all the ticket types
 */
CREATE TABLE ticket_type (
  vtype     CHAR(10),
  fine      number(5,2),
  PRIMARY KEY (vtype)
);

/*
 *  Ticket records
 */
CREATE TABLE ticket (
  ticket_no     int,
  violator_no   CHAR(15),  
  vehicle_id    CHAR(15),
  office_no     CHAR(15),
  vtype        char(10),
  vdate        date,
  place        varchar(20),
  descriptions varchar(1024),
  PRIMARY KEY (ticket_no),
  FOREIGN KEY (vtype) REFERENCES ticket_type,
  FOREIGN KEY (violator_no) REFERENCES people ON DELETE CASCADE,
  FOREIGN KEY (vehicle_id)  REFERENCES vehicle,
  FOREIGN KEY (office_no) REFERENCES people ON DELETE CASCADE
);


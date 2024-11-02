CREATE TABLE "city" (
	"ID" INTEGER PRIMARY KEY AUTOINCREMENT,
	"Name" CHARACTER(35) NOT NULL DEFAULT '' ,
	"CountryCode" CHARACTER(3) NOT NULL DEFAULT '' ,
	"District" CHARACTER(20) NOT NULL DEFAULT '' ,
	"Population" INTEGER NOT NULL DEFAULT '0',
	FOREIGN KEY("CountryCode") REFERENCES "country" ("Code") ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE "country" (
	"Code" CHARACTER(3) NOT NULL DEFAULT '' ,
	"Name" CHARACTER(52) NOT NULL DEFAULT '' ,
	"Continent" TEXT NOT NULL DEFAULT 'Asia' ,
	"Region" CHARACTER(26) NOT NULL DEFAULT '' ,
	"SurfaceArea" DECIMAL NOT NULL DEFAULT '0.00' ,
	"IndepYear" SMALLINT NULL  ,
	"Population" INTEGER NOT NULL DEFAULT '0' ,
	"LifeExpectancy" DECIMAL NULL  ,
	"GNP" DECIMAL NULL  ,
	"GNPOld" DECIMAL NULL  ,
	"LocalName" CHARACTER(45) NOT NULL DEFAULT '' ,
	"GovernmentForm" CHARACTER(45) NOT NULL DEFAULT '' ,
	"HeadOfState" CHARACTER(60) NULL  ,
	"Capital" INTEGER NULL  ,
	"Code2" CHARACTER(2) NOT NULL DEFAULT '' ,
	PRIMARY KEY ("Code")
);
CREATE TABLE "countrylanguage" (
	"CountryCode" CHARACTER(3) NOT NULL DEFAULT '' ,
	"Language" CHARACTER(30) NOT NULL DEFAULT '' ,
	"IsOfficial" TEXT NOT NULL DEFAULT 'F' ,
	"Percentage" DECIMAL NOT NULL DEFAULT '0.0' ,
	PRIMARY KEY ("CountryCode", "Language"),
	FOREIGN KEY("CountryCode") REFERENCES "country" ("Code") ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE "airline" (
	"airline_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"iata" CHARACTER(2) NOT NULL  ,
	"airlinename" VARCHAR(30) NULL  ,
	"base_airport" SMALLINT NOT NULL,
	FOREIGN KEY("base_airport") REFERENCES "airport" ("airport_id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE "airplane" (
	"airplane_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"capacity" MEDIUMINT NOT NULL  ,
	"type_id" INTEGER NOT NULL  ,
	"airline_id" INTEGER NOT NULL,
	FOREIGN KEY("type_id") REFERENCES "airplane_type" ("type_id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE "airplane_type" (
	"type_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"identifier" VARCHAR(50) NULL  ,
	"description" TEXT NULL
);
CREATE TABLE "airport" (
	"airport_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"iata" CHARACTER(3) NULL  ,
	"icao" CHARACTER(4) NOT NULL  ,
	"name" VARCHAR(50) NOT NULL
);
CREATE TABLE "airport_geo" (
	"airport_id" SMALLINT NOT NULL  ,
	"name" VARCHAR(50) NOT NULL  ,
	"city" VARCHAR(50) NULL  ,
	"country" VARCHAR(50) NULL  ,
	"latitude" DECIMAL NOT NULL  ,
	"longitude" DECIMAL NOT NULL  ,
	"geolocation" TEXT NOT NULL  ,
	PRIMARY KEY ("airport_id"),
	FOREIGN KEY("airport_id") REFERENCES "airport" ("airport_id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE "airport_reachable" (
	"airport_id" SMALLINT NOT NULL  ,
	"hops" INTEGER NULL  ,
	PRIMARY KEY ("airport_id"),
	FOREIGN KEY("airport_id") REFERENCES "airport" ("airport_id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE "booking" (
	"booking_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"flight_id" INTEGER NOT NULL  ,
	"seat" CHARACTER(4) NULL  ,
	"passenger_id" INTEGER NOT NULL  ,
	"price" DECIMAL NOT NULL,
	FOREIGN KEY("flight_id") REFERENCES "flight" ("flight_id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY("passenger_id") REFERENCES "passenger" ("passenger_id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE "employee" (
	"employee_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"firstname" VARCHAR(100) NOT NULL  ,
	"lastname" VARCHAR(100) NOT NULL  ,
	"birthdate" DATE NOT NULL  ,
	"sex" CHARACTER(1) NULL  ,
	"street" VARCHAR(100) NOT NULL  ,
	"city" VARCHAR(100) NOT NULL  ,
	"zip" SMALLINT NOT NULL  ,
	"country" VARCHAR(100) NOT NULL  ,
	"emailaddress" VARCHAR(120) NULL  ,
	"telephoneno" VARCHAR(30) NULL  ,
	"salary" DECIMAL NULL  ,
	"department" TEXT NULL  ,
	"username" VARCHAR(20) NULL  ,
	"password" CHARACTER(32) NULL
);
CREATE TABLE "flight" (
	"flight_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"flightno" CHARACTER(8) NOT NULL  ,
	"from" SMALLINT NOT NULL  ,
	"to" SMALLINT NOT NULL  ,
	"departure" DATETIME NOT NULL  ,
	"arrival" DATETIME NOT NULL  ,
	"airline_id" SMALLINT NOT NULL  ,
	"airplane_id" INTEGER NOT NULL,
	FOREIGN KEY("from") REFERENCES "airport" ("airport_id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY("to") REFERENCES "airport" ("airport_id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY("airline_id") REFERENCES "airline" ("airline_id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY("airplane_id") REFERENCES "airplane" ("airplane_id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY("flightno") REFERENCES "flightschedule" ("flightno") ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE "flight_log" (
	"flight_log_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"log_date" DATETIME NOT NULL  ,
	"user" VARCHAR(100) NOT NULL  ,
	"flight_id" INTEGER NOT NULL  ,
	"flightno_old" CHARACTER(8) NOT NULL  ,
	"flightno_new" CHARACTER(8) NOT NULL  ,
	"from_old" SMALLINT NOT NULL  ,
	"to_old" SMALLINT NOT NULL  ,
	"from_new" SMALLINT NOT NULL  ,
	"to_new" SMALLINT NOT NULL  ,
	"departure_old" DATETIME NOT NULL  ,
	"arrival_old" DATETIME NOT NULL  ,
	"departure_new" DATETIME NOT NULL  ,
	"arrival_new" DATETIME NOT NULL  ,
	"airplane_id_old" INTEGER NOT NULL  ,
	"airplane_id_new" INTEGER NOT NULL  ,
	"airline_id_old" SMALLINT NOT NULL  ,
	"airline_id_new" SMALLINT NOT NULL  ,
	"comment" VARCHAR(200) NULL,
	FOREIGN KEY("flight_id") REFERENCES "flight" ("flight_id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE "flightschedule" (
	"flightno" CHARACTER(8) NOT NULL  ,
	"from" SMALLINT NOT NULL  ,
	"to" SMALLINT NOT NULL  ,
	"departure" TIME NOT NULL  ,
	"arrival" TIME NOT NULL  ,
	"airline_id" SMALLINT NOT NULL  ,
	"monday" TINYINT NULL DEFAULT '0' ,
	"tuesday" TINYINT NULL DEFAULT '0' ,
	"wednesday" TINYINT NULL DEFAULT '0' ,
	"thursday" TINYINT NULL DEFAULT '0' ,
	"friday" TINYINT NULL DEFAULT '0' ,
	"saturday" TINYINT NULL DEFAULT '0' ,
	"sunday" TINYINT NULL DEFAULT '0' ,
	PRIMARY KEY ("flightno"),
	FOREIGN KEY("from") REFERENCES "airport" ("airport_id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY("to") REFERENCES "airport" ("airport_id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY("airline_id") REFERENCES "airline" ("airline_id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE "passenger" (
	"passenger_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"passportno" CHARACTER(9) NOT NULL  ,
	"firstname" VARCHAR(100) NOT NULL  ,
	"lastname" VARCHAR(100) NOT NULL
);
CREATE TABLE "passengerdetails" (
	"passenger_id" INTEGER NOT NULL  ,
	"birthdate" DATE NOT NULL  ,
	"sex" CHARACTER(1) NULL  ,
	"street" VARCHAR(100) NOT NULL  ,
	"city" VARCHAR(100) NOT NULL  ,
	"zip" SMALLINT NOT NULL  ,
	"country" VARCHAR(100) NOT NULL  ,
	"emailaddress" VARCHAR(120) NULL  ,
	"telephoneno" VARCHAR(30) NULL  ,
	PRIMARY KEY ("passenger_id"),
	FOREIGN KEY("passenger_id") REFERENCES "passenger" ("passenger_id") ON UPDATE NO ACTION ON DELETE CASCADE
);
CREATE TABLE "weatherdata" (
	"log_date" DATE NOT NULL  ,
	"time" TIME NOT NULL  ,
	"station" INTEGER NOT NULL  ,
	"temp" DECIMAL NOT NULL  ,
	"humidity" DECIMAL NOT NULL  ,
	"airpressure" DECIMAL NOT NULL  ,
	"wind" DECIMAL NOT NULL  ,
	"weather" TEXT NULL  ,
	"winddirection" SMALLINT NOT NULL  ,
	PRIMARY KEY ("log_date", "time", "station")
);

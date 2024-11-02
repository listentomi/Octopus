CREATE TABLE "borders" (
	"Country1" VARCHAR(4) NOT NULL DEFAULT '' ,
	"Country2" VARCHAR(4) NOT NULL DEFAULT '' ,
	"Length" VARCHAR(35) NULL  ,
	PRIMARY KEY ("Country1", "Country2"),
	FOREIGN KEY("Country1") REFERENCES "country" ("Code") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("Country2") REFERENCES "country" ("Code") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "capt_country" (
	"Country" VARCHAR(4) NOT NULL  ,
	"Capital" VARCHAR(64) NOT NULL  ,
	PRIMARY KEY ("Country", "Capital"),
	FOREIGN KEY("Capital") REFERENCES "city" ("City_id") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("Country") REFERENCES "country" ("Code") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "capt_prov" (
	"Province" VARCHAR(64) NOT NULL  ,
	"Capital" VARCHAR(64) NOT NULL  ,
	PRIMARY KEY ("Province", "Capital"),
	FOREIGN KEY("Capital") REFERENCES "city" ("City_id") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("Province") REFERENCES "province" ("Prov_id") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "city" (
	"City_id" VARCHAR(64) NOT NULL DEFAULT '' ,
	"Population" INTEGER NULL  ,
	"Longitude" FLOAT NULL  ,
	"Latitude" FLOAT NULL  ,
	PRIMARY KEY ("City_id")
);
CREATE TABLE "cityinprov" (
	"City" VARCHAR(64) NOT NULL  ,
	"Province" VARCHAR(64) NOT NULL  ,
	PRIMARY KEY ("City", "Province"),
	FOREIGN KEY("City") REFERENCES "city" ("City_id") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("Province") REFERENCES "province" ("Prov_id") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "continent" (
	"Name" VARCHAR(20) NOT NULL DEFAULT '' ,
	"Area" VARCHAR(35) NULL  ,
	PRIMARY KEY ("Name")
);
CREATE TABLE "country" (
	"Code" VARCHAR(4) NOT NULL DEFAULT '' ,
	"Area" VARCHAR(35) NULL  ,
	"Population" VARCHAR(35) NULL  ,
	PRIMARY KEY ("Code")
);
CREATE TABLE "countryofprov" (
	"Province" VARCHAR(64) NOT NULL  ,
	"Country" VARCHAR(4) NOT NULL  ,
	PRIMARY KEY ("Province", "Country"),
	FOREIGN KEY("Country") REFERENCES "country" ("Code") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("Province") REFERENCES "province" ("Prov_id") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "encompasses" (
	"Country" VARCHAR(4) NOT NULL  ,
	"Continent" VARCHAR(20) NOT NULL  ,
	"Percentage" VARCHAR(35) NULL  ,
	PRIMARY KEY ("Continent", "Country"),
	FOREIGN KEY("Continent") REFERENCES "continent" ("Name") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("Country") REFERENCES "country" ("Code") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "province" (
	"Prov_id" VARCHAR(64) NOT NULL DEFAULT '' ,
	"Population" VARCHAR(35) NULL  ,
	"Area" VARCHAR(35) NULL  ,
	PRIMARY KEY ("Prov_id")
);

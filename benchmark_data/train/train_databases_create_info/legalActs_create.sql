CREATE TABLE "legalact_link" (
	"actId1" INTEGER NOT NULL  ,
	"actId2" INTEGER NOT NULL  ,
	PRIMARY KEY ("actId1", "actId2"),
	FOREIGN KEY("actId1") REFERENCES "legalacts" ("id") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("actId2") REFERENCES "legalacts" ("id") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "legalact_people" (
	"peopleId" INTEGER NOT NULL  ,
	"actId" INTEGER NOT NULL  ,
	PRIMARY KEY ("peopleId", "actId"),
	FOREIGN KEY("peopleId") REFERENCES "people" ("personId") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("actId") REFERENCES "legalacts" ("id") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "legalacts" (
	"id" INTEGER NOT NULL  ,
	"hash" CHARACTER(32) NOT NULL  ,
	"update" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ,
	"Court" VARCHAR(100) NULL  ,
	"CaseKind" VARCHAR(50) NULL  ,
	"CaseNumber" SMALLINT NULL  ,
	"ActYear" SMALLINT NULL  ,
	"Judge" VARCHAR(255) NULL  ,
	"ActKind" VARCHAR(20) NULL  ,
	"ActNumber" SMALLINT NULL  ,
	"StartDate" DATE NULL  ,
	"LegalDate" DATE NULL  ,
	"Status" VARCHAR(20) NULL  ,
	"ActLink" TINYINT NOT NULL DEFAULT '0' ,
	"MotiveDate" DATE NULL  ,
	"MotiveLink" TINYINT NOT NULL DEFAULT '0' ,
	"HighCourt" VARCHAR(100) NULL  ,
	"OutNumber" SMALLINT NULL  ,
	"YearHigherCourt" SMALLINT NULL  ,
	"TypeOfDocument" VARCHAR(100) NULL  ,
	"SendDate" DATE NULL  ,
	"ResultOfAppeal" VARCHAR(100) NULL  ,
	PRIMARY KEY ("id")
);
CREATE TABLE "people" (
	"personId" INTEGER PRIMARY KEY AUTOINCREMENT,
	"name" VARCHAR(255) NOT NULL  ,
	"jury" TINYINT NOT NULL DEFAULT '0' ,
	"court" VARCHAR(100) NULL
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE "scrapefix" (
	"actId" INTEGER NOT NULL  ,
	"fix_description" TEXT NOT NULL  ,
	"contributor" VARCHAR(50) NULL  ,
	PRIMARY KEY ("actId"),
	FOREIGN KEY("actId") REFERENCES "legalacts" ("id") ON UPDATE CASCADE ON DELETE CASCADE
);

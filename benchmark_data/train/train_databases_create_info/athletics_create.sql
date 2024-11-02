CREATE TABLE "athletics-at-the-2004-summer-olympics" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "Freebase ID" VARCHAR(255),
  "sport" VARCHAR(255),
  "part of" VARCHAR(255),
  "instance of" VARCHAR(255),
  "follows" VARCHAR(255),
  "number of participants" VARCHAR(255),
  "location" VARCHAR(255),
  "followed by" VARCHAR(255),
  "point in time" VARCHAR(255),
  "winner" VARCHAR(255),
  "organizer" VARCHAR(255),
  "start time" VARCHAR(255),
  "end time" VARCHAR(255),
  "competition class" VARCHAR(255),
  "Olympedia event ID" VARCHAR(255),
  FOREIGN KEY ("competition class") REFERENCES "competition-class" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY ("followed by") REFERENCES "followed-by" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY ("follows") REFERENCES "follows" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY ("winner") REFERENCES "winner" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT
);
CREATE TABLE "competition-class" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "instance of" VARCHAR(255),
  "sport" VARCHAR(255),
  "competition class" VARCHAR(255)
);
CREATE TABLE "place-of-birth" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "located in the administrative territorial entity" VARCHAR(255),
  "Commons category" VARCHAR(255),
  "country" VARCHAR(255),
  "image" VARCHAR(255),
  "coordinate location" VARCHAR(255),
  "topic's main category" VARCHAR(255),
  "instance of" VARCHAR(255),
  "Freebase ID" VARCHAR(255),
  "population" VARCHAR(255),
  "GeoNames ID" VARCHAR(255),
  "area" VARCHAR(255),
  "Who's on First ID" VARCHAR(255),
  FOREIGN KEY ("located in the administrative territorial entity") REFERENCES "administrative-territorial-entity" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT
);
CREATE TABLE "winner" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "sex or gender" VARCHAR(255),
  "country of citizenship" VARCHAR(255),
  "place of birth" VARCHAR(255),
  "date of birth" VARCHAR(255),
  "instance of" VARCHAR(255),
  "occupation" VARCHAR(255),
  "Freebase ID" VARCHAR(255),
  "World Athletics athlete ID" VARCHAR(255),
  "Sports-Reference.com Olympic athlete ID (archived)" VARCHAR(255),
  "sport" VARCHAR(255),
  "participant in" VARCHAR(255),
  "given name" VARCHAR(255),
  "mass" VARCHAR(255),
  "height" VARCHAR(255),
  "Olympedia people ID" VARCHAR(255),
  "Munzinger Sport number" VARCHAR(255),
  "Olympic.org athlete ID (archived)" VARCHAR(255),
  "Olympics.com athlete ID" VARCHAR(255)
);
CREATE TABLE "twin-town" (
  "label" TEXT(255),
  "description" TEXT(255),
  "postal code" TEXT(255),
  "twinned administrative body" TEXT(255),
  "Dewey Decimal Classification" TEXT(255),
  "country" TEXT(255),
  "Commons category" TEXT(255),
  "coordinate location" TEXT(255),
  "located in the administrative territorial entity" TEXT(255),
  "GND ID" TEXT(255),
  "instance of" TEXT(255),
  "Freebase ID" TEXT(255),
  "coat of arms image" TEXT(255),
  "topic's main category" TEXT(255),
  "MusicBrainz area ID" TEXT(255),
  "local dialing code" TEXT(255),
  "population" TEXT(255),
  "official website" TEXT(255),
  "GeoNames ID" TEXT(255),
  "image" TEXT(255),
  "category of associated people" TEXT(255),
  "elevation above sea level" TEXT(255),
  "located in time zone" TEXT(255),
  "Quora topic ID" TEXT(255),
  "area" TEXT(255),
  "Encyclopædia Britannica Online ID" TEXT(255),
  "VIAF ID" TEXT(255),
  "Library of Congress authority ID" TEXT(255),
  "NKCR AUT ID" TEXT(255),
  "Who's on First ID" TEXT(255),
  "WorldCat Identities ID" TEXT(255),
  "native label" TEXT(255),
  "official name" TEXT(255),
  "page banner" TEXT(255),
  "flag image" TEXT(255),
  "National Library of Israel J9U ID" TEXT(255),
  "Online PWN Encyclopedia ID" TEXT(255)
);
CREATE TABLE "administrative-territorial-entity" (
  "label" TEXT(255),
  "description" TEXT(255),
  "instance of" TEXT(255),
  "located in the administrative territorial entity" TEXT(255),
  "population" TEXT(255),
  "country" TEXT(255),
  "Freebase ID" TEXT(255),
  "GeoNames ID" TEXT(255),
  "area" TEXT(255),
  "locator map image" TEXT(255),
  "coordinate location" TEXT(255),
  "capital" TEXT(255)
);
CREATE TABLE "capital-city" (
  "label" TEXT(255),
  "description" TEXT(255),
  "twinned administrative body" TEXT(255),
  "Commons category" TEXT(255),
  "located in the administrative territorial entity" TEXT(255),
  "instance of" TEXT(255),
  "Freebase ID" TEXT(255),
  "country" TEXT(255),
  "population" TEXT(255),
  "image" TEXT(255),
  "GeoNames ID" TEXT(255),
  "GND ID" TEXT(255),
  "coordinate location" TEXT(255),
  "capital of" TEXT(255),
  "VIAF ID" TEXT(255),
  "topic's main category" TEXT(255),
  "category of associated people" TEXT(255),
  "elevation above sea level" TEXT(255),
  "area" TEXT(255),
  "Library of Congress authority ID" TEXT(255),
  "Who's on First ID" TEXT(255),
  "National Library of Israel J9U ID" TEXT(255),
  "located in time zone" TEXT(255)
);
CREATE TABLE "followed-by" (
  "label" TEXT(255),
  "description" TEXT(255),
  "Freebase ID" TEXT(255),
  "sport" TEXT(255),
  "part of" TEXT(255),
  "instance of" TEXT(255),
  "country" TEXT(255),
  "follows" TEXT(255),
  "number of participants" TEXT(255),
  "location" TEXT(255),
  "competition class" TEXT(255),
  "point in time" TEXT(255),
  "followed by" TEXT(255),
  "organizer" TEXT(255),
  "winner" TEXT(255),
  "Olympedia event ID" TEXT(255)
);
CREATE TABLE "follows" (
  "label" TEXT(255),
  "description" TEXT(255),
  "Freebase ID" TEXT(255),
  "sport" TEXT(255),
  "part of" TEXT(255),
  "instance of" TEXT(255),
  "follows" TEXT(255),
  "location" TEXT(255),
  "country" TEXT(255),
  "point in time" TEXT(255),
  "followed by" TEXT(255),
  "winner" TEXT(255),
  "organizer" TEXT(255),
  "start time" TEXT(255),
  "end time" TEXT(255),
  "competition class" TEXT(255),
  "number of participants" TEXT(255),
  "Olympedia event ID" TEXT(255)
);

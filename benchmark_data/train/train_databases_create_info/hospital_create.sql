CREATE TABLE "coat-of-arms" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "country" VARCHAR(255),
  "image" VARCHAR(255),
  "applies to jurisdiction" VARCHAR(255),
  "depicts" VARCHAR(255),
  "significant event" VARCHAR(255),
  "instance of" VARCHAR(255),
  FOREIGN KEY ("applies to jurisdiction") REFERENCES "jurisdiction" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT
);
CREATE TABLE "general-hospital" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "country" VARCHAR(255),
  "coordinate location" VARCHAR(255),
  "instance of" VARCHAR(255),
  "located in the administrative territorial entity" VARCHAR(255),
  "location" VARCHAR(255),
  "official website" VARCHAR(255),
  "street address" VARCHAR(255),
  "postal code" VARCHAR(255),
  "part of" VARCHAR(255),
  "emergency services" VARCHAR(255),
  "has facility" VARCHAR(255),
  "partnership with" VARCHAR(255),
  FOREIGN KEY ("partnership with") REFERENCES "partnership-with" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY ("part of") REFERENCES "part" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY ("located in the administrative territorial entity") REFERENCES "administrative-territorial-entity" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY ("location") REFERENCES "physical-location" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT
);
CREATE TABLE "jurisdiction" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "topic's main category" VARCHAR(255),
  "CBS municipality code" VARCHAR(255),
  "flag image" VARCHAR(255),
  "coat of arms image" VARCHAR(255),
  "locator map image" VARCHAR(255),
  "postal code" VARCHAR(255),
  "country" VARCHAR(255),
  "coordinate location" VARCHAR(255),
  "instance of" VARCHAR(255),
  "Freebase ID" VARCHAR(255),
  "Commons category" VARCHAR(255),
  "GeoNames ID" VARCHAR(255),
  "shares border with" VARCHAR(255),
  "contains settlement" VARCHAR(255),
  "image" VARCHAR(255),
  "official website" VARCHAR(255),
  "population" VARCHAR(255),
  "number of households" VARCHAR(255),
  "coat of arms" VARCHAR(255),
  "located in time zone" VARCHAR(255),
  "area" VARCHAR(255),
  "elevation above sea level" VARCHAR(255),
  "Amsterdam code" VARCHAR(255),
  "located in the administrative territorial entity" VARCHAR(255),
  "category for maps" VARCHAR(255),
  "iNaturalist place ID" VARCHAR(255),
  "RKD thesaurus ID" VARCHAR(255),
  "KvK company ID" VARCHAR(255),
  "flag" VARCHAR(255)
);
CREATE TABLE "part" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "InterPro ID" VARCHAR(255),
  "instance of" VARCHAR(255)
);
CREATE TABLE "partnership-with" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "country" VARCHAR(255),
  "located in the administrative territorial entity" VARCHAR(255),
  "instance of" VARCHAR(255),
  "official website" VARCHAR(255),
  "location" VARCHAR(255),
  "partnership with" VARCHAR(255),
  "coordinate location" VARCHAR(255),
  FOREIGN KEY ("located in the administrative territorial entity") REFERENCES "administrative-territorial-entity" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT
);
CREATE TABLE "physical-location" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "country" VARCHAR(255),
  "instance of" VARCHAR(255),
  "coordinate location" VARCHAR(255),
  "located in the administrative territorial entity" VARCHAR(255),
  "BAG residence ID" VARCHAR(255),
  "GeoNames ID" VARCHAR(255),
  "Who's on First ID" VARCHAR(255),
  "RKD thesaurus ID" VARCHAR(255),
  FOREIGN KEY ("located in the administrative territorial entity") REFERENCES "administrative-territorial-entity" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT
);
CREATE TABLE "administrative-territorial-entity" (
  "label" TEXT(255),
  "description" TEXT(255),
  "Commons category" TEXT(255),
  "country" TEXT(255),
  "coordinate location" TEXT(255),
  "flag image" TEXT(255),
  "instance of" TEXT(255),
  "located in time zone" TEXT(255),
  "CBS municipality code" TEXT(255),
  "Amsterdam code" TEXT(255),
  "located in the administrative territorial entity" TEXT(255),
  "population" TEXT(255),
  "iNaturalist place ID" TEXT(255),
  "capital" TEXT(255),
  "postal code" TEXT(255),
  "shares border with" TEXT(255),
  "contains settlement" TEXT(255),
  "coat of arms image" TEXT(255),
  "locator map image" TEXT(255),
  "number of households" TEXT(255),
  "image" TEXT(255),
  "official website" TEXT(255),
  "GeoNames ID" TEXT(255),
  "MusicBrainz area ID" TEXT(255),
  "flag" TEXT(255),
  "topic's main category" TEXT(255),
  "area" TEXT(255),
  "VIAF ID" TEXT(255),
  "RKD thesaurus ID" TEXT(255),
  "KvK company ID" TEXT(255),
  "Freebase ID" TEXT(255)
);
CREATE TABLE "human-settlement" (
  "label" TEXT(255),
  "description" TEXT(255),
  "country" TEXT(255),
  "instance of" TEXT(255),
  "located in the administrative territorial entity" TEXT(255),
  "coordinate location" TEXT(255)
);
CREATE TABLE "political-border" (
  "label" TEXT(255),
  "description" TEXT(255),
  "topic's main category" TEXT(255),
  "CBS municipality code" TEXT(255),
  "flag image" TEXT(255),
  "coat of arms image" TEXT(255),
  "locator map image" TEXT(255),
  "postal code" TEXT(255),
  "country" TEXT(255),
  "coordinate location" TEXT(255),
  "instance of" TEXT(255),
  "Freebase ID" TEXT(255),
  "Commons category" TEXT(255),
  "GeoNames ID" TEXT(255),
  "shares border with" TEXT(255),
  "contains settlement" TEXT(255),
  "image" TEXT(255),
  "official website" TEXT(255),
  "population" TEXT(255),
  "number of households" TEXT(255),
  "coat of arms" TEXT(255),
  "located in time zone" TEXT(255),
  "area" TEXT(255),
  "elevation above sea level" TEXT(255),
  "Amsterdam code" TEXT(255),
  "located in the administrative territorial entity" TEXT(255),
  "category for maps" TEXT(255),
  "iNaturalist place ID" TEXT(255),
  "RKD thesaurus ID" TEXT(255),
  "KvK company ID" TEXT(255),
  "flag" TEXT(255)
);

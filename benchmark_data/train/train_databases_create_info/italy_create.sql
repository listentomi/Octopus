CREATE TABLE "administrative-centre" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "instance of" VARCHAR(255),
  "country" VARCHAR(255),
  "Commons category" VARCHAR(255),
  "locator map image" VARCHAR(255),
  "located in the administrative territorial entity" VARCHAR(255),
  "coordinate location" VARCHAR(255),
  "capital" VARCHAR(255),
  "Freebase ID" VARCHAR(255)
);
CREATE TABLE "office-held-by-head-of-government" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "instance of" VARCHAR(255),
  "subclass of" VARCHAR(255),
  "applies to jurisdiction" VARCHAR(255),
  "country" VARCHAR(255),
  "officeholder" VARCHAR(255)
);
CREATE TABLE "place-of-death" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "instance of" VARCHAR(255),
  "category combines topics" VARCHAR(255),
  "category contains" VARCHAR(255)
);
CREATE TABLE "province-of-italy" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "instance of" VARCHAR(255),
  "country" VARCHAR(255),
  "capital" VARCHAR(255),
  "shares border with" VARCHAR(255),
  "located in the administrative territorial entity" VARCHAR(255),
  "Commons category" VARCHAR(255),
  "licence plate code" VARCHAR(255),
  "ISO 3166-2 code" VARCHAR(255),
  "coordinate location" VARCHAR(255),
  "locator map image" VARCHAR(255),
  "located in time zone" VARCHAR(255),
  "topic's main category" VARCHAR(255),
  "Freebase ID" VARCHAR(255),
  "GeoNames ID" VARCHAR(255),
  "postal code" VARCHAR(255),
  "image" VARCHAR(255),
  "area" VARCHAR(255),
  "ISTAT ID" VARCHAR(255),
  "official website" VARCHAR(255),
  "OpenStreetMap relation ID" VARCHAR(255),
  "HASC" VARCHAR(255),
  "geoshape" VARCHAR(255),
  "office held by head of government" VARCHAR(255),
  "topic's main template" VARCHAR(255),
  "EU Knowledge Graph item ID" VARCHAR(255),
  FOREIGN KEY ("shares border with") REFERENCES "political-border" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY ("located in the administrative territorial entity") REFERENCES "administrative-territorial-entity" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY ("office held by head of government") REFERENCES "office-held-by-head-of-government" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY ("capital") REFERENCES "capital-city" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT
);
CREATE TABLE "source-of-information" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "instance of" VARCHAR(255),
  "language of work or name" VARCHAR(255)
);
CREATE TABLE "administrative-territorial-entity" (
  "label" TEXT(255),
  "description" TEXT(255),
  "Dewey Decimal Classification" TEXT(255),
  "country" TEXT(255),
  "shares border with" TEXT(255),
  "capital" TEXT(255),
  "contains the administrative territorial entity" TEXT(255),
  "instance of" TEXT(255),
  "Commons category" TEXT(255),
  "flag image" TEXT(255),
  "coat of arms image" TEXT(255),
  "ISO 3166-2 code" TEXT(255),
  "located in the administrative territorial entity" TEXT(255),
  "coordinate location" TEXT(255),
  "locator map image" TEXT(255),
  "located in time zone" TEXT(255),
  "GND ID" TEXT(255),
  "VIAF ID" TEXT(255),
  "Library of Congress authority ID" TEXT(255),
  "topic's main category" TEXT(255),
  "page banner" TEXT(255),
  "Curlie ID" TEXT(255),
  "Freebase ID" TEXT(255),
  "FIPS 10-4 (countries and regions)" TEXT(255),
  "category for people born here" TEXT(255),
  "category for people who died here" TEXT(255),
  "GeoNames ID" TEXT(255),
  "category for films shot at this location" TEXT(255),
  "category of associated people" TEXT(255),
  "MusicBrainz area ID" TEXT(255),
  "NUTS code" TEXT(255),
  "head of government" TEXT(255),
  "Commons gallery" TEXT(255),
  "geography of topic" TEXT(255),
  "official website" TEXT(255),
  "elevation above sea level" TEXT(255),
  "image" TEXT(255),
  "ISNI" TEXT(255),
  "topic's main Wikimedia portal" TEXT(255),
  "area" TEXT(255),
  "OpenStreetMap relation ID" TEXT(255),
  "GACS ID" TEXT(255),
  "demonym" TEXT(255),
  "Encyclopædia Universalis ID" TEXT(255),
  "office held by head of government" TEXT(255),
  "legislative body" TEXT(255),
  "executive body" TEXT(255),
  "Gran Enciclopèdia Catalana ID" TEXT(255),
  "Store norske leksikon ID" TEXT(255),
  "ISTAT ID" TEXT(255),
  "Getty Thesaurus of Geographic Names ID" TEXT(255),
  "Bibliothèque nationale de France ID" TEXT(255),
  "archINFORM location ID" TEXT(255),
  "NKCR AUT ID" TEXT(255),
  "Encyclopædia Britannica Online ID" TEXT(255),
  "native label" TEXT(255),
  "population" TEXT(255),
  "Treccani's Dizionario di Storia ID" TEXT(255),
  "category for maps" TEXT(255),
  "French Vikidia ID" TEXT(255),
  "WorldCat Identities ID" TEXT(255),
  "HASC" TEXT(255),
  "Interlingual Index ID" TEXT(255),
  "economy of topic" TEXT(255),
  "category for the view of the item" TEXT(255),
  "WordNet 3.1 Synset ID" TEXT(255),
  "iNaturalist place ID" TEXT(255),
  "Schoenberg Database of Manuscripts place ID" TEXT(255),
  "Colon Classification" TEXT(255),
  "National Library of Israel J9U ID" TEXT(255),
  "Catalan Vikidia ID" TEXT(255),
  "Online PWN Encyclopedia ID" TEXT(255),
  "Den Store Danske ID" TEXT(255),
  "geoshape" TEXT(255),
  "EU Knowledge Graph item ID" TEXT(255),
  "museum-digital place ID" TEXT(255)
);
CREATE TABLE "capital-city" (
  "label" TEXT(255),
  "description" TEXT(255),
  "Dewey Decimal Classification" TEXT(255),
  "Commons category" TEXT(255),
  "located in the administrative territorial entity" TEXT(255),
  "postal code" TEXT(255),
  "shares border with" TEXT(255),
  "ISTAT ID" TEXT(255),
  "coordinate location" TEXT(255),
  "country" TEXT(255),
  "local dialing code" TEXT(255),
  "Italian cadastre code (municipality)" TEXT(255),
  "topic's main category" TEXT(255),
  "official website" TEXT(255),
  "instance of" TEXT(255),
  "Freebase ID" TEXT(255),
  "GND ID" TEXT(255),
  "MusicBrainz area ID" TEXT(255),
  "twinned administrative body" TEXT(255),
  "category for people who died here" TEXT(255),
  "GeoNames ID" TEXT(255),
  "category of associated people" TEXT(255),
  "image" TEXT(255),
  "capital of" TEXT(255),
  "VIAF ID" TEXT(255),
  "elevation above sea level" TEXT(255),
  "Commons gallery" TEXT(255),
  "licence plate code" TEXT(255),
  "coordinates of northernmost point" TEXT(255),
  "coordinates of southernmost point" TEXT(255),
  "coordinates of easternmost point" TEXT(255),
  "coordinates of westernmost point" TEXT(255),
  "OpenStreetMap relation ID" TEXT(255),
  "UN/LOCODE" TEXT(255),
  "Quora topic ID" TEXT(255),
  "population" TEXT(255),
  "area" TEXT(255),
  "archINFORM location ID" TEXT(255),
  "Encyclopædia Britannica Online ID" TEXT(255),
  "Library of Congress authority ID" TEXT(255),
  "IndicePA ID" TEXT(255),
  "Gran Enciclopèdia Catalana ID" TEXT(255),
  "Who's on First ID" TEXT(255),
  "locator map image" TEXT(255),
  "NKCR AUT ID" TEXT(255),
  "WorldCat Identities ID" TEXT(255),
  "Wiki Loves Monuments ID" TEXT(255),
  "located in time zone" TEXT(255),
  "described by source" TEXT(255),
  "Colon Classification" TEXT(255),
  "National Library of Israel J9U ID" TEXT(255),
  "page banner" TEXT(255),
  "coat of arms image" TEXT(255),
  "SBN place ID" TEXT(255),
  "patron saint" TEXT(255),
  "seismic classification" TEXT(255),
  "EU Knowledge Graph item ID" TEXT(255),
  "Online PWN Encyclopedia ID" TEXT(255)
);
CREATE TABLE "twin-town" (
  "label" TEXT(255),
  "description" TEXT(255),
  "twinned administrative body" TEXT(255),
  "Dewey Decimal Classification" TEXT(255),
  "country" TEXT(255),
  "Commons category" TEXT(255),
  "located in the administrative territorial entity" TEXT(255),
  "coordinate location" TEXT(255),
  "instance of" TEXT(255),
  "page banner" TEXT(255),
  "topic's main category" TEXT(255),
  "MusicBrainz area ID" TEXT(255),
  "official website" TEXT(255),
  "Freebase ID" TEXT(255),
  "GeoNames ID" TEXT(255),
  "GND ID" TEXT(255),
  "category of associated people" TEXT(255),
  "image" TEXT(255),
  "capital of" TEXT(255),
  "VIAF ID" TEXT(255),
  "area" TEXT(255),
  "population" TEXT(255),
  "Library of Congress authority ID" TEXT(255),
  "elevation above sea level" TEXT(255),
  "located in time zone" TEXT(255),
  "postal code" TEXT(255),
  "Who's on First ID" TEXT(255),
  "WorldCat Identities ID" TEXT(255),
  "National Library of Israel J9U ID" TEXT(255)
);
CREATE TABLE "political-border" (
  "label" TEXT(255),
  "description" TEXT(255),
  "Dewey Decimal Classification" TEXT(255),
  "country" TEXT(255),
  "capital" TEXT(255),
  "shares border with" TEXT(255),
  "located in the administrative territorial entity" TEXT(255),
  "Commons category" TEXT(255),
  "licence plate code" TEXT(255),
  "postal code" TEXT(255),
  "located in time zone" TEXT(255),
  "ISO 3166-2 code" TEXT(255),
  "image" TEXT(255),
  "coordinate location" TEXT(255),
  "contains the administrative territorial entity" TEXT(255),
  "locator map image" TEXT(255),
  "topic's main category" TEXT(255),
  "MusicBrainz area ID" TEXT(255),
  "instance of" TEXT(255),
  "Freebase ID" TEXT(255),
  "GND ID" TEXT(255),
  "GeoNames ID" TEXT(255),
  "NUTS code" TEXT(255),
  "VIAF ID" TEXT(255),
  "Commons gallery" TEXT(255),
  "official website" TEXT(255),
  "category of associated people" TEXT(255),
  "ISTAT ID" TEXT(255),
  "archINFORM location ID" TEXT(255),
  "area" TEXT(255),
  "Getty Thesaurus of Geographic Names ID" TEXT(255),
  "Library of Congress authority ID" TEXT(255),
  "Gran Enciclopèdia Catalana ID" TEXT(255),
  "WorldCat Identities ID" TEXT(255),
  "iNaturalist place ID" TEXT(255),
  "office held by head of government" TEXT(255),
  "Colon Classification" TEXT(255),
  "National Library of Israel J9U ID" TEXT(255),
  "EU Knowledge Graph item ID" TEXT(255),
  "OpenStreetMap relation ID" TEXT(255),
  "Who's on First ID" TEXT(255),
  "HASC" TEXT(255),
  "geoshape" TEXT(255),
  "topic's main template" TEXT(255),
  "page banner" TEXT(255)
);

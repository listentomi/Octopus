CREATE TABLE "depiction" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "instance of" VARCHAR(255)
);
CREATE TABLE "dream-of-the-red-chamber" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "language of work or name" VARCHAR(255),
  "instance of" VARCHAR(255),
  "title" VARCHAR(255),
  "part of" VARCHAR(255),
  "published in" VARCHAR(255),
  "follows" VARCHAR(255),
  "chapter" VARCHAR(255),
  "characters" VARCHAR(255),
  "narrative location" VARCHAR(255),
  "followed by" VARCHAR(255),
  "depicts" VARCHAR(255),
  FOREIGN KEY ("narrative location") REFERENCES "narrative-location" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY ("depicts") REFERENCES "depiction" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY ("characters") REFERENCES "fictional-character" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY ("followed by") REFERENCES "followed-by" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY ("follows") REFERENCES "follows" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT
);
CREATE TABLE "family-name" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "instance of" VARCHAR(255),
  "topic's main category" VARCHAR(255),
  "described by source" VARCHAR(255),
  "writing system" VARCHAR(255),
  "native label" VARCHAR(255),
  "said to be the same as" VARCHAR(255),
  "different from" VARCHAR(255),
  "image" VARCHAR(255),
  "exact match" VARCHAR(255)
);
CREATE TABLE "father" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "present in work" VARCHAR(255),
  "instance of" VARCHAR(255),
  "family name" VARCHAR(255),
  "child" VARCHAR(255),
  "sex or gender" VARCHAR(255),
  "spouse" VARCHAR(255),
  "native language" VARCHAR(255),
  "languages spoken, written or signed" VARCHAR(255),
  "country of citizenship" VARCHAR(255),
  "from narrative universe" VARCHAR(255),
  FOREIGN KEY ("family name") REFERENCES "family-name" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY ("spouse") REFERENCES "spouse" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT
);
CREATE TABLE "fictional-character" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "sex or gender" VARCHAR(255),
  "instance of" VARCHAR(255),
  "present in work" VARCHAR(255),
  "family name" VARCHAR(255),
  "father" VARCHAR(255),
  "residence" VARCHAR(255),
  "name in native language" VARCHAR(255),
  "native language" VARCHAR(255),
  "languages spoken, written or signed" VARCHAR(255),
  "country of citizenship" VARCHAR(255),
  "from narrative universe" VARCHAR(255),
  "first appearance" VARCHAR(255),
  FOREIGN KEY ("family name") REFERENCES "family-name" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY ("father") REFERENCES "father" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT
);
CREATE TABLE "narrative-location" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "instance of" VARCHAR(255),
  "present in work" VARCHAR(255),
  "country" VARCHAR(255),
  "located in the administrative territorial entity" VARCHAR(255),
  "native label" VARCHAR(255),
  "first appearance" VARCHAR(255),
  "from narrative universe" VARCHAR(255)
);
CREATE TABLE "spouse" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "present in work" VARCHAR(255),
  "instance of" VARCHAR(255),
  "child" VARCHAR(255),
  "sex or gender" VARCHAR(255),
  "spouse" VARCHAR(255),
  "country of citizenship" VARCHAR(255),
  "from narrative universe" VARCHAR(255),
  "native language" VARCHAR(255),
  "languages spoken, written or signed" VARCHAR(255)
);
CREATE TABLE "followed-by" (
  "label" TEXT(255),
  "description" TEXT(255),
  "language of work or name" TEXT(255),
  "follows" TEXT(255),
  "part of" TEXT(255),
  "chapter" TEXT(255),
  "instance of" TEXT(255),
  "title" TEXT(255),
  "characters" TEXT(255),
  "narrative location" TEXT(255),
  "followed by" TEXT(255),
  "depicts" TEXT(255),
  "published in" TEXT(255)
);
CREATE TABLE "follows" (
  "label" TEXT(255),
  "description" TEXT(255),
  "language of work or name" TEXT(255),
  "follows" TEXT(255),
  "part of" TEXT(255),
  "chapter" TEXT(255),
  "instance of" TEXT(255),
  "title" TEXT(255),
  "characters" TEXT(255),
  "narrative location" TEXT(255),
  "followed by" TEXT(255),
  "depicts" TEXT(255),
  "published in" TEXT(255)
);

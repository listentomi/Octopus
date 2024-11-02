CREATE TABLE "aspartic-peptidase-active-site-protein-family" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "UniProt protein ID" VARCHAR(255),
  "encoded by" VARCHAR(255),
  "biological process" VARCHAR(255),
  "molecular function" VARCHAR(255),
  "has part(s)" VARCHAR(255),
  "found in taxon" VARCHAR(255),
  "RefSeq protein ID" VARCHAR(255),
  "instance of" VARCHAR(255),
  "part of" VARCHAR(255),
  FOREIGN KEY ("biological process") REFERENCES "biological-process" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY ("encoded by") REFERENCES "encoded-by" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY ("found in taxon") REFERENCES "natural-product" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY ("part of") REFERENCES "part" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY ("molecular function") REFERENCES "molecular-function" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT
);
CREATE TABLE "biological-process" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "Gene Ontology ID" VARCHAR(255),
  "subclass of" VARCHAR(255),
  "exact match" VARCHAR(255),
  "instance of" VARCHAR(255)
);
CREATE TABLE "encoded-by" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "Entrez Gene ID" VARCHAR(255),
  "encodes" VARCHAR(255),
  "found in taxon" VARCHAR(255),
  "genomic start" VARCHAR(255),
  "strand orientation" VARCHAR(255),
  "genomic end" VARCHAR(255),
  "instance of" VARCHAR(255),
  FOREIGN KEY ("encodes") REFERENCES "encodes" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY ("found in taxon") REFERENCES "natural-product" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT
);
CREATE TABLE "encodes" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "UniProt protein ID" VARCHAR(255),
  "encoded by" VARCHAR(255),
  "biological process" VARCHAR(255),
  "molecular function" VARCHAR(255),
  "has part(s)" VARCHAR(255),
  "found in taxon" VARCHAR(255),
  "RefSeq protein ID" VARCHAR(255),
  "instance of" VARCHAR(255),
  "part of" VARCHAR(255)
);
CREATE TABLE "molecular-function" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "Gene Ontology ID" VARCHAR(255),
  "subclass of" VARCHAR(255),
  "exact match" VARCHAR(255),
  "instance of" VARCHAR(255)
);
CREATE TABLE "natural-product" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "instance of" VARCHAR(255),
  "taxon name" VARCHAR(255),
  "parent taxon" VARCHAR(255),
  "NCBI taxonomy ID" VARCHAR(255),
  FOREIGN KEY ("parent taxon") REFERENCES "taxon" ("label") ON DELETE RESTRICT ON UPDATE RESTRICT
);
CREATE TABLE "part" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "InterPro ID" VARCHAR(255),
  "instance of" VARCHAR(255)
);
CREATE TABLE "taxon" (
  "label" VARCHAR(255),
  "description" VARCHAR(255),
  "parent taxon" VARCHAR(255),
  "taxon name" VARCHAR(255),
  "instance of" VARCHAR(255),
  "taxon rank" VARCHAR(255),
  "ITIS TSN" VARCHAR(255),
  "NCBI taxonomy ID" VARCHAR(255),
  "GBIF taxon ID" VARCHAR(255)
);

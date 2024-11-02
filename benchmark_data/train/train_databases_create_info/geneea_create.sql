CREATE TABLE "bod_schuze" (
	"id_bod" INTEGER NOT NULL  ,
	"id_schuze" INTEGER NOT NULL  ,
	"id_tisk" VARCHAR(255) NULL  ,
	"id_typ" VARCHAR(255) NULL  ,
	"bod" INTEGER NOT NULL  ,
	"uplny_naz" TEXT NULL  ,
	"uplny_kon" VARCHAR(255) NULL  ,
	"poznamka" VARCHAR(255) NULL  ,
	"id_bod_stav" INTEGER NOT NULL  ,
	"pozvanka" VARCHAR(255) NULL  ,
	"rj" VARCHAR(255) NULL  ,
	"pozn2" VARCHAR(255) NULL  ,
	"druh_bodu" VARCHAR(255) NULL  ,
	"id_sd" VARCHAR(255) NULL  ,
	"zkratka" VARCHAR(255) NULL,
	FOREIGN KEY("id_schuze") REFERENCES "schuze" ("id_schuze") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("id_bod_stav") REFERENCES "bod_stav" ("id_bod_stav") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "bod_stav" (
	"id_bod_stav" INTEGER NOT NULL  ,
	"popis" VARCHAR(255) NULL  ,
	PRIMARY KEY ("id_bod_stav")
);
CREATE TABLE "funkce" (
	"id_funkce" INTEGER NOT NULL  ,
	"id_organ" INTEGER NULL  ,
	"id_typ_funkce" INTEGER NULL  ,
	"nazev_funkce_cz" TEXT NULL  ,
	"priorita" INTEGER NULL  ,
	PRIMARY KEY ("id_funkce"),
	FOREIGN KEY("id_organ") REFERENCES "organy" ("id_organ") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("id_typ_funkce") REFERENCES "typ_funkce" ("id_typ_funkce") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "hl_check" (
	"id_hlasovani" INTEGER NULL  ,
	"turn" INTEGER NULL  ,
	"mode" INTEGER NULL  ,
	"id_h2" VARCHAR(255) NULL  ,
	"id_h3" VARCHAR(255) NULL,
	FOREIGN KEY("id_hlasovani") REFERENCES "hl_hlasovani" ("id_hlasovani") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "hl_hlasovani" (
	"id_hlasovani" INTEGER NOT NULL  ,
	"id_organ" INTEGER NULL  ,
	"schuze" INTEGER NULL  ,
	"cislo" INTEGER NULL  ,
	"bod" INTEGER NULL  ,
	"datum" DATE NULL  ,
	"cas" TIME NULL  ,
	"pro" INTEGER NULL  ,
	"proti" INTEGER NULL  ,
	"zdrzel" INTEGER NULL  ,
	"nehlasoval" INTEGER NULL  ,
	"prihlaseno" INTEGER NULL  ,
	"kvorum" INTEGER NULL  ,
	"druh_hlasovani" VARCHAR(255) NULL  ,
	"vysledek" VARCHAR(255) NULL  ,
	"nazev_dlouhy" TEXT NULL  ,
	"nazev_kratky" VARCHAR(255) NULL  ,
	PRIMARY KEY ("id_hlasovani"),
	FOREIGN KEY("id_organ") REFERENCES "organy" ("id_organ") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "hl_poslanec" (
	"id_poslanec" INTEGER NOT NULL  ,
	"id_hlasovani" INTEGER NOT NULL  ,
	"vysledek" VARCHAR(255) NULL,
	FOREIGN KEY("id_poslanec") REFERENCES "poslanec" ("id_poslanec") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "hl_vazby" (
	"id_hlasovani" INTEGER NULL  ,
	"turn" INTEGER NULL  ,
	"typ" INTEGER NULL,
	FOREIGN KEY("id_hlasovani") REFERENCES "hl_hlasovani" ("id_hlasovani") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "hl_zposlanec" (
	"id_hlasovani" INTEGER NULL  ,
	"id_osoba" INTEGER NULL  ,
	"mode" INTEGER NULL,
	FOREIGN KEY("id_hlasovani") REFERENCES "hl_hlasovani" ("id_hlasovani") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("id_osoba") REFERENCES "osoby" ("id_osoba") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "omluvy" (
	"id_organ" INTEGER NOT NULL  ,
	"id_poslanec" INTEGER NOT NULL  ,
	"den" VARCHAR(255) NOT NULL  ,
	"od" VARCHAR(255) NULL  ,
	"do" VARCHAR(255) NULL,
	FOREIGN KEY("id_organ") REFERENCES "organy" ("id_organ") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("id_poslanec") REFERENCES "poslanec" ("id_poslanec") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "organy" (
	"id_organ" INTEGER NOT NULL  ,
	"organ_id_organ" INTEGER NULL  ,
	"id_typ_organu" INTEGER NULL  ,
	"zkratka" VARCHAR(255) NULL  ,
	"nazev_organu_cz" TEXT NULL  ,
	"nazev_organu_en" TEXT NULL  ,
	"od_organ" VARCHAR(255) NULL  ,
	"do_organ" VARCHAR(255) NULL  ,
	"priorita" VARCHAR(255) NULL  ,
	"cl_organ_base" INTEGER NULL  ,
	PRIMARY KEY ("id_organ"),
	FOREIGN KEY("id_typ_organu") REFERENCES "typ_organu" ("id_typ_org") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "osoby" (
	"id_osoba" INTEGER NOT NULL  ,
	"pred" VARCHAR(255) NULL  ,
	"jmeno" VARCHAR(255) NULL  ,
	"prijmeni" VARCHAR(255) NULL  ,
	"za" VARCHAR(255) NULL  ,
	"narozeni" VARCHAR(255) NULL  ,
	"pohlavi" VARCHAR(255) NULL  ,
	"zmena" VARCHAR(255) NULL  ,
	"umrti" VARCHAR(255) NULL  ,
	PRIMARY KEY ("id_osoba")
);
CREATE TABLE "pkgps" (
	"id_poslanec" INTEGER NULL  ,
	"adresa" VARCHAR(255) NULL  ,
	"sirka" FLOAT NULL  ,
	"delka" FLOAT NULL,
	FOREIGN KEY("id_poslanec") REFERENCES "poslanec" ("id_poslanec") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "poslanec" (
	"id_poslanec" INTEGER NOT NULL  ,
	"id_osoba" INTEGER NULL  ,
	"id_kraj" INTEGER NULL  ,
	"id_kandidatka" INTEGER NULL  ,
	"id_obdobi" INTEGER NULL  ,
	"web" VARCHAR(255) NULL  ,
	"ulice" VARCHAR(255) NULL  ,
	"obec" VARCHAR(255) NULL  ,
	"psc" VARCHAR(255) NULL  ,
	"email" VARCHAR(255) NULL  ,
	"telefon" VARCHAR(255) NULL  ,
	"fax" VARCHAR(255) NULL  ,
	"psp_telefon" VARCHAR(255) NULL  ,
	"facebook" VARCHAR(255) NULL  ,
	"foto" INTEGER NULL  ,
	PRIMARY KEY ("id_poslanec"),
	FOREIGN KEY("id_osoba") REFERENCES "osoby" ("id_osoba") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "schuze" (
	"id_schuze" INTEGER NOT NULL  ,
	"id_organ" INTEGER NULL  ,
	"schuze" INTEGER NULL  ,
	"od_schuze" VARCHAR(255) NULL  ,
	"do_schuze" VARCHAR(255) NULL  ,
	"aktualizace" VARCHAR(255) NULL  ,
	PRIMARY KEY ("id_schuze"),
	FOREIGN KEY("id_organ") REFERENCES "organy" ("id_organ") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "schuze_stav" (
	"id_schuze" INTEGER NULL  ,
	"stav" INTEGER NULL  ,
	"typ" VARCHAR(255) NULL  ,
	"text_dt" VARCHAR(255) NULL  ,
	"text_st" VARCHAR(255) NULL  ,
	"tm_line" VARCHAR(255) NULL,
	FOREIGN KEY("id_schuze") REFERENCES "schuze" ("id_schuze") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "typ_funkce" (
	"id_typ_funkce" INTEGER NOT NULL  ,
	"id_typ_org" INTEGER NULL  ,
	"typ_funkce_cz" VARCHAR(255) NULL  ,
	"typ_funkce_en" VARCHAR(255) NULL  ,
	"priorita" INTEGER NULL  ,
	"typ_funkce_obecny" INTEGER NULL  ,
	PRIMARY KEY ("id_typ_funkce"),
	FOREIGN KEY("id_typ_org") REFERENCES "typ_organu" ("id_typ_org") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "typ_organu" (
	"id_typ_org" INTEGER NOT NULL  ,
	"typ_id_typ_org" VARCHAR(255) NULL  ,
	"nazev_typ_org_cz" VARCHAR(255) NULL  ,
	"nazev_typ_org_en" VARCHAR(255) NULL  ,
	"typ_org_obecny" VARCHAR(255) NULL  ,
	"priorita" INTEGER NULL  ,
	PRIMARY KEY ("id_typ_org")
);
CREATE TABLE "zarazeni" (
	"id_osoba" INTEGER NULL  ,
	"id_of" INTEGER NULL  ,
	"cl_funkce" INTEGER NULL  ,
	"od_o" VARCHAR(255) NULL  ,
	"do_o" VARCHAR(255) NULL  ,
	"od_f" VARCHAR(255) NULL  ,
	"do_f" VARCHAR(255) NULL,
	FOREIGN KEY("id_osoba") REFERENCES "osoby" ("id_osoba") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "zmatecne" (
	"id_hlasovani" INTEGER NULL,
	FOREIGN KEY("id_hlasovani") REFERENCES "hl_hlasovani" ("id_hlasovani") ON UPDATE CASCADE ON DELETE CASCADE
);

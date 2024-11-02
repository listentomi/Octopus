CREATE TABLE "account" (
	"account_id" INTEGER NOT NULL DEFAULT '0' ,
	"district_id" INTEGER NOT NULL DEFAULT '0' ,
	"frequency" VARCHAR(18) NOT NULL  ,
	"date" DATE NOT NULL  ,
	PRIMARY KEY ("account_id"),
	FOREIGN KEY("district_id") REFERENCES "district" ("district_id") ON UPDATE RESTRICT ON DELETE RESTRICT
);
CREATE TABLE "card" (
	"card_id" INTEGER NOT NULL DEFAULT '0' ,
	"disp_id" INTEGER NOT NULL  ,
	"type" VARCHAR(7) NOT NULL  ,
	"issued" DATE NOT NULL  ,
	PRIMARY KEY ("card_id"),
	FOREIGN KEY("disp_id") REFERENCES "disp" ("disp_id") ON UPDATE RESTRICT ON DELETE RESTRICT
);
CREATE TABLE "client" (
	"client_id" INTEGER NOT NULL  ,
	"gender" VARCHAR(1) NOT NULL  ,
	"birth_date" DATE NOT NULL  ,
	"district_id" INTEGER NOT NULL  ,
	PRIMARY KEY ("client_id"),
	FOREIGN KEY("district_id") REFERENCES "district" ("district_id") ON UPDATE RESTRICT ON DELETE RESTRICT
);
CREATE TABLE "disp" (
	"disp_id" INTEGER NOT NULL  ,
	"client_id" INTEGER NOT NULL  ,
	"account_id" INTEGER NOT NULL  ,
	"type" VARCHAR(9) NOT NULL  ,
	PRIMARY KEY ("disp_id"),
	FOREIGN KEY("account_id") REFERENCES "account" ("account_id") ON UPDATE RESTRICT ON DELETE RESTRICT,
	FOREIGN KEY("client_id") REFERENCES "client" ("client_id") ON UPDATE RESTRICT ON DELETE RESTRICT
);
CREATE TABLE "district" (
	"district_id" INTEGER NOT NULL DEFAULT '0' ,
	"A2" VARCHAR(19) NOT NULL  ,
	"A3" VARCHAR(15) NOT NULL  ,
	"A4" INTEGER NOT NULL  ,
	"A5" INTEGER NOT NULL  ,
	"A6" INTEGER NOT NULL  ,
	"A7" INTEGER NOT NULL  ,
	"A8" INTEGER NOT NULL  ,
	"A9" INTEGER NOT NULL  ,
	"A10" DECIMAL NOT NULL  ,
	"A11" INTEGER NOT NULL  ,
	"A12" DECIMAL NULL  ,
	"A13" DECIMAL NOT NULL  ,
	"A14" INTEGER NOT NULL  ,
	"A15" INTEGER NULL  ,
	"A16" INTEGER NOT NULL  ,
	PRIMARY KEY ("district_id")
);
CREATE TABLE "loan" (
	"loan_id" INTEGER NOT NULL DEFAULT '0' ,
	"account_id" INTEGER NOT NULL  ,
	"date" DATE NOT NULL  ,
	"amount" INTEGER NOT NULL  ,
	"duration" INTEGER NOT NULL  ,
	"payments" DECIMAL NOT NULL  ,
	"status" VARCHAR(1) NOT NULL  ,
	PRIMARY KEY ("loan_id"),
	FOREIGN KEY("account_id") REFERENCES "account" ("account_id") ON UPDATE RESTRICT ON DELETE RESTRICT
);
CREATE TABLE "order" (
	"order_id" INTEGER NOT NULL DEFAULT '0' ,
	"account_id" INTEGER NOT NULL  ,
	"bank_to" VARCHAR(2) NOT NULL  ,
	"account_to" INTEGER NOT NULL  ,
	"amount" DECIMAL NOT NULL  ,
	"k_symbol" VARCHAR(8) NOT NULL  ,
	PRIMARY KEY ("order_id"),
	FOREIGN KEY("account_id") REFERENCES "account" ("account_id") ON UPDATE RESTRICT ON DELETE RESTRICT
);
CREATE TABLE "trans" (
	"trans_id" INTEGER NOT NULL DEFAULT '0' ,
	"account_id" INTEGER NOT NULL DEFAULT '0' ,
	"date" DATE NOT NULL  ,
	"type" VARCHAR(6) NOT NULL  ,
	"operation" VARCHAR(14) NULL  ,
	"amount" INTEGER NOT NULL  ,
	"balance" INTEGER NOT NULL  ,
	"k_symbol" VARCHAR(11) NULL  ,
	"bank" VARCHAR(2) NULL  ,
	"account" INTEGER NULL  ,
	PRIMARY KEY ("trans_id"),
	FOREIGN KEY("account_id") REFERENCES "account" ("account_id") ON UPDATE RESTRICT ON DELETE RESTRICT
);

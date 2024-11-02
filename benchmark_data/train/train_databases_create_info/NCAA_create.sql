CREATE TABLE "regular_season_compact_results" (
	"season" INTEGER NOT NULL  ,
	"daynum" INTEGER NOT NULL  ,
	"wteam" INTEGER NOT NULL  ,
	"wscore" INTEGER NULL  ,
	"lteam" INTEGER NOT NULL  ,
	"lscore" INTEGER NULL  ,
	"wloc" VARCHAR(255) NULL  ,
	"numot" INTEGER NULL  ,
	PRIMARY KEY ("season", "daynum", "wteam", "lteam"),
	FOREIGN KEY("season") REFERENCES "seasons" ("season") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("wteam") REFERENCES "teams" ("team_id") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("lteam") REFERENCES "teams" ("team_id") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "regular_season_detailed_results" (
	"season" INTEGER NOT NULL  ,
	"daynum" INTEGER NOT NULL  ,
	"wteam" INTEGER NOT NULL  ,
	"wscore" INTEGER NOT NULL  ,
	"lteam" INTEGER NOT NULL  ,
	"lscore" INTEGER NOT NULL  ,
	"wloc" VARCHAR(255) NULL  ,
	"numot" INTEGER NULL  ,
	"wfgm" INTEGER NULL  ,
	"wfga" INTEGER NULL  ,
	"wfgm3" INTEGER NULL  ,
	"wfga3" INTEGER NULL  ,
	"wftm" INTEGER NULL  ,
	"wfta" INTEGER NULL  ,
	"wor" INTEGER NULL  ,
	"wdr" INTEGER NULL  ,
	"wast" INTEGER NULL  ,
	"wto" INTEGER NULL  ,
	"wstl" INTEGER NULL  ,
	"wblk" INTEGER NULL  ,
	"wpf" INTEGER NULL  ,
	"lfgm" INTEGER NULL  ,
	"lfga" INTEGER NULL  ,
	"lfgm3" INTEGER NULL  ,
	"lfga3" INTEGER NULL  ,
	"lftm" INTEGER NULL  ,
	"lfta" INTEGER NULL  ,
	"lor" INTEGER NULL  ,
	"ldr" INTEGER NULL  ,
	"last" INTEGER NULL  ,
	"lto" INTEGER NULL  ,
	"lstl" INTEGER NULL  ,
	"lblk" INTEGER NULL  ,
	"lpf" INTEGER NULL  ,
	PRIMARY KEY ("season", "daynum", "wteam", "lteam"),
	FOREIGN KEY("season") REFERENCES "seasons" ("season") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("wteam") REFERENCES "teams" ("team_id") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("lteam") REFERENCES "teams" ("team_id") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "seasons" (
	"season" INTEGER NOT NULL  ,
	"dayzero" DATETIME NULL  ,
	"regionW" VARCHAR(255) NULL  ,
	"regionX" VARCHAR(255) NULL  ,
	"regionY" VARCHAR(255) NULL  ,
	"regionZ" VARCHAR(255) NULL  ,
	PRIMARY KEY ("season")
);
CREATE TABLE "target" (
	"id" VARCHAR(255) NOT NULL  ,
	"season" INTEGER NULL  ,
	"team_id1" INTEGER NULL  ,
	"team_id2" INTEGER NULL  ,
	"pred" FLOAT NULL  ,
	"team_id1_wins" INTEGER NULL  ,
	"team_id2_wins" INTEGER NULL  ,
	PRIMARY KEY ("id"),
	FOREIGN KEY("team_id1") REFERENCES "teams" ("team_id") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("team_id2") REFERENCES "teams" ("team_id") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "teams" (
	"team_id" INTEGER NOT NULL  ,
	"team_name" VARCHAR(255) NULL  ,
	PRIMARY KEY ("team_id")
);
CREATE TABLE "tourney_compact_results" (
	"season" INTEGER NOT NULL  ,
	"daynum" INTEGER NOT NULL  ,
	"wteam" INTEGER NOT NULL  ,
	"wscore" INTEGER NULL  ,
	"lteam" INTEGER NOT NULL  ,
	"lscore" INTEGER NULL  ,
	"wloc" VARCHAR(255) NULL  ,
	"numot" INTEGER NULL  ,
	PRIMARY KEY ("season", "daynum", "wteam", "lteam"),
	FOREIGN KEY("season") REFERENCES "seasons" ("season") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("wteam") REFERENCES "teams" ("team_id") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("lteam") REFERENCES "teams" ("team_id") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "tourney_detailed_results" (
	"season" INTEGER NOT NULL  ,
	"daynum" INTEGER NOT NULL  ,
	"wteam" INTEGER NOT NULL  ,
	"wscore" INTEGER NULL  ,
	"lteam" INTEGER NOT NULL  ,
	"lscore" INTEGER NULL  ,
	"wloc" VARCHAR(255) NULL  ,
	"numot" INTEGER NULL  ,
	"wfgm" INTEGER NULL  ,
	"wfga" INTEGER NULL  ,
	"wfgm3" INTEGER NULL  ,
	"wfga3" INTEGER NULL  ,
	"wftm" INTEGER NULL  ,
	"wfta" INTEGER NULL  ,
	"wor" INTEGER NULL  ,
	"wdr" INTEGER NULL  ,
	"wast" INTEGER NULL  ,
	"wto" INTEGER NULL  ,
	"wstl" INTEGER NULL  ,
	"wblk" INTEGER NULL  ,
	"wpf" INTEGER NULL  ,
	"lfgm" INTEGER NULL  ,
	"lfga" INTEGER NULL  ,
	"lfgm3" INTEGER NULL  ,
	"lfga3" INTEGER NULL  ,
	"lftm" INTEGER NULL  ,
	"lfta" INTEGER NULL  ,
	"lor" INTEGER NULL  ,
	"ldr" INTEGER NULL  ,
	"last" INTEGER NULL  ,
	"lto" INTEGER NULL  ,
	"lstl" INTEGER NULL  ,
	"lblk" INTEGER NULL  ,
	"lpf" INTEGER NULL  ,
	PRIMARY KEY ("season", "daynum", "wteam", "lteam"),
	FOREIGN KEY("season") REFERENCES "seasons" ("season") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("wteam") REFERENCES "teams" ("team_id") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("lteam") REFERENCES "teams" ("team_id") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "tourney_seeds" (
	"season" INTEGER NOT NULL  ,
	"seed" VARCHAR(255) NOT NULL  ,
	"team" INTEGER NULL  ,
	PRIMARY KEY ("season", "seed"),
	FOREIGN KEY("season") REFERENCES "seasons" ("season") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("team") REFERENCES "teams" ("team_id") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE "tourney_slots" (
	"season" INTEGER NOT NULL  ,
	"slot" VARCHAR(255) NOT NULL  ,
	"strongseed" VARCHAR(255) NULL  ,
	"weakseed" VARCHAR(255) NULL  ,
	PRIMARY KEY ("slot", "season"),
	FOREIGN KEY("season") REFERENCES "seasons" ("season") ON UPDATE CASCADE ON DELETE CASCADE
);
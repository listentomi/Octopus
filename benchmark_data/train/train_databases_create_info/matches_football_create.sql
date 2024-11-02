CREATE TABLE "matches" (
"tourney_id" TEXT,
  "tourney_name" TEXT,
  "surface" TEXT,
  "draw_size" TEXT,
  "tourney_level" TEXT,
  "tourney_date" REAL,
  "match_num" TEXT,
  "winner1_id" REAL,
  "winner2_id" TEXT,
  "winner_seed" TEXT,
  "winner_entry" TEXT,
  "loser1_id" TEXT,
  "loser2_id" REAL,
  "loser_seed" TEXT,
  "loser_entry" TEXT,
  "score" TEXT,
  "best_of" TEXT,
  "round" TEXT,
  "winner1_name" TEXT,
  "winner1_hand" REAL,
  "winner1_ht" TEXT,
  "winner1_ioc" REAL,
  "winner1_age" TEXT,
  "winner2_name" TEXT,
  "winner2_hand" REAL,
  "winner2_ht" TEXT,
  "winner2_ioc" REAL,
  "winner2_age" TEXT,
  "loser1_name" TEXT,
  "loser1_hand" REAL,
  "loser1_ht" TEXT,
  "loser1_ioc" REAL,
  "loser1_age" TEXT,
  "loser2_name" TEXT,
  "loser2_hand" REAL,
  "loser2_ht" TEXT,
  "loser2_ioc" REAL,
  "loser2_age" REAL,
  "winner1_rank" REAL,
  "winner1_rank_points" REAL,
  "winner2_rank" REAL,
  "winner2_rank_points" REAL,
  "loser1_rank" REAL,
  "loser1_rank_points" REAL,
  "loser2_rank" REAL,
  "loser2_rank_points" REAL,
  "minutes" REAL,
  "w_ace" REAL,
  "w_df" REAL,
  "w_svpt" REAL,
  "w_1stIn" REAL,
  "w_1stWon" REAL,
  "w_2ndWon" REAL,
  "w_SvGms" REAL,
  "w_bpSaved" REAL,
  "w_bpFaced" REAL,
  "l_ace" REAL,
  "l_df" REAL,
  "l_svpt" REAL,
  "l_1stIn" REAL,
  "l_1stWon" REAL,
  "l_2ndWon" REAL,
  "l_SvGms" REAL,
  "l_bpSaved" REAL,
  "l_bpFaced" REAL,
  "winner_id" REAL,
  "winner_name" TEXT,
  "winner_hand" TEXT,
  "winner_ht" REAL,
  "winner_ioc" TEXT,
  "winner_age" REAL,
  "loser_id" REAL,
  "loser_name" TEXT,
  "loser_hand" TEXT,
  "loser_ht" REAL,
  "loser_ioc" TEXT,
  "loser_age" REAL,
  "winner_rank" REAL,
  "winner_rank_points" REAL,
  "loser_rank" REAL,
  "loser_rank_points" REAL
);
CREATE TABLE "players" (
"player_id" INTEGER,
  "name_first" TEXT,
  "name_last" TEXT,
  "hand" TEXT,
  "dob" REAL,
  "ioc" TEXT,
  "height" REAL,
  "wikidata_id" TEXT
);
CREATE TABLE "rankings" (
"ranking_date" INTEGER,
  "rank" INTEGER,
  "player" INTEGER,
  "points" REAL
);
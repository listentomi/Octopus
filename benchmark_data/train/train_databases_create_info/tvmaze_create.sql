CREATE TABLE tvmaze (
    tvmaze_id integer NOT NULL primary key,
    update_timestamp integer DEFAULT 0,
    showname text,
    first_airing text,
    imdb text,
    lang text,
    description text
);
CREATE TABLE tvmaze_characters (
    tvmaze_character_id integer NOT NULL primary key,
    name text,
    is_self_role boolean
);
CREATE TABLE tvmaze_people (
    tvmaze_person_id integer NOT NULL primary key,
    name text,
    birthday text,
    deathday text,
    gender text
);
CREATE TABLE tvmaze_casting (
    tvmaze_id integer not null references tvmaze,
    tvmaze_person_id integer not null references tvmaze_people,
    tvmaze_character_id integer not null references tvmaze_characters
);
CREATE TABLE tvmaze_genre (
    tvmaze_id integer not null references tvmaze,
    genre text
);

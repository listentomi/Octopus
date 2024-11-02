CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE tip (
        user_id TEXT,
        business_id TEXT,
        text TEXT,
        date TEXT,
        likes INTEGER
    );
CREATE TABLE friend (
        user_id TEXT,
        friend_id TEXT
    );
CREATE TABLE user (
        id TEXT,
        name TEXT,
        review_count INTEGER,
        yelping_since TEXT,
        useful INTEGER,
        funny INTEGER,
        cool INTEGER,
        fans INTEGER,
        average_stars REAL,
        compliment_hot INTEGER,
        compliment_more INTEGER,
        compliment_profile INTEGER,
        compliment_cute INTEGER,
        compliment_list INTEGER,
        compliment_note INTEGER,
        compliment_plain INTEGER,
        compliment_cool INTEGER,
        compliment_funny INTEGER,
        compliment_writer INTEGER,
        compliment_photos INTEGER
    );
CREATE TABLE business (
        id TEXT,
        name TEXT,
        address TEXT,
        city TEXT,
        state TEXT,
        postal_code TEXT,
        latitude FLOAT,
        longitude FLOAT,
        stars INTEGER,
        review_count INTEGER,
        is_open INTEGER
    );
CREATE TABLE attribute (
        business_id TEXT,
        name TEXT,
        value TEXT
    );
CREATE TABLE review (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stars INTEGER,
        date TEXT,
        text TEXT,
        useful INTEGER,
        funny INTEGER,
        cool INTEGER,
        business_id TEXT,
        user_id TEXT
    );
CREATE TABLE checkin (
        business_id TEXT,
        date TEXT,
        count INTEGER
    );
CREATE TABLE category (
        business_id TEXT,
        category TEXT
    );
CREATE TABLE elite_years (
        user_id TEXT,
        year INTEGER
    );
CREATE TABLE hours (
        hours TEXT,
        business_id TEXT
    );

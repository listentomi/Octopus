CREATE TABLE artists
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(120)
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE albums
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(160)  NOT NULL,
    artist_id INTEGER  NOT NULL,
    FOREIGN KEY (artist_id) REFERENCES artists (id)
    ON DELETE NO ACTION ON UPDATE NO ACTION
);
CREATE TABLE employees
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name VARCHAR(20)  NOT NULL,
    first_name VARCHAR(20)  NOT NULL,
    title VARCHAR(30),
    reports_to INTEGER,
    birth_date TIMESTAMP,
    hire_date TIMESTAMP,
    address VARCHAR(70),
    city VARCHAR(40),
    state VARCHAR(40),
    country VARCHAR(40),
    postal_code VARCHAR(10),
    phone VARCHAR(24),
    fax VARCHAR(24),
    email VARCHAR(60),
    FOREIGN KEY (reports_to) REFERENCES employees (id)
    ON DELETE NO ACTION ON UPDATE NO ACTION
);
CREATE TABLE customers
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(40)  NOT NULL,
    last_name VARCHAR(20)  NOT NULL,
    company VARCHAR(80),
    address VARCHAR(70),
    city VARCHAR(40),
    state VARCHAR(40),
    country VARCHAR(40),
    postal_code VARCHAR(10),
    phone VARCHAR(24),
    fax VARCHAR(24),
    email VARCHAR(60)  NOT NULL,
    support_rep_id INTEGER,
    FOREIGN KEY (support_rep_id) REFERENCES employees (id)
    ON DELETE NO ACTION ON UPDATE NO ACTION
);
CREATE TABLE genres
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(120)
);
CREATE TABLE invoices
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER  NOT NULL,
    invoice_date TIMESTAMP  NOT NULL,
    billing_address VARCHAR(70),
    billing_city VARCHAR(40),
    billing_state VARCHAR(40),
    billing_country VARCHAR(40),
    billing_postal_code VARCHAR(10),
    total NUMERIC(10,2)  NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (id)
    ON DELETE NO ACTION ON UPDATE NO ACTION
);
CREATE TABLE media_types
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(120)
);
CREATE TABLE tracks
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200)  NOT NULL,
    album_id INTEGER,
    media_type_id INTEGER  NOT NULL,
    genre_id INTEGER,
    composer VARCHAR(220),
    milliseconds INTEGER  NOT NULL,
    bytes INTEGER,
    unit_price NUMERIC(10,2)  NOT NULL,
    FOREIGN KEY (album_id) REFERENCES albums (id)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (genre_id) REFERENCES genres (id)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (media_type_id) REFERENCES media_types (id)
    ON DELETE NO ACTION ON UPDATE NO ACTION
);
CREATE TABLE invoice_lines
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER  NOT NULL,
    track_id INTEGER  NOT NULL,
    unit_price NUMERIC(10,2)  NOT NULL,
    quantity INTEGER  NOT NULL,
    FOREIGN KEY (invoice_id) REFERENCES invoices (id)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (track_id) REFERENCES tracks (id)
    ON DELETE NO ACTION ON UPDATE NO ACTION
);
CREATE TABLE playlists
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(120)
);
CREATE TABLE playlist_tracks
(
    playlist_id INTEGER  NOT NULL,
    track_id INTEGER  NOT NULL,
    CONSTRAINT PK_PlaylistTrack PRIMARY KEY  (playlist_id, track_id),
    FOREIGN KEY (playlist_id) REFERENCES playlists (id)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (track_id) REFERENCES tracks (id)
    ON DELETE NO ACTION ON UPDATE NO ACTION
);

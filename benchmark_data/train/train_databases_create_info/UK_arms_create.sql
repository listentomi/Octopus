CREATE TABLE item (
	item_id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	core VARCHAR NOT NULL, 
	PRIMARY KEY (item_id), 
	UNIQUE (name)
);
CREATE TABLE bundle (
	bundle_id INTEGER NOT NULL, 
	single BOOLEAN, 
	PRIMARY KEY (bundle_id), 
	CHECK (single IN (0, 1))
);
CREATE TABLE region (
	region_id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	iso2 VARCHAR, 
	PRIMARY KEY (region_id), 
	UNIQUE (name)
);
CREATE TABLE rating (
	rating_id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	military BOOLEAN, 
	full_description VARCHAR, 
	short_description VARCHAR, 
	sort INTEGER, 
	PRIMARY KEY (rating_id), 
	UNIQUE (name), 
	CHECK (military IN (0, 1))
);
CREATE TABLE user_type (
	user_type_id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	PRIMARY KEY (user_type_id), 
	UNIQUE (name)
);
CREATE TABLE licence_type (
	licence_type_id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	PRIMARY KEY (licence_type_id), 
	UNIQUE (name)
);
CREATE TABLE footnote (
	footnote_id INTEGER NOT NULL, 
	text VARCHAR NOT NULL, 
	PRIMARY KEY (footnote_id)
);
CREATE TABLE calendar (
	date DATE NOT NULL, 
	PRIMARY KEY (date)
);
CREATE TABLE criteria (
	criteria_id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	PRIMARY KEY (criteria_id)
);
CREATE TABLE licence (
	licence_id INTEGER NOT NULL, 
	bundle_id INTEGER, 
	licence_type_id INTEGER NOT NULL, 
	region_id INTEGER NOT NULL, 
	item_id INTEGER NOT NULL, 
	user_type_id INTEGER, 
	date DATE NOT NULL, 
	refused BOOLEAN NOT NULL, 
	unused VARCHAR, 
	quantity INTEGER, 
	"temporary" BOOLEAN NOT NULL, 
	incorporation BOOLEAN NOT NULL, 
	ec_reg_1236_2005 BOOLEAN NOT NULL, 
	known_revoked BOOLEAN NOT NULL, 
	revocation_date DATE, 
	PRIMARY KEY (licence_id), 
	FOREIGN KEY(bundle_id) REFERENCES bundle (bundle_id), 
	FOREIGN KEY(licence_type_id) REFERENCES licence_type (licence_type_id), 
	FOREIGN KEY(region_id) REFERENCES region (region_id), 
	FOREIGN KEY(item_id) REFERENCES item (item_id), 
	FOREIGN KEY(user_type_id) REFERENCES user_type (user_type_id), 
	FOREIGN KEY(date) REFERENCES calendar (date), 
	CHECK (refused IN (0, 1)), 
	CHECK ("temporary" IN (0, 1)), 
	CHECK (incorporation IN (0, 1)), 
	CHECK (ec_reg_1236_2005 IN (0, 1)), 
	CHECK (known_revoked IN (0, 1))
);
CREATE TABLE refusal_criteria (
	bundle_id INTEGER, 
	criteria_id INTEGER, 
	FOREIGN KEY(bundle_id) REFERENCES bundle (bundle_id), 
	FOREIGN KEY(criteria_id) REFERENCES criteria (criteria_id)
);
CREATE TABLE source (
	bundle_id INTEGER, 
	region_id INTEGER, 
	FOREIGN KEY(bundle_id) REFERENCES bundle (bundle_id), 
	FOREIGN KEY(region_id) REFERENCES region (region_id)
);
CREATE TABLE valuation (
	valuation_id INTEGER NOT NULL, 
	bundle_id INTEGER NOT NULL, 
	rating_id INTEGER NOT NULL, 
	count INTEGER NOT NULL, 
	value BIGINT, 
	region_id INTEGER NOT NULL, 
	date DATE NOT NULL, 
	refused BOOLEAN NOT NULL, 
	unused VARCHAR, 
	PRIMARY KEY (valuation_id), 
	FOREIGN KEY(bundle_id) REFERENCES bundle (bundle_id), 
	FOREIGN KEY(rating_id) REFERENCES rating (rating_id), 
	FOREIGN KEY(region_id) REFERENCES region (region_id), 
	FOREIGN KEY(date) REFERENCES calendar (date), 
	CHECK (refused IN (0, 1))
);
CREATE TABLE destination (
	bundle_id INTEGER, 
	region_id INTEGER, 
	FOREIGN KEY(bundle_id) REFERENCES bundle (bundle_id), 
	FOREIGN KEY(region_id) REFERENCES region (region_id)
);
CREATE TABLE region_footnote (
	region_id INTEGER, 
	date DATE, 
	footnote_id INTEGER, 
	FOREIGN KEY(region_id) REFERENCES region (region_id), 
	FOREIGN KEY(date) REFERENCES calendar (date), 
	FOREIGN KEY(footnote_id) REFERENCES footnote (footnote_id)
);
CREATE TABLE licence_footnote (
	licence_id INTEGER, 
	footnote_id INTEGER, 
	FOREIGN KEY(licence_id) REFERENCES licence (licence_id), 
	FOREIGN KEY(footnote_id) REFERENCES footnote (footnote_id)
);

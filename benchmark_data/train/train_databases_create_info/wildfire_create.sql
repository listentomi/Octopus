CREATE TABLE spatial_ref_sys (
srid INTEGER NOT NULL PRIMARY KEY,
auth_name TEXT NOT NULL,
auth_srid INTEGER NOT NULL,
ref_sys_name TEXT NOT NULL DEFAULT 'Unknown',
proj4text TEXT NOT NULL,
srtext TEXT NOT NULL DEFAULT 'Undefined');
CREATE TABLE spatialite_history (
event_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
table_name TEXT NOT NULL,
geometry_column TEXT,
event TEXT NOT NULL,
timestamp TEXT NOT NULL,
ver_sqlite TEXT NOT NULL,
ver_splite TEXT NOT NULL);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE geometry_columns (
f_table_name TEXT NOT NULL,
f_geometry_column TEXT NOT NULL,
geometry_type INTEGER NOT NULL,
coord_dimension INTEGER NOT NULL,
srid INTEGER NOT NULL,
spatial_index_enabled INTEGER NOT NULL,
CONSTRAINT pk_geom_cols PRIMARY KEY (f_table_name, f_geometry_column),
CONSTRAINT fk_gc_srs FOREIGN KEY (srid) REFERENCES spatial_ref_sys (srid),
CONSTRAINT ck_gc_rtree CHECK (spatial_index_enabled IN (0,1,2)));
CREATE TABLE spatial_ref_sys_aux (
	srid INTEGER NOT NULL PRIMARY KEY,
	is_geographic INTEGER,
	has_flipped_axes INTEGER,
	spheroid TEXT,
	prime_meridian TEXT,
	datum TEXT,
	projection TEXT,
	unit TEXT,
	axis_1_name TEXT,
	axis_1_orientation TEXT,
	axis_2_name TEXT,
	axis_2_orientation TEXT,
	CONSTRAINT fk_sprefsys FOREIGN KEY (srid) 	REFERENCES spatial_ref_sys (srid));
CREATE TABLE views_geometry_columns (
view_name TEXT NOT NULL,
view_geometry TEXT NOT NULL,
view_rowid TEXT NOT NULL,
f_table_name TEXT NOT NULL,
f_geometry_column TEXT NOT NULL,
read_only INTEGER NOT NULL,
CONSTRAINT pk_geom_cols_views PRIMARY KEY (view_name, view_geometry),
CONSTRAINT fk_views_geom_cols FOREIGN KEY (f_table_name, f_geometry_column) REFERENCES geometry_columns (f_table_name, f_geometry_column) ON DELETE CASCADE,
CONSTRAINT ck_vw_rdonly CHECK (read_only IN (0,1)));
CREATE TABLE virts_geometry_columns (
virt_name TEXT NOT NULL,
virt_geometry TEXT NOT NULL,
geometry_type INTEGER NOT NULL,
coord_dimension INTEGER NOT NULL,
srid INTEGER NOT NULL,
CONSTRAINT pk_geom_cols_virts PRIMARY KEY (virt_name, virt_geometry),
CONSTRAINT fk_vgc_srid FOREIGN KEY (srid) REFERENCES spatial_ref_sys (srid));
CREATE TABLE geometry_columns_statistics (
f_table_name TEXT NOT NULL,
f_geometry_column TEXT NOT NULL,
last_verified TIMESTAMP,
row_count INTEGER,
extent_min_x DOUBLE,
extent_min_y DOUBLE,
extent_max_x DOUBLE,
extent_max_y DOUBLE,
CONSTRAINT pk_gc_statistics PRIMARY KEY (f_table_name, f_geometry_column),
CONSTRAINT fk_gc_statistics FOREIGN KEY (f_table_name, f_geometry_column) REFERENCES geometry_columns (f_table_name, f_geometry_column) ON DELETE CASCADE);
CREATE TABLE views_geometry_columns_statistics (
view_name TEXT NOT NULL,
view_geometry TEXT NOT NULL,
last_verified TIMESTAMP,
row_count INTEGER,
extent_min_x DOUBLE,
extent_min_y DOUBLE,
extent_max_x DOUBLE,
extent_max_y DOUBLE,
CONSTRAINT pk_vwgc_statistics PRIMARY KEY (view_name, view_geometry),
CONSTRAINT fk_vwgc_statistics FOREIGN KEY (view_name, view_geometry) REFERENCES views_geometry_columns (view_name, view_geometry) ON DELETE CASCADE);
CREATE TABLE virts_geometry_columns_statistics (
virt_name TEXT NOT NULL,
virt_geometry TEXT NOT NULL,
last_verified TIMESTAMP,
row_count INTEGER,
extent_min_x DOUBLE,
extent_min_y DOUBLE,
extent_max_x DOUBLE,
extent_max_y DOUBLE,
CONSTRAINT pk_vrtgc_statistics PRIMARY KEY (virt_name, virt_geometry),
CONSTRAINT fk_vrtgc_statistics FOREIGN KEY (virt_name, virt_geometry) REFERENCES virts_geometry_columns (virt_name, virt_geometry) ON DELETE CASCADE);
CREATE TABLE geometry_columns_field_infos (
f_table_name TEXT NOT NULL,
f_geometry_column TEXT NOT NULL,
ordinal INTEGER NOT NULL,
column_name TEXT NOT NULL,
null_values INTEGER NOT NULL,
integer_values INTEGER NOT NULL,
double_values INTEGER NOT NULL,
text_values INTEGER NOT NULL,
blob_values INTEGER NOT NULL,
max_size INTEGER,
integer_min INTEGER,
integer_max INTEGER,
double_min DOUBLE,
double_max DOUBLE,
CONSTRAINT pk_gcfld_infos PRIMARY KEY (f_table_name, f_geometry_column, ordinal, column_name),
CONSTRAINT fk_gcfld_infos FOREIGN KEY (f_table_name, f_geometry_column) REFERENCES geometry_columns (f_table_name, f_geometry_column) ON DELETE CASCADE);
CREATE TABLE views_geometry_columns_field_infos (
view_name TEXT NOT NULL,
view_geometry TEXT NOT NULL,
ordinal INTEGER NOT NULL,
column_name TEXT NOT NULL,
null_values INTEGER NOT NULL,
integer_values INTEGER NOT NULL,
double_values INTEGER NOT NULL,
text_values INTEGER NOT NULL,
blob_values INTEGER NOT NULL,
max_size INTEGER,
integer_min INTEGER,
integer_max INTEGER,
double_min DOUBLE,
double_max DOUBLE,
CONSTRAINT pk_vwgcfld_infos PRIMARY KEY (view_name, view_geometry, ordinal, column_name),
CONSTRAINT fk_vwgcfld_infos FOREIGN KEY (view_name, view_geometry) REFERENCES views_geometry_columns (view_name, view_geometry) ON DELETE CASCADE);
CREATE TABLE virts_geometry_columns_field_infos (
virt_name TEXT NOT NULL,
virt_geometry TEXT NOT NULL,
ordinal INTEGER NOT NULL,
column_name TEXT NOT NULL,
null_values INTEGER NOT NULL,
integer_values INTEGER NOT NULL,
double_values INTEGER NOT NULL,
text_values INTEGER NOT NULL,
blob_values INTEGER NOT NULL,
max_size INTEGER,
integer_min INTEGER,
integer_max INTEGER,
double_min DOUBLE,
double_max DOUBLE,
CONSTRAINT pk_vrtgcfld_infos PRIMARY KEY (virt_name, virt_geometry, ordinal, column_name),
CONSTRAINT fk_vrtgcfld_infos FOREIGN KEY (virt_name, virt_geometry) REFERENCES virts_geometry_columns (virt_name, virt_geometry) ON DELETE CASCADE);
CREATE TABLE geometry_columns_time (
f_table_name TEXT NOT NULL,
f_geometry_column TEXT NOT NULL,
last_insert TIMESTAMP NOT NULL DEFAULT '0000-01-01T00:00:00.000Z',
last_update TIMESTAMP NOT NULL DEFAULT '0000-01-01T00:00:00.000Z',
last_delete TIMESTAMP NOT NULL DEFAULT '0000-01-01T00:00:00.000Z',
CONSTRAINT pk_gc_time PRIMARY KEY (f_table_name, f_geometry_column),
CONSTRAINT fk_gc_time FOREIGN KEY (f_table_name, f_geometry_column) REFERENCES geometry_columns (f_table_name, f_geometry_column) ON DELETE CASCADE);
CREATE TABLE geometry_columns_auth (
f_table_name TEXT NOT NULL,
f_geometry_column TEXT NOT NULL,
read_only INTEGER NOT NULL,
hidden INTEGER NOT NULL,
CONSTRAINT pk_gc_auth PRIMARY KEY (f_table_name, f_geometry_column),
CONSTRAINT fk_gc_auth FOREIGN KEY (f_table_name, f_geometry_column) REFERENCES geometry_columns (f_table_name, f_geometry_column) ON DELETE CASCADE,
CONSTRAINT ck_gc_ronly CHECK (read_only IN (0,1)),
CONSTRAINT ck_gc_hidden CHECK (hidden IN (0,1)));
CREATE TABLE views_geometry_columns_auth (
view_name TEXT NOT NULL,
view_geometry TEXT NOT NULL,
hidden INTEGER NOT NULL,
CONSTRAINT pk_vwgc_auth PRIMARY KEY (view_name, view_geometry),
CONSTRAINT fk_vwgc_auth FOREIGN KEY (view_name, view_geometry) REFERENCES views_geometry_columns (view_name, view_geometry) ON DELETE CASCADE,
CONSTRAINT ck_vwgc_hidden CHECK (hidden IN (0,1)));
CREATE TABLE virts_geometry_columns_auth (
virt_name TEXT NOT NULL,
virt_geometry TEXT NOT NULL,
hidden INTEGER NOT NULL,
CONSTRAINT pk_vrtgc_auth PRIMARY KEY (virt_name, virt_geometry),
CONSTRAINT fk_vrtgc_auth FOREIGN KEY (virt_name, virt_geometry) REFERENCES virts_geometry_columns (virt_name, virt_geometry) ON DELETE CASCADE,
CONSTRAINT ck_vrtgc_hidden CHECK (hidden IN (0,1)));
CREATE TABLE sql_statements_log (
id INTEGER PRIMARY KEY AUTOINCREMENT,
time_start TIMESTAMP NOT NULL DEFAULT '0000-01-01T00:00:00.000Z',
time_end TIMESTAMP NOT NULL DEFAULT '0000-01-01T00:00:00.000Z',
user_agent TEXT NOT NULL,
sql_statement TEXT NOT NULL,
success INTEGER NOT NULL DEFAULT 0,
error_cause TEXT NOT NULL DEFAULT 'ABORTED',
CONSTRAINT sqllog_success CHECK (success IN (0,1)));
CREATE VIRTUAL TABLE SpatialIndex USING VirtualSpatialIndex();
CREATE VIRTUAL TABLE ElementaryGeometries USING VirtualElementary();
CREATE VIRTUAL TABLE KNN USING VirtualKNN();
CREATE TABLE Fires (OBJECTID integer primary key autoincrement not null, FOD_ID int32 check((typeof(FOD_ID) = 'integer' or typeof(FOD_ID) = 'null') and FOD_ID >= -2147483648 and FOD_ID <= 2147483647), FPA_ID text(100) check((typeof(FPA_ID) = 'text' or typeof(FPA_ID) = 'null') and not length(FPA_ID) > 100), SOURCE_SYSTEM_TYPE text(255) check((typeof(SOURCE_SYSTEM_TYPE) = 'text' or typeof(SOURCE_SYSTEM_TYPE) = 'null') and not length(SOURCE_SYSTEM_TYPE) > 255), SOURCE_SYSTEM text(30) check((typeof(SOURCE_SYSTEM) = 'text' or typeof(SOURCE_SYSTEM) = 'null') and not length(SOURCE_SYSTEM) > 30), NWCG_REPORTING_AGENCY text(255) check((typeof(NWCG_REPORTING_AGENCY) = 'text' or typeof(NWCG_REPORTING_AGENCY) = 'null') and not length(NWCG_REPORTING_AGENCY) > 255), NWCG_REPORTING_UNIT_ID text(255) check((typeof(NWCG_REPORTING_UNIT_ID) = 'text' or typeof(NWCG_REPORTING_UNIT_ID) = 'null') and not length(NWCG_REPORTING_UNIT_ID) > 255), NWCG_REPORTING_UNIT_NAME text(255) check((typeof(NWCG_REPORTING_UNIT_NAME) = 'text' or typeof(NWCG_REPORTING_UNIT_NAME) = 'null') and not length(NWCG_REPORTING_UNIT_NAME) > 255), SOURCE_REPORTING_UNIT text(30) check((typeof(SOURCE_REPORTING_UNIT) = 'text' or typeof(SOURCE_REPORTING_UNIT) = 'null') and not length(SOURCE_REPORTING_UNIT) > 30), SOURCE_REPORTING_UNIT_NAME text(255) check((typeof(SOURCE_REPORTING_UNIT_NAME) = 'text' or typeof(SOURCE_REPORTING_UNIT_NAME) = 'null') and not length(SOURCE_REPORTING_UNIT_NAME) > 255), LOCAL_FIRE_REPORT_ID text(255) check((typeof(LOCAL_FIRE_REPORT_ID) = 'text' or typeof(LOCAL_FIRE_REPORT_ID) = 'null') and not length(LOCAL_FIRE_REPORT_ID) > 255), LOCAL_INCIDENT_ID text(255) check((typeof(LOCAL_INCIDENT_ID) = 'text' or typeof(LOCAL_INCIDENT_ID) = 'null') and not length(LOCAL_INCIDENT_ID) > 255), FIRE_CODE text(10) check((typeof(FIRE_CODE) = 'text' or typeof(FIRE_CODE) = 'null') and not length(FIRE_CODE) > 10), FIRE_NAME text(255) check((typeof(FIRE_NAME) = 'text' or typeof(FIRE_NAME) = 'null') and not length(FIRE_NAME) > 255), ICS_209_INCIDENT_NUMBER text(255) check((typeof(ICS_209_INCIDENT_NUMBER) = 'text' or typeof(ICS_209_INCIDENT_NUMBER) = 'null') and not length(ICS_209_INCIDENT_NUMBER) > 255), ICS_209_NAME text(255) check((typeof(ICS_209_NAME) = 'text' or typeof(ICS_209_NAME) = 'null') and not length(ICS_209_NAME) > 255), MTBS_ID text(255) check((typeof(MTBS_ID) = 'text' or typeof(MTBS_ID) = 'null') and not length(MTBS_ID) > 255), MTBS_FIRE_NAME text(50) check((typeof(MTBS_FIRE_NAME) = 'text' or typeof(MTBS_FIRE_NAME) = 'null') and not length(MTBS_FIRE_NAME) > 50), COMPLEX_NAME text(255) check((typeof(COMPLEX_NAME) = 'text' or typeof(COMPLEX_NAME) = 'null') and not length(COMPLEX_NAME) > 255), FIRE_YEAR int16 check((typeof(FIRE_YEAR) = 'integer' or typeof(FIRE_YEAR) = 'null') and FIRE_YEAR >= -32768 and FIRE_YEAR <= 32767), DISCOVERY_DATE realdate check((typeof(DISCOVERY_DATE) = 'real' or typeof(DISCOVERY_DATE) = 'null') and DISCOVERY_DATE >= 0.0), DISCOVERY_DOY int32 check((typeof(DISCOVERY_DOY) = 'integer' or typeof(DISCOVERY_DOY) = 'null') and DISCOVERY_DOY >= -2147483648 and DISCOVERY_DOY <= 2147483647), DISCOVERY_TIME text(4) check((typeof(DISCOVERY_TIME) = 'text' or typeof(DISCOVERY_TIME) = 'null') and not length(DISCOVERY_TIME) > 4), STAT_CAUSE_CODE float64 check(typeof(STAT_CAUSE_CODE) = 'real' or typeof(STAT_CAUSE_CODE) = 'null'), STAT_CAUSE_DESCR text(100) check((typeof(STAT_CAUSE_DESCR) = 'text' or typeof(STAT_CAUSE_DESCR) = 'null') and not length(STAT_CAUSE_DESCR) > 100), CONT_DATE realdate check((typeof(CONT_DATE) = 'real' or typeof(CONT_DATE) = 'null') and CONT_DATE >= 0.0), CONT_DOY int32 check((typeof(CONT_DOY) = 'integer' or typeof(CONT_DOY) = 'null') and CONT_DOY >= -2147483648 and CONT_DOY <= 2147483647), CONT_TIME text(4) check((typeof(CONT_TIME) = 'text' or typeof(CONT_TIME) = 'null') and not length(CONT_TIME) > 4), FIRE_SIZE float64 check(typeof(FIRE_SIZE) = 'real' or typeof(FIRE_SIZE) = 'null'), FIRE_SIZE_CLASS text(1) check((typeof(FIRE_SIZE_CLASS) = 'text' or typeof(FIRE_SIZE_CLASS) = 'null') and not length(FIRE_SIZE_CLASS) > 1), LATITUDE float64 check(typeof(LATITUDE) = 'real' or typeof(LATITUDE) = 'null'), LONGITUDE float64 check(typeof(LONGITUDE) = 'real' or typeof(LONGITUDE) = 'null'), OWNER_CODE float64 check(typeof(OWNER_CODE) = 'real' or typeof(OWNER_CODE) = 'null'), OWNER_DESCR text(100) check((typeof(OWNER_DESCR) = 'text' or typeof(OWNER_DESCR) = 'null') and not length(OWNER_DESCR) > 100), STATE text(255) check((typeof(STATE) = 'text' or typeof(STATE) = 'null') and not length(STATE) > 255), COUNTY text(255) check((typeof(COUNTY) = 'text' or typeof(COUNTY) = 'null') and not length(COUNTY) > 255), FIPS_CODE text(255) check((typeof(FIPS_CODE) = 'text' or typeof(FIPS_CODE) = 'null') and not length(FIPS_CODE) > 255), FIPS_NAME text(255) check((typeof(FIPS_NAME) = 'text' or typeof(FIPS_NAME) = 'null') and not length(FIPS_NAME) > 255), Shape POINT not null);
CREATE VIRTUAL TABLE "idx_Fires_Shape" USING rtree(pkid, xmin, xmax, ymin, ymax);
CREATE TABLE "idx_Fires_Shape_node"(nodeno INTEGER PRIMARY KEY, data BLOB);
CREATE TABLE "idx_Fires_Shape_rowid"(rowid INTEGER PRIMARY KEY, nodeno INTEGER);
CREATE TABLE "idx_Fires_Shape_parent"(nodeno INTEGER PRIMARY KEY, parentnode INTEGER);
CREATE TABLE NWCG_UnitIDActive_20170109 (OBJECTID integer primary key autoincrement not null, UnitId text(255) check((typeof(UnitId) = 'text' or typeof(UnitId) = 'null') and not length(UnitId) > 255), GeographicArea text(255) check((typeof(GeographicArea) = 'text' or typeof(GeographicArea) = 'null') and not length(GeographicArea) > 255), Gacc text(255) check((typeof(Gacc) = 'text' or typeof(Gacc) = 'null') and not length(Gacc) > 255), WildlandRole text(255) check((typeof(WildlandRole) = 'text' or typeof(WildlandRole) = 'null') and not length(WildlandRole) > 255), UnitType text(255) check((typeof(UnitType) = 'text' or typeof(UnitType) = 'null') and not length(UnitType) > 255), Department text(255) check((typeof(Department) = 'text' or typeof(Department) = 'null') and not length(Department) > 255), Agency text(255) check((typeof(Agency) = 'text' or typeof(Agency) = 'null') and not length(Agency) > 255), Parent text(255) check((typeof(Parent) = 'text' or typeof(Parent) = 'null') and not length(Parent) > 255), Country text(255) check((typeof(Country) = 'text' or typeof(Country) = 'null') and not length(Country) > 255), State text(255) check((typeof(State) = 'text' or typeof(State) = 'null') and not length(State) > 255), Code text(255) check((typeof(Code) = 'text' or typeof(Code) = 'null') and not length(Code) > 255), Name text(255) check((typeof(Name) = 'text' or typeof(Name) = 'null') and not length(Name) > 255));

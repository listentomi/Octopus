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
CREATE TABLE "buildings_points" (
"PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
"osm_id" TEXT,
"name" TEXT,
"type" TEXT, "Geometry" POINT);
CREATE TABLE "idx_buildings_points_Geometry_node"(nodeno INTEGER PRIMARY KEY, data BLOB);
CREATE TABLE "idx_buildings_points_Geometry_rowid"(rowid INTEGER PRIMARY KEY, nodeno INTEGER);
CREATE TABLE "idx_buildings_points_Geometry_parent"(nodeno INTEGER PRIMARY KEY, parentnode INTEGER);
CREATE TABLE "landuse_polygon" (
"PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
"osm_id" TEXT,
"code" INTEGER,
"fclass" TEXT, "Geometry" MULTIPOLYGON);
CREATE TABLE "idx_landuse_polygon_Geometry_node"(nodeno INTEGER PRIMARY KEY, data BLOB);
CREATE TABLE "idx_landuse_polygon_Geometry_rowid"(rowid INTEGER PRIMARY KEY, nodeno INTEGER);
CREATE TABLE "idx_landuse_polygon_Geometry_parent"(nodeno INTEGER PRIMARY KEY, parentnode INTEGER);
CREATE TABLE "pois_polygon" (
"PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
"osm_id" TEXT,
"code" INTEGER,
"fclass" TEXT,
"name" TEXT, "Geometry" MULTIPOLYGON);
CREATE TABLE "idx_pois_polygon_Geometry_node"(nodeno INTEGER PRIMARY KEY, data BLOB);
CREATE TABLE "idx_pois_polygon_Geometry_rowid"(rowid INTEGER PRIMARY KEY, nodeno INTEGER);
CREATE TABLE "idx_pois_polygon_Geometry_parent"(nodeno INTEGER PRIMARY KEY, parentnode INTEGER);
CREATE TABLE "roads_lines" (
"PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
"osm_id" TEXT,
"code" INTEGER,
"fclass" TEXT,
"name" TEXT,
"ref" TEXT,
"oneway" TEXT,
"maxspeed" INTEGER,
"layer" INTEGER,
"bridge" TEXT,
"tunnel" TEXT, "Geometry" LINESTRING);
CREATE TABLE "idx_roads_lines_Geometry_node"(nodeno INTEGER PRIMARY KEY, data BLOB);
CREATE TABLE "idx_roads_lines_Geometry_rowid"(rowid INTEGER PRIMARY KEY, nodeno INTEGER);
CREATE TABLE "idx_roads_lines_Geometry_parent"(nodeno INTEGER PRIMARY KEY, parentnode INTEGER);
CREATE TABLE "waterways_lines" (
"PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
"osm_id" TEXT,
"code" INTEGER,
"fclass" TEXT,
"width" INTEGER,
"name" TEXT, "Geometry" LINESTRING);
CREATE TABLE "idx_waterways_lines_Geometry_node"(nodeno INTEGER PRIMARY KEY, data BLOB);
CREATE TABLE "idx_waterways_lines_Geometry_rowid"(rowid INTEGER PRIMARY KEY, nodeno INTEGER);
CREATE TABLE "idx_waterways_lines_Geometry_parent"(nodeno INTEGER PRIMARY KEY, parentnode INTEGER);
CREATE TABLE sqlite_stat1(tbl,idx,stat);
CREATE TABLE sqlite_stat3(tbl,idx,neq,nlt,ndlt,sample);
CREATE VIRTUAL TABLE SpatialIndex USING VirtualSpatialIndex();
CREATE VIRTUAL TABLE ElementaryGeometries USING VirtualElementary();
CREATE VIRTUAL TABLE "idx_buildings_points_Geometry" USING rtree(pkid, xmin, xmax, ymin, ymax);
CREATE VIRTUAL TABLE "idx_landuse_polygon_Geometry" USING rtree(pkid, xmin, xmax, ymin, ymax);
CREATE VIRTUAL TABLE "idx_pois_polygon_Geometry" USING rtree(pkid, xmin, xmax, ymin, ymax);
CREATE VIRTUAL TABLE "idx_roads_lines_Geometry" USING rtree(pkid, xmin, xmax, ymin, ymax);
CREATE VIRTUAL TABLE "idx_waterways_lines_Geometry" USING rtree(pkid, xmin, xmax, ymin, ymax);

CREATE TABLE "categories" (
	"CategoryID" INTEGER PRIMARY KEY AUTOINCREMENT,
	"CategoryName" VARCHAR(15) NOT NULL  ,
	"Description" TEXT NULL  ,
	"Picture" BLOB NULL
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE "customercustomerdemo" (
	"CustomerID" VARCHAR(5) NOT NULL  ,
	"CustomerTypeID" VARCHAR(10) NOT NULL  ,
	PRIMARY KEY ("CustomerID", "CustomerTypeID"),
	FOREIGN KEY("CustomerTypeID") REFERENCES "customerdemographics" ("CustomerTypeID") ON UPDATE RESTRICT ON DELETE RESTRICT,
	FOREIGN KEY("CustomerID") REFERENCES "customers" ("CustomerID") ON UPDATE RESTRICT ON DELETE RESTRICT
);
CREATE TABLE "customerdemographics" (
	"CustomerTypeID" VARCHAR(10) NOT NULL  ,
	"CustomerDesc" TEXT NULL  ,
	PRIMARY KEY ("CustomerTypeID")
);
CREATE TABLE "customers" (
	"CustomerID" VARCHAR(5) NOT NULL  ,
	"CompanyName" VARCHAR(40) NOT NULL  ,
	"ContactName" VARCHAR(30) NULL  ,
	"ContactTitle" VARCHAR(30) NULL  ,
	"Address" VARCHAR(60) NULL  ,
	"City" VARCHAR(15) NULL  ,
	"Region" VARCHAR(15) NULL  ,
	"PostalCode" VARCHAR(10) NULL  ,
	"Country" VARCHAR(15) NULL  ,
	"Phone" VARCHAR(24) NULL  ,
	"Fax" VARCHAR(24) NULL  ,
	PRIMARY KEY ("CustomerID")
);
CREATE TABLE "employees" (
	"EmployeeID" INTEGER PRIMARY KEY AUTOINCREMENT,
	"LastName" VARCHAR(20) NOT NULL  ,
	"FirstName" VARCHAR(10) NOT NULL  ,
	"Title" VARCHAR(30) NULL  ,
	"TitleOfCourtesy" VARCHAR(25) NULL  ,
	"BirthDate" DATETIME NULL  ,
	"HireDate" DATETIME NULL  ,
	"Address" VARCHAR(60) NULL  ,
	"City" VARCHAR(15) NULL  ,
	"Region" VARCHAR(15) NULL  ,
	"PostalCode" VARCHAR(10) NULL  ,
	"Country" VARCHAR(15) NULL  ,
	"HomePhone" VARCHAR(24) NULL  ,
	"Extension" VARCHAR(4) NULL  ,
	"Photo" BLOB NULL  ,
	"Notes" TEXT NOT NULL  ,
	"ReportsTo" INTEGER NULL  ,
	"PhotoPath" VARCHAR(255) NULL  ,
	"Salary" FLOAT NULL,
	FOREIGN KEY("ReportsTo") REFERENCES "employees" ("EmployeeID") ON UPDATE RESTRICT ON DELETE RESTRICT
);
CREATE TABLE "employeeterritories" (
	"EmployeeID" INTEGER NOT NULL  ,
	"TerritoryID" VARCHAR(20) NOT NULL  ,
	PRIMARY KEY ("EmployeeID", "TerritoryID"),
	FOREIGN KEY("EmployeeID") REFERENCES "employees" ("EmployeeID") ON UPDATE RESTRICT ON DELETE RESTRICT,
	FOREIGN KEY("TerritoryID") REFERENCES "territories" ("TerritoryID") ON UPDATE RESTRICT ON DELETE RESTRICT
);
CREATE TABLE "order details" (
	"OrderID" INTEGER NOT NULL  ,
	"ProductID" INTEGER NOT NULL  ,
	"UnitPrice" DECIMAL NOT NULL DEFAULT '0.0000' ,
	"Quantity" SMALLINT NOT NULL DEFAULT '1' ,
	"Discount" DOUBLE NOT NULL DEFAULT '0' ,
	PRIMARY KEY ("OrderID", "ProductID"),
	FOREIGN KEY("OrderID") REFERENCES "orders" ("OrderID") ON UPDATE RESTRICT ON DELETE RESTRICT,
	FOREIGN KEY("ProductID") REFERENCES "products" ("ProductID") ON UPDATE RESTRICT ON DELETE RESTRICT
);
CREATE TABLE "orders" (
	"OrderID" INTEGER PRIMARY KEY AUTOINCREMENT,
	"CustomerID" VARCHAR(5) NULL  ,
	"EmployeeID" INTEGER NULL  ,
	"OrderDate" DATETIME NULL  ,
	"RequiredDate" DATETIME NULL  ,
	"ShippedDate" DATETIME NULL  ,
	"ShipVia" INTEGER NULL  ,
	"Freight" DECIMAL NULL DEFAULT '0.0000' ,
	"ShipName" VARCHAR(40) NULL  ,
	"ShipAddress" VARCHAR(60) NULL  ,
	"ShipCity" VARCHAR(15) NULL  ,
	"ShipRegion" VARCHAR(15) NULL  ,
	"ShipPostalCode" VARCHAR(10) NULL  ,
	"ShipCountry" VARCHAR(15) NULL,
	FOREIGN KEY("CustomerID") REFERENCES "customers" ("CustomerID") ON UPDATE RESTRICT ON DELETE RESTRICT,
	FOREIGN KEY("EmployeeID") REFERENCES "employees" ("EmployeeID") ON UPDATE RESTRICT ON DELETE RESTRICT,
	FOREIGN KEY("ShipVia") REFERENCES "shippers" ("ShipperID") ON UPDATE RESTRICT ON DELETE RESTRICT
);
CREATE TABLE "products" (
	"ProductID" INTEGER PRIMARY KEY AUTOINCREMENT,
	"ProductName" VARCHAR(40) NOT NULL  ,
	"SupplierID" INTEGER NULL  ,
	"CategoryID" INTEGER NULL  ,
	"QuantityPerUnit" VARCHAR(20) NULL  ,
	"UnitPrice" DECIMAL NULL DEFAULT '0.0000' ,
	"UnitsInStock" SMALLINT NULL DEFAULT '0' ,
	"UnitsOnOrder" SMALLINT NULL DEFAULT '0' ,
	"ReorderLevel" SMALLINT NULL DEFAULT '0' ,
	"Discontinued" TINYINT NOT NULL,
	FOREIGN KEY("CategoryID") REFERENCES "categories" ("CategoryID") ON UPDATE RESTRICT ON DELETE RESTRICT,
	FOREIGN KEY("SupplierID") REFERENCES "suppliers" ("SupplierID") ON UPDATE RESTRICT ON DELETE RESTRICT
);
CREATE TABLE "region" (
	"RegionID" INTEGER NOT NULL  ,
	"RegionDescription" VARCHAR(50) NOT NULL  ,
	PRIMARY KEY ("RegionID")
);
CREATE TABLE "shippers" (
	"ShipperID" INTEGER PRIMARY KEY AUTOINCREMENT,
	"CompanyName" VARCHAR(40) NOT NULL  ,
	"Phone" VARCHAR(24) NULL
);
CREATE TABLE "suppliers" (
	"SupplierID" INTEGER PRIMARY KEY AUTOINCREMENT,
	"CompanyName" VARCHAR(40) NOT NULL  ,
	"ContactName" VARCHAR(30) NULL  ,
	"ContactTitle" VARCHAR(30) NULL  ,
	"Address" VARCHAR(60) NULL  ,
	"City" VARCHAR(15) NULL  ,
	"Region" VARCHAR(15) NULL  ,
	"PostalCode" VARCHAR(10) NULL  ,
	"Country" VARCHAR(15) NULL  ,
	"Phone" VARCHAR(24) NULL  ,
	"Fax" VARCHAR(24) NULL  ,
	"HomePage" TEXT NULL
);
CREATE TABLE "territories" (
	"TerritoryID" VARCHAR(20) NOT NULL  ,
	"TerritoryDescription" VARCHAR(50) NOT NULL  ,
	"RegionID" INTEGER NOT NULL  ,
	PRIMARY KEY ("TerritoryID"),
	FOREIGN KEY("RegionID") REFERENCES "region" ("RegionID") ON UPDATE RESTRICT ON DELETE RESTRICT
);

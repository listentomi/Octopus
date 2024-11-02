CREATE TABLE "customers" (
	"customerNumber" INTEGER NOT NULL  ,
	"customerName" VARCHAR(50) NOT NULL  ,
	"contactLastName" VARCHAR(50) NOT NULL  ,
	"contactFirstName" VARCHAR(50) NOT NULL  ,
	"phone" VARCHAR(50) NOT NULL  ,
	"addressLine1" VARCHAR(50) NOT NULL  ,
	"addressLine2" VARCHAR(50) NULL  ,
	"city" VARCHAR(50) NOT NULL  ,
	"state" VARCHAR(50) NULL  ,
	"postalCode" VARCHAR(15) NULL  ,
	"country" VARCHAR(50) NOT NULL  ,
	"salesRepEmployeeNumber" INTEGER NULL  ,
	"creditLimit" DOUBLE NULL  ,
	PRIMARY KEY ("customerNumber"),
	FOREIGN KEY("salesRepEmployeeNumber") REFERENCES "employees" ("employeeNumber") ON UPDATE RESTRICT ON DELETE RESTRICT
);
CREATE TABLE "employees" (
	"employeeNumber" INTEGER NOT NULL  ,
	"lastName" VARCHAR(50) NOT NULL  ,
	"firstName" VARCHAR(50) NOT NULL  ,
	"extension" VARCHAR(10) NOT NULL  ,
	"email" VARCHAR(100) NOT NULL  ,
	"officeCode" VARCHAR(10) NOT NULL  ,
	"reportsTo" INTEGER NULL  ,
	"jobTitle" VARCHAR(50) NOT NULL  ,
	PRIMARY KEY ("employeeNumber"),
	FOREIGN KEY("reportsTo") REFERENCES "employees" ("employeeNumber") ON UPDATE RESTRICT ON DELETE RESTRICT,
	FOREIGN KEY("officeCode") REFERENCES "offices" ("officeCode") ON UPDATE RESTRICT ON DELETE RESTRICT
);
CREATE TABLE "offices" (
	"officeCode" VARCHAR(10) NOT NULL  ,
	"city" VARCHAR(50) NOT NULL  ,
	"phone" VARCHAR(50) NOT NULL  ,
	"addressLine1" VARCHAR(50) NOT NULL  ,
	"addressLine2" VARCHAR(50) NULL  ,
	"state" VARCHAR(50) NULL  ,
	"country" VARCHAR(50) NOT NULL  ,
	"postalCode" VARCHAR(15) NOT NULL  ,
	"territory" VARCHAR(10) NOT NULL  ,
	PRIMARY KEY ("officeCode")
);
CREATE TABLE "orderdetails" (
	"orderNumber" INTEGER NOT NULL  ,
	"productCode" VARCHAR(15) NOT NULL  ,
	"quantityOrdered" INTEGER NOT NULL  ,
	"priceEach" DOUBLE NOT NULL  ,
	"orderLineNumber" SMALLINT NOT NULL  ,
	PRIMARY KEY ("orderNumber", "productCode"),
	FOREIGN KEY("orderNumber") REFERENCES "orders" ("orderNumber") ON UPDATE RESTRICT ON DELETE RESTRICT,
	FOREIGN KEY("productCode") REFERENCES "products" ("productCode") ON UPDATE RESTRICT ON DELETE RESTRICT
);
CREATE TABLE "orders" (
	"orderNumber" INTEGER NOT NULL  ,
	"orderDate" DATE NOT NULL  ,
	"requiredDate" DATE NOT NULL  ,
	"shippedDate" DATE NULL  ,
	"status" VARCHAR(15) NOT NULL  ,
	"comments" TEXT NULL  ,
	"customerNumber" INTEGER NOT NULL  ,
	PRIMARY KEY ("orderNumber"),
	FOREIGN KEY("customerNumber") REFERENCES "customers" ("customerNumber") ON UPDATE RESTRICT ON DELETE RESTRICT
);
CREATE TABLE "payments" (
	"customerNumber" INTEGER NOT NULL  ,
	"checkNumber" VARCHAR(50) NOT NULL  ,
	"paymentDate" DATE NOT NULL  ,
	"amount" DOUBLE NOT NULL  ,
	PRIMARY KEY ("customerNumber", "checkNumber"),
	FOREIGN KEY("customerNumber") REFERENCES "customers" ("customerNumber") ON UPDATE RESTRICT ON DELETE RESTRICT
);
CREATE TABLE "productlines" (
	"productLine" VARCHAR(50) NOT NULL  ,
	"textDescription" VARCHAR(4000) NULL  ,
	"htmlDescription" TEXT NULL  ,
	"image" BLOB NULL  ,
	PRIMARY KEY ("productLine")
);
CREATE TABLE "products" (
	"productCode" VARCHAR(15) NOT NULL  ,
	"productName" VARCHAR(70) NOT NULL  ,
	"productLine" VARCHAR(50) NOT NULL  ,
	"productScale" VARCHAR(10) NOT NULL  ,
	"productVendor" VARCHAR(50) NOT NULL  ,
	"productDescription" TEXT NOT NULL  ,
	"quantityInStock" SMALLINT NOT NULL  ,
	"buyPrice" DOUBLE NOT NULL  ,
	"MSRP" DOUBLE NOT NULL  ,
	PRIMARY KEY ("productCode"),
	FOREIGN KEY("productLine") REFERENCES "productlines" ("productLine") ON UPDATE RESTRICT ON DELETE RESTRICT
);


/*
 ----------------------------------------------------------------------------
 File name: db/init/001_schema.sql
 Bookstore Demo DB Tables and Data Objects for MariaDB/MySQL

 Requires:
 - MariaDB 10.2.1+ OR MySQL 8.0.13+
   (uses DEFAULT (UUID()) and CURRENT_TIMESTAMP(6))

 (C) Copyright Panos Zafeiropoulos - 2022-26

 -----------------------------------------------------------------------------
 Updates:
         260213: Tables:     3
                 Triggers:   0
                 Procedures: 0
                 Triggers:   0
                 Views:      0
 ----------------------------------------------------------------------------
 Last update: 260213
 ----------------------------------------------------------------------------


Important reminder:
--------------------
When MariaDB initializes for the first time, it executes:
001_schema.sql
002_seed.sql

Seed scripts in /docker-entrypoint-initdb.d run only when mariadb_data volume is empty
If you already started MariaDB once:

First, stop and remove the containers, network(s) and the volume(s) created by docker compose up:
docker compose --profile app1 --profile app2 --profile app3 down --volumes
Then, start the MariaDB container again:
docker compose --profile app1 --profile app2 --profile app3 up -d

Thi is required to re-run init scripts.

*/

-- --------------------------------------------------------
-- CREATE DATABASE bookstore1
-- --------------------------------------------------------
CREATE DATABASE IF NOT EXISTS bookstore1
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE bookstore1;

-- --------------------------------------------------------
-- Table: categories
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS categories (
  categoryId           INT UNSIGNED NOT NULL AUTO_INCREMENT,
  categoryName         VARCHAR(100) NOT NULL,
  categoryStatusId     SMALLINT UNSIGNED NOT NULL DEFAULT 1,
  categoryCrUUID       CHAR(36) NOT NULL DEFAULT (UUID()),
  categoryCrTimestamp  TIMESTAMP(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  categoryClientUUID   VARCHAR(40) NULL,
  PRIMARY KEY (categoryId),
  UNIQUE KEY uq_categories_name (categoryName)
) ENGINE=InnoDB;

-- --------------------------------------------------------
-- Table: items
-- (many-to-many: no category id here)
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS items (
  itemId           INT UNSIGNED NOT NULL AUTO_INCREMENT,
  itemName         VARCHAR(100) NOT NULL,
  itemListPrice    DECIMAL(10,2) NOT NULL,
  itemModelYear    SMALLINT UNSIGNED NULL,
  itemStatusId     SMALLINT UNSIGNED NOT NULL DEFAULT 1,
  itemCrUUID       CHAR(36) NOT NULL DEFAULT (UUID()),
  itemCrTimestamp  TIMESTAMP(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  itemClientUUID   VARCHAR(40) NULL,
  PRIMARY KEY (itemId),
  KEY ix_items_name (itemName)
) ENGINE=InnoDB;

-- --------------------------------------------------------
-- Table: categoryitems (junction table)
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS categoryitems (
  categoryitemId           INT UNSIGNED NOT NULL AUTO_INCREMENT,
  categoryitemCategoryId   INT UNSIGNED NOT NULL,
  categoryitemItemId       INT UNSIGNED NOT NULL,
  categoryitemCrUUID       CHAR(36) NOT NULL DEFAULT (UUID()),
  categoryitemCrTimestamp  TIMESTAMP(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  categoryitemClientUUID   VARCHAR(40) NULL,
  PRIMARY KEY (categoryitemId),

  -- Prevent duplicates like (category=5,item=10) appearing twice
  UNIQUE KEY uq_categoryitems_pair (categoryitemCategoryId, categoryitemItemId),

  -- Helpful indexes for joins
  KEY ix_categoryitems_categoryId (categoryitemCategoryId),
  KEY ix_categoryitems_itemId (categoryitemItemId),

  CONSTRAINT fk_categoryitems_category
    FOREIGN KEY (categoryitemCategoryId)
    REFERENCES categories(categoryId)
    ON UPDATE CASCADE
    ON DELETE CASCADE,

  CONSTRAINT fk_categoryitems_item
    FOREIGN KEY (categoryitemItemId)
    REFERENCES items(itemId)
    ON UPDATE CASCADE
    ON DELETE CASCADE
) ENGINE=InnoDB;

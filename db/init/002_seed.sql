/*
 ----------------------------------------------------------------------------
 File name: db/init/002_seed.sql
 Bookstore Demo DB Tables and Data Objects for MariaDB/MySQL


 -----------------------------------------------------------------------------
 Updates:
         260213: Initial entries
                 Categories: 7
                 Items: 20
                 Many-to-many relationships via categoryitems
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
-- ADD RECORDS TO TABLES
-- --------------------------------------------------------


USE bookstore1;

-- --------------------------------------------------------
-- Insert Categories
-- --------------------------------------------------------
INSERT INTO categories (categoryName) VALUES
('Fiction'),
('Science'),
('Technology'),
('History'),
('Business'),
('Philosophy'),
('Education');

-- --------------------------------------------------------
-- Insert Items (20 entries)
-- --------------------------------------------------------
INSERT INTO items (itemName, itemListPrice, itemModelYear) VALUES
('The Quantum World', 29.90, 2022),
('Python Backend Essentials', 45.00, 2024),
('World War II Atlas', 39.50, 2020),
('Modern Sci-Fi Stories', 22.00, 2023),
('AI Fundamentals', 49.00, 2023),
('Deep Learning Explained', 55.00, 2021),
('Startup Strategy', 27.50, 2022),
('Lean Business Models', 31.20, 2019),
('Ancient Philosophy Reader', 24.00, 2018),
('Ethics in Technology', 28.90, 2024),
('Database Design Mastery', 42.00, 2023),
('Docker in Practice', 36.00, 2022),
('Distributed Systems Guide', 47.80, 2024),
('Physics for Everyone', 18.50, 2017),
('Educational Psychology', 26.00, 2021),
('Teaching Programming', 33.00, 2020),
('Cybersecurity Basics', 40.00, 2023),
('Historical Maps Collection', 30.00, 2016),
('Science Fiction Classics', 21.50, 2015),
('The Logic Handbook', 19.90, 2014);

-- --------------------------------------------------------
-- Many-to-many relations
-- --------------------------------------------------------

-- Science
INSERT INTO categoryitems (categoryitemCategoryId, categoryitemItemId)
SELECT c.categoryId, i.itemId FROM categories c JOIN items i
WHERE c.categoryName='Science' AND i.itemName IN (
'The Quantum World','Physics for Everyone','Deep Learning Explained'
);

-- Technology
INSERT INTO categoryitems (categoryitemCategoryId, categoryitemItemId)
SELECT c.categoryId, i.itemId FROM categories c JOIN items i
WHERE c.categoryName='Technology' AND i.itemName IN (
'Python Backend Essentials','AI Fundamentals','Database Design Mastery',
'Docker in Practice','Distributed Systems Guide','Cybersecurity Basics',
'Ethics in Technology'
);

-- History
INSERT INTO categoryitems (categoryitemCategoryId, categoryitemItemId)
SELECT c.categoryId, i.itemId FROM categories c JOIN items i
WHERE c.categoryName='History' AND i.itemName IN (
'World War II Atlas','Historical Maps Collection'
);

-- Fiction
INSERT INTO categoryitems (categoryitemCategoryId, categoryitemItemId)
SELECT c.categoryId, i.itemId FROM categories c JOIN items i
WHERE c.categoryName='Fiction' AND i.itemName IN (
'Modern Sci-Fi Stories','Science Fiction Classics'
);

-- Business
INSERT INTO categoryitems (categoryitemCategoryId, categoryitemItemId)
SELECT c.categoryId, i.itemId FROM categories c JOIN items i
WHERE c.categoryName='Business' AND i.itemName IN (
'Startup Strategy','Lean Business Models'
);

-- Philosophy
INSERT INTO categoryitems (categoryitemCategoryId, categoryitemItemId)
SELECT c.categoryId, i.itemId FROM categories c JOIN items i
WHERE c.categoryName='Philosophy' AND i.itemName IN (
'Ancient Philosophy Reader','The Logic Handbook','Ethics in Technology'
);

-- Education
INSERT INTO categoryitems (categoryitemCategoryId, categoryitemItemId)
SELECT c.categoryId, i.itemId FROM categories c JOIN items i
WHERE c.categoryName='Education' AND i.itemName IN (
'Educational Psychology','Teaching Programming'
);

-- --------------------------------------------------------
-- Example cross-category assignments (true many-to-many)
-- --------------------------------------------------------

-- Modern Sci-Fi Stories belongs also to Technology
INSERT INTO categoryitems (categoryitemCategoryId, categoryitemItemId)
SELECT c.categoryId, i.itemId
FROM categories c JOIN items i
WHERE c.categoryName='Technology' AND i.itemName='Modern Sci-Fi Stories';

-- AI Fundamentals belongs also to Science
INSERT INTO categoryitems (categoryitemCategoryId, categoryitemItemId)
SELECT c.categoryId, i.itemId
FROM categories c JOIN items i
WHERE c.categoryName='Science' AND i.itemName='AI Fundamentals';



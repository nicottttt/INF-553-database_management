--Chuhao Tang, Alex Quach

CREATE DATABASE pubmed2
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    -- LC_COLLATE = 'Chinese (Simplified)_China.936'
    -- LC_CTYPE = 'Chinese (Simplified)_China.936'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

\connect pubmed2;

CREATE TABLE pubmed_article (
    article_id INT PRIMARY KEY,
    title VARCHAR(8046) NOT NULL,
    journal_title VARCHAR(8046) NOT NULL,
    doi VARCHAR(8046) NOT NULL,
    pubmed_link VARCHAR(8046) NOT NULL,
    year INT NOT NULL
);

CREATE TABLE pubmed_affiliation (
    affl_id INT PRIMARY KEY,
    norm_affl VARCHAR(8046) NOT NULL
);

CREATE TABLE pubmed_author (
    author_id INT PRIMARY KEY,
    author_name VARCHAR(8046) NOT NULL,
    affl_id INT,
    FOREIGN KEY (affl_id) REFERENCES pubmed_affiliation(affl_id)
);

CREATE TABLE article_author (
    article_id INT,
    author_id INT,
    PRIMARY KEY (article_id, author_id),
    FOREIGN KEY (article_id) REFERENCES pubmed_article(article_id),
    FOREIGN KEY (author_id) REFERENCES pubmed_author(author_id)
);

CREATE TABLE grant_info (
    grant_id INT PRIMARY KEY,
    grant_val VARCHAR(8046) NOT NULL
);

CREATE TABLE article_grant (
    article_id INT,
    grant_id INT,
    PRIMARY KEY (article_id, grant_id),
    FOREIGN KEY (article_id) REFERENCES pubmed_article(article_id),
    FOREIGN KEY (grant_id) REFERENCES grant_info(grant_id)
);

CREATE TABLE article_coi (
    article_id INT,
    coi_id INT PRIMARY KEY,
    coi_text TEXT,
    FOREIGN KEY (article_id) REFERENCES pubmed_article(article_id)
);


\COPY pubmed_article FROM 'PUBMED_DATA\PUBMED_DATA\pubmed_article.csv' DELIMITER ',' CSV HEADER ENCODING 'UTF8';
\COPY pubmed_affiliation FROM 'PUBMED_DATA\PUBMED_DATA\pubmed_affiliation.csv' DELIMITER ',' CSV HEADER ENCODING 'UTF8';
\COPY pubmed_author FROM 'PUBMED_DATA\PUBMED_DATA\pubmed_author.csv' DELIMITER ',' CSV HEADER ENCODING 'UTF8';
\COPY article_author FROM 'PUBMED_DATA\PUBMED_DATA\article_author.csv' DELIMITER ',' CSV HEADER ENCODING 'UTF8';
\COPY grant_info FROM 'PUBMED_DATA\PUBMED_DATA\grant_info.csv' DELIMITER ',' CSV HEADER ENCODING 'UTF8';
\COPY article_grant FROM 'PUBMED_DATA\PUBMED_DATA\article_grant.csv' DELIMITER ',' CSV HEADER ENCODING 'UTF8';
\COPY article_coi FROM 'PUBMED_DATA\PUBMED_DATA\article_coi.csv' DELIMITER ',' CSV HEADER ENCODING 'UTF8';

-- .\schemacrawler.cmd    --server=postgresql    --user=postgres  --password=242401  --database=pubmed    --command=schema --info-level=standard    --portable-names    --output-format=png    --output-file=schema.png
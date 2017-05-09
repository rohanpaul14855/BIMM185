--Creates tables for Week 4/5 exercises
--Call using source makeGenomes.sql in SQL command prompt

CREATE TABLE genomes (
  genome_id  INT      (10) UNSIGNED NOT NULL AUTO_INCREMENT,
  tax_id     INT      (10) UNSIGNED NOT NULL,
  shortname  VARCHAR (100),
  longname   VARCHAR (200),
  length     INT (15) NOT NULL,
  domain     ENUM("bacteria","archaea","eukarya") NOT NULL,
  genbank_accesion  VARCHAR(15),
  PRIMARY KEY (genome_id),
  KEY (tax_id)
) ENGINE=InnoDB;


CREATE TABLE replicons (
  replicon_id  INT  (10) UNSIGNED NOT NULL,
  genome_id  INT  (10) UNSIGNED NOT NULL,
  name VARCHAR  (100),
  num_genes  INT  (15),
  replicon_type  ENUM("chromosome","plasmid"),
  replicon_structure  ENUM("linear","circular"),
  PRIMARY KEY (replicon_id),
  KEY (genome_id)
) ENGINE=InnoDB;


CREATE TABLE genes (
  gene_id  INT  (10) UNSIGNED NOT NULL,
  genome_id  INT  (10) UNSIGNED NOT NULL AUTO_INCREMENT,
  replicon_id  INT  (10) UNSIGNED NOT NULL,
  locus_tag  VARCHAR  (25) NOT NULL,
  name  VARCHAR (100),
  strand  ENUM("+", "-") NOT NULL,
  num_exons  INT (15) NOT NULL,
  length  INT (15) NOT NULL,
  product_name  VARCHAR (100),
  PRIMARY KEY  (gene_id),
  KEY  (genome_id),
  KEY  (replicon_id)
) ENGINE=InnoDB;


CREATE TABLE exons (
  gene_id  INT (10) UNSIGNED NOT NULL,
  exon  INT (10),
  start_pos  INT (10),
  end_pos  INT (10),
  length  INT (10),
  KEY  (gene_id)
) ENGINE=InnoDB;


CREATE TABLE gene_synonyms (
  gene_id  INT  (10) UNSIGNED NOT NULL,
  synonyms  VARCHAR  (50),
  KEY  (gene_id)
) ENGINE=InnoDB;

CREATE TABLE externalrefs (
  gene_id  INT (10) UNSIGNED NOT NULL,
  externaldb  VARCHAR (50),
  externalID  VARCHAR (50),
  KEY (gene_id)
) ENGINE=InnoDB;

CREATE TABLE functions (
  gene_id  INT  (10) UNSIGNED NOT NULL,
  fn  VARCHAR  (50) NOT NULL,
  KEY (gene_id)
) ENGINE=InnoDB; 

*/

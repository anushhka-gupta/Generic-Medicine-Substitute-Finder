CREATE TABLE medicines (
    id                  INT PRIMARY KEY AUTO_INCREMENT,
    name                VARCHAR(255) NOT NULL,
    price               DECIMAL(12,2),
    is_discontinued     BOOLEAN NOT NULL DEFAULT FALSE,
    manufacturer_name   VARCHAR(255),
    type                VARCHAR(100),
    pack_size_label     VARCHAR(100),
    short_composition1  VARCHAR(255),
    short_composition2  VARCHAR(255)
);

CREATE TABLE accounts (
    id VARCHAR(36) PRIMARY KEY, name VARCHAR(80) NOT NULL, email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(100) NOT NULL, role VARCHAR(30) NOT NULL,
    organization VARCHAR(100) NOT NULL, area VARCHAR(80) NOT NULL
);
CREATE TABLE donations (
    id VARCHAR(36) PRIMARY KEY, name VARCHAR(100) NOT NULL, category VARCHAR(30) NOT NULL,
    description VARCHAR(2000) NOT NULL, quantity INTEGER NOT NULL CHECK (quantity > 0), unit VARCHAR(30) NOT NULL,
    location VARCHAR(250) NOT NULL, area VARCHAR(80) NOT NULL, distance DOUBLE NOT NULL,
    prepared_at TIMESTAMP(6) NOT NULL, deadline TIMESTAMP(6) NOT NULL, image LONGTEXT NOT NULL,
    donor VARCHAR(100) NOT NULL, dietary VARCHAR(250) NOT NULL, allergens VARCHAR(250) NOT NULL,
    owner_id VARCHAR(36) NOT NULL, claimed BOOLEAN NOT NULL, created_at TIMESTAMP(6) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES accounts(id)
);
CREATE INDEX idx_donations_available ON donations(claimed, deadline);
CREATE TABLE pickups (
    id VARCHAR(36) PRIMARY KEY, donation_id VARCHAR(36) NOT NULL UNIQUE,
    recipient_id VARCHAR(36) NOT NULL, volunteer_id VARCHAR(36), stage INTEGER NOT NULL CHECK (stage BETWEEN 1 AND 4),
    created_at TIMESTAMP(6) NOT NULL,
    FOREIGN KEY (donation_id) REFERENCES donations(id), FOREIGN KEY (recipient_id) REFERENCES accounts(id),
    FOREIGN KEY (volunteer_id) REFERENCES accounts(id)
);
CREATE TABLE pickup_timestamps (
    pickup_id VARCHAR(36) NOT NULL, stage_index INTEGER NOT NULL, occurred_at TIMESTAMP(6) NOT NULL,
    PRIMARY KEY (pickup_id, stage_index), FOREIGN KEY (pickup_id) REFERENCES pickups(id)
);


# SQL queries
CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS pcs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    price DECIMAL(10, 2),
    ref VARCHAR(255),
    name VARCHAR(255),
    description TEXT,
    availability VARCHAR(50)
);
"""

INSERT_QUERY = """
INSERT INTO pcs (price, ref, name, description, availability)
VALUES (%s, %s, %s, %s, %s)
"""

# Function to execute the queries


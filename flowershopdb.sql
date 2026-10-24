-- running this script again deletes flowershopdb and rebuilds it with the demo data
DROP DATABASE IF EXISTS flowershopdb;

CREATE DATABASE flowershopdb;

USE flowershopdb;

CREATE TABLE customer (
    customer_id INT PRIMARY KEY,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    address VARCHAR(150),
    phone VARCHAR(20),
    email VARCHAR(100),
    delivery_address VARCHAR(150),
    customer_status VARCHAR(10)
);

CREATE TABLE staff (
    staff_id INT PRIMARY KEY,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    address VARCHAR(150),
    phone VARCHAR(20),
    email VARCHAR(100),
    position VARCHAR(50),
    username VARCHAR(30) NOT NULL UNIQUE,
    password_hash CHAR(64) NOT NULL,
    access_level VARCHAR(10)
);

CREATE TABLE supplier (
    supplier_id INT PRIMARY KEY,
    supplier_name VARCHAR(80) NOT NULL,
    contact_name VARCHAR(80),
    phone VARCHAR(20),
    email VARCHAR(100),
    address VARCHAR(150)
);

CREATE TABLE product (
    product_code CHAR(4) PRIMARY KEY,
    product_name VARCHAR(80) NOT NULL,
    category VARCHAR(30),
    unit_price DOUBLE,
    stock_qty INT,
    product_type VARCHAR(20),
    extra_info VARCHAR(20)
);

CREATE TABLE customer_order (
    order_id INT PRIMARY KEY,
    customer_id INT NULL,
    staff_id INT NOT NULL,
    order_date DATE,
    delivery_date DATE,
    order_type VARCHAR(10),
    delivery_address VARCHAR(150),
    order_status VARCHAR(10),
    payment_status VARCHAR(10),
    FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
    FOREIGN KEY (staff_id) REFERENCES staff (staff_id)
);

-- product_name and unit_price are copied when the order is taken, so an order line
-- keeps its history even after the item changes or leaves the catalog
CREATE TABLE order_item (
    order_id INT,
    product_code CHAR(4),
    product_name VARCHAR(80),
    quantity INT,
    unit_price DOUBLE,
    extra_charge DOUBLE,
    PRIMARY KEY (order_id, product_code),
    FOREIGN KEY (order_id) REFERENCES customer_order (order_id)
);

CREATE TABLE charge (
    charge_no INT PRIMARY KEY,
    charge_title VARCHAR(40) NOT NULL,
    charge_rate DOUBLE,
    charge_kind VARCHAR(10)
);

CREATE TABLE bill_detail (
    order_id INT,
    charge_no INT,
    base DOUBLE,
    rate DOUBLE,
    amount DOUBLE,
    bill_month INT,
    bill_year INT,
    PRIMARY KEY (order_id, charge_no),
    FOREIGN KEY (order_id) REFERENCES customer_order (order_id),
    FOREIGN KEY (charge_no) REFERENCES charge (charge_no)
);

CREATE TABLE restock (
    restock_id INT PRIMARY KEY,
    product_code CHAR(4) NOT NULL,
    supplier_id INT NOT NULL,
    restock_date DATE,
    quantity INT,
    unit_cost DOUBLE,
    FOREIGN KEY (product_code) REFERENCES product (product_code),
    FOREIGN KEY (supplier_id) REFERENCES supplier (supplier_id)
);

INSERT INTO customer (customer_id, last_name, first_name, address, phone, email, delivery_address, customer_status) VALUES
    (1001, 'Tremblay', 'Marie', '450 Rue Sherbrooke, Montreal, QC H2X 1Y4', '514-555-0142', 'marie.tremblay@gmail.com', '1200 Rue Saint-Denis, Montreal, QC H1M 2P8', 'Active'),
    (1002, 'Nguyen', 'Bao', '78 Avenue du Parc, Montreal, QC H2X 1V6', '514-555-0177', 'bao.nguyen@gmail.com', '78 Avenue du Parc, Montreal, QC H2X 1V6', 'Active'),
    (1003, 'Silva', 'Paulo', '300 Boulevard Saint-Laurent, Montreal, QC H3H 1A1', '438-555-0109', 'paulo.silva@gmail.com', '55 Rue Rachel, Montreal, QC H1E 7C8', 'Active'),
    (1004, 'Pires', 'Jennifer', '247 rue Michel Auger Montreal, QC H9L 7Y7', '514-693-6320', 'jpires@yahoo.com', '14 chemin Paul Lemonnier Montreal, QC H5Z 1E4', 'Active'),
    (1005, 'Smith', 'Clara', '455 rue Sherbroke, Montreal, QC H9L 3I4', '514-438-4580', 'csmith@outlook.com', '455 rue Sherbroke, Montreal, QC H9L 3I4', 'Active');

INSERT INTO staff (staff_id, last_name, first_name, address, phone, email, position, username, password_hash, access_level) VALUES
    (2001, 'Administrator', 'Shop', 'Flower Shop, Montreal, QC', '514-555-0100', 'admin@flowershop.com', 'Owner', 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Admin'),
    (2002, 'Piara', 'Lucie', '12 Rue Ontario, Montreal, QC H2L 1N8', '514-555-0188', 'lucie.piara@flowershop.com', 'Counter clerk', 'lucie', 'b90ea9b51b7c06a0b2e2d456acff3cab37cf96f71b18254042fefd8f9d991428', 'Clerk'),
    (2003, 'Nasser', 'Marc', '12 Rue Ontario, Montreal, QC H2L 1N8', '514-555-0155', 'marc.nasser@flowershop.com', 'Shop manager', 'marc', 'a5f89b14a8ffafcab104cde9b9e487e84ead7d0f8c8d7426e280187d6ae868c2', 'Manager');

INSERT INTO supplier (supplier_id, supplier_name, contact_name, phone, email, address) VALUES
    (3001, 'Laurentian Greenhouses', 'Sophie Lavoie', '450-555-0131', 'orders@laurentiangreenhouses.ca', '1400 Chemin du Lac, Saint-Sauveur, QC J0R 1R0'),
    (3002, 'Rive Sud Plant Wholesale', 'Martin Roy', '450-555-0174', 'sales@rivesudplants.ca', '85 Rue Industrielle, Longueuil, QC J4G 1A6'),
    (3003, 'Atwater Floral Supply', 'Amina Benali', '514-555-0196', 'contact@atwaterfloral.ca', '2300 Rue Notre-Dame Ouest, Montreal, QC H3J 1N4');

INSERT INTO product (product_code, product_name, category, unit_price, stock_qty, product_type, extra_info) VALUES
    ('B001', 'Red rose bouquet', 'Bouquets', 45.0, 11, 'Bouquet', '12'),
    ('B002', 'Spring mixed bouquet', 'Bouquets', 38.5, 5, 'Bouquet', '15'),
    ('P001', 'Orchid in ceramic pot', 'Potted plants', 52.0, 4, 'PottedPlant', '15 cm'),
    ('P002', 'Small succulent', 'Potted plants', 14.75, 0, 'PottedPlant', '8 cm'),
    ('O001', 'Sympathy arrangement', 'Occasions', 75.0, 2, 'Product', '0'),
    ('B003', 'Tulip bouquet', 'Bouquets', 31.0, 20, 'Bouquet', '10');

INSERT INTO customer_order (order_id, customer_id, staff_id, order_date, delivery_date, order_type, delivery_address, order_status, payment_status) VALUES
    (5002, 1001, 2002, '2026-10-11', '2026-10-17', 'Delivery', '1200 Rue Saint-Denis, Montreal, QC H1M 2P8', 'Completed', 'Paid'),
    (5003, NULL, 2002, '2026-10-11', '2026-10-17', 'Pickup', '', 'New', 'Unpaid');

INSERT INTO order_item (order_id, product_code, product_name, quantity, unit_price, extra_charge) VALUES
    (5002, 'O001', 'Sympathy arrangement', 1, 75.0, 0.0),
    (5002, 'B002', 'Spring mixed bouquet', 2, 38.5, 5.0),
    (5003, 'B001', 'Red rose bouquet', 1, 45.0, 5.0);

INSERT INTO charge (charge_no, charge_title, charge_rate, charge_kind) VALUES
    (100, 'Subtotal', 100.0, 'Percent'),
    (200, 'GST', 5.0, 'Percent'),
    (201, 'QST', 9.975, 'Percent'),
    (300, 'Delivery fee', 11.0, 'Fixed'),
    (101, 'Total', 100.0, 'Percent');

INSERT INTO bill_detail (order_id, charge_no, base, rate, amount, bill_month, bill_year) VALUES
    (5002, 100, 162.0, 100.0, 162.0, 10, 2026),
    (5002, 300, 162.0, 11.0, 11.0, 10, 2026),
    (5002, 200, 173.0, 5.0, 8.65, 10, 2026),
    (5002, 201, 173.0, 9.975, 17.26, 10, 2026),
    (5002, 101, 198.91, 100.0, 198.91, 10, 2026);

INSERT INTO restock (restock_id, product_code, supplier_id, restock_date, quantity, unit_cost) VALUES
    (7001, 'B001', 3001, '2026-10-05', 10, 22.50),
    (7002, 'P001', 3002, '2026-10-06', 6, 26.00),
    (7003, 'O001', 3003, '2026-10-08', 3, 40.00),
    (7004, 'B003', 3001, '2026-10-13', 20, 15.50);

SHOW TABLES;

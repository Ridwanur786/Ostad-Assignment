
--CREATE CUSTOMERS TABLE

CREATE TABLE customers(
		customers_id INT PRIMARY KEY,
		name VARCHAR(255) NOT NULL,
		email VARCHAR(100) UNIQUE,
		phone VARCHAR(20),
		city VARCHAR(50)		
);

--SHOW ALL CUSTOMERS

	SELECT * FROM customers;


	


--INSERT 5 DATA INTO CUSTOMERS TABLE

INSERT INTO customers(
		customers_id,
		name,
		email,
		phone,
		city
		) VALUES
		(1,  'Arif Chowdhury',	'arif@gmail.com',   '01877-180311', 	'Dhaka'),
		(2,  'Mitu Akter',      'mitu@yahoo.com',	'01877-180312', 	'Chittagong'),
		(3,  'Sujon Mia',       'sujon@gmail.com',	'01877-180313',  	'Sylhet'),
		(4,  'Puja Das',        'puja@hotmail.com', '01877-180314', 	'Dhaka'),
		(5,  'Rubel Khan',      'rubel@gmail.com',	'01877-180315', 	'Rajshahi');

-- CUSTOMERS TABLE CITY UPDATE

	UPDATE customers SET city='Dinajpur' WHERE city='Dhaka';

--DELETE 1 CUSTOMER

	 DELETE  FROM customers WHERE cutomer_id=1;

	--SHOW CUSTOMERS FROM DHAKA
	SELECT * FROM customers WHERE city IN('Dhaka');

	--SHOW CUSTOMERS ALPHABETICALLY

	SELECT * FROM customers ORDER BY name ASC;

	-- COUNT TOTAL CUSTOMERS

	SELECT COUNT(*) FROM customers;


	

--CREATE CATAGORIES TABLE

CREATE TABLE categories(
		category_id INT PRIMARY KEY,
		category_name VARCHAR(50)
);


--SHOW ALL CATEGORIES

	SELECT * FROM categories;
	

--INSERT 5 DATA INTO CATEGORIES TABLE

INSERT INTO categories(
		category_id,
		category_name
		) VALUES
		(1,  'Electronics'),
		(2,  'Fashion'),
		(3,  'Grocery'),
		(4,  'Mobile Accessories'),
		(5,  'IOT');



--CREATE PRODUCTS TABLE

CREATE TABLE products(
		product_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
		product_name VARCHAR(100),
		price DECIMAL(10,2),
		stock INT,
		category_id INT REFERENCES categories(category_id)		
);


--SHOW ALL PRODUCTS
	SELECT * FROM products;

	--SHOW PRODUCTS BY PRICE (HIGHEST TO LOWEST)

	SELECT * FROM products ORDER BY price DESC;


	--SHOW FIRST 5 PRODUCTS

	SELECT * FROM products ORDER BY product_id LIMIT 5;
	

--INSERT 5 DATA INTO PRODUCTS TABLE

INSERT INTO products(
		product_name,
		price,
		stock,
		category_id
		) VALUES
('Xiaomi Redmi 12 Phone',    18500.00,     50,     1),
('Samsung Phone A35',        32000.00,     30,     3),
('HP Laptop 15s',      65000.00,     15,     5),
('Dell Inspiron 15',   72000.00,     10,     2),
('Walton TV 43"',      42000.00,     20,     3),
('Sony Earbuds WF',    4500.00,     100,     1),
('Flour', 				950.00,     200,     2),
('Asus Router',        6800.00,      40,     4),
('iPad 10th Gen',      75000.00,      8,     5),
('Anker Power Bank',   2800.00,     150,     4);

DELETE FROM products;
--SHOW PRODUCTS PRICE > 1000

	SELECT * FROM products WHERE price > 1000;

	--SHOW AVERAGE PRICE OF ALL PRODUCT

	SELECT AVG(price) FROM products;

--SHOW PRODUCTS WHOSE STOCK IS < 10

	SELECT * FROM products WHERE stock < 10

	--CALCULATE MAXIMUM PRODUCT PRICE


	SELECT MAX(price) FROM products;


	--CALCULATE MINIMUM PRODUCT PRICE


	SELECT MIN(price) FROM products;

	--SHOW TOTAL STOCK

	SELECT COUNT(stock) FROM products;


	--SHOW AVERAGE STOCK

	SELECT AVG(stock) FROM products;


--UPDATE PRODUCTS PRICE

	UPDATE products set price='100000' WHERE price > 50000;
	
--UPDATE STOCK

	UPDATE products SET stock=stock-2 WHERE product_id=2 AND STOCK>= 30;


--DELETE 1 PRODUCT

	DELETE FROM products WHERE product_id=1;

--CREATE ORDERS TABLE

CREATE TABLE orders(
		order_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
		customers_id INT REFERENCES customers(customers_id),		
		order_date DATE
);

--INSERT DATA TO ORDER TABLE
INSERT INTO orders (customers_id, order_date) VALUES
(1, '2026-01-15'),
(2, '2026-02-01'),
(1, '2026-02-14'),
(3, '2026-03-10'),
(5, '2026-03-22');

--DELETE ORDER

	DELETE FROM orders WHERE customers_id=1;

	
--SHOW ALL ORDERS

	 SELECT * FROM orders;

	 DELETE FROM orders;

	--SHOW TOTAL NUMBER OF ORDERS

	SELECT COUNT(*) FROM orders GROUP BY order_date;

--show customer name with orders
	SELECT customers.name,
	orders.order_date FROM customers INNER JOIN
	orders ON customers.customers_id = orders.order_id;


	--SHOW PRODUCTS NAME WITH CATEGORY NAME


	SELECT products.product_name,
	categories.category_name FROM products INNER JOIN
	categories ON products.category_id = categories.category_id;


	--SHOW ORDER DETAILS WITH CUSTOMER NAME

	SELECT orders.order_id, 
	orders.customers_id,
	orders.order_date,
	customers.name FROM orders RIGHT JOIN
	customers ON orders.customers_id = customers.customers_id;


--PRODUCTS CONTAINING THE WORD PHONE

	SELECT * FROM products WHERE product_name 
	ILIKE '%Phone%' ORDER BY product_id DESC;

	--CUSTOMERS NAME STARTS WITH A

	 SELECT * FROM customers WHERE name ILIKE 'A%';

	 --PRODUCTS PRICE BETWEEN 500 AND 3000

	 SELECT * FROM products WHERE price BETWEEN 500 AND 3000;

	 --which product have the heightest price?

	 SELECT * FROM products WHERE price = (SELECT MAX(price) FROM products);

	 --which customer places the largest order?


	CREATE TABLE order_items (
    order_item_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INT REFERENCES products(product_id),
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL
);


-- Inserting sample order items?
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 2, 1200.00),   
(1, 3, 1, 850.50),    
(2, 2, 1, 2500.00),   
(3, 1, 1, 1200.00),   
(3, 4, 3, 1500.00),   
(3, 2, 1, 2500.00);  
	 
	
	
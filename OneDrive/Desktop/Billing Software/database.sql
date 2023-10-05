CREATE TABLE customers (
  customer_id INT PRIMARY KEY,
  customer_name VARCHAR(255),
  customer_address VARCHAR(255),
  -- Add other customer details as needed
);

CREATE TABLE bills (
  bill_id INT PRIMARY KEY,
  customer_id INT,
  bill_date DATE,
  total_amount DECIMAL(10, 2),
  FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

CREATE TABLE products (
  product_id INT PRIMARY KEY,
  product_name VARCHAR(255),
  price DECIMAL(10, 2),
  -- Add other product details as needed
);

CREATE TABLE bill_items (
  bill_item_id INT PRIMARY KEY,
  bill_id INT,
  product_id INT,
  quantity INT,
  FOREIGN KEY (bill_id) REFERENCES Bills(bill_id),
  FOREIGN KEY (product_id) REFERENCES Products(product_id)
);


SELECT c.customer_name, c.customer_email, c.customer_mobile, b.bill_no, p.product, b.quantity, p.price, b.total_bill
FROM customer AS c
JOIN billtable AS b ON c.customer_id = b.customer_id
JOIN products AS p ON p.p_id = b.p_id
WHERE b.bill_no = bill_no

/* 

self.db.customer_values(self.txtCusName.get() ,self.txtEmail.get(), self.entry_mob.get())
                  query = '''
                        SELECT c.customer_id , p.p_id 
                        FROM customer as c
                        JOIN products AS p ON p.product = ?
                        WHERE c.customer_mobile = ? '''
                  
                  self.crsr.execute(query , (product_name , customer_mobile))
                  
                  result = self.crsr.fetchone()
                  if result :
                        cus_id , p_id = result
                        #print(bill_no , total_bill , p_id , cus_id)
                        query = '''
                              INSERT INTO billtable(bill_no , total_bill , p_id , customer_id )
                              VALUES(?,?,?,?)'''
                        self.crsr.execute(query,(bill_no ,total_bill,p_id , cus_id))
                  else :
                        messagebox.showerror("INcorrect details" ,"Please provide the details")
*/

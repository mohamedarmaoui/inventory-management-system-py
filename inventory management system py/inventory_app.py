import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database setup
def create_table():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a product
def add_product():
    try:
        id_val = int(id_entry.get())
        name = name_entry.get()
        category = category_entry.get()
        quantity = int(quantity_entry.get())
        price = float(price_entry.get())
        
        if not name or not category:
            messagebox.showerror("Error", "Name and Category cannot be empty.")
            return
        
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (id, name, category, quantity, price) VALUES (?, ?, ?, ?, ?)",
                       (id_val, name, category, quantity, price))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Product added successfully!")
        clear_fields()
        view_products()
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Ensure ID, Quantity are integers and Price is a number.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Product ID already exists.")

# Function to update a product
def update_product():
    try:
        id_val = int(id_entry.get())
        name = name_entry.get()
        category = category_entry.get()
        quantity = int(quantity_entry.get())
        price = float(price_entry.get())
        
        if not name or not category:
            messagebox.showerror("Error", "Name and Category cannot be empty.")
            return
        
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET name=?, category=?, quantity=?, price=? WHERE id=?",
                       (name, category, quantity, price, id_val))
        if cursor.rowcount == 0:
            messagebox.showerror("Error", "Product ID not found.")
        else:
            messagebox.showinfo("Success", "Product updated successfully!")
        conn.commit()
        conn.close()
        clear_fields()
        view_products()
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Ensure ID, Quantity are integers and Price is a number.")

# Function to delete a product
def delete_product():
    try:
        id_val = int(id_entry.get())
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=?", (id_val,))
        if cursor.rowcount == 0:
            messagebox.showerror("Error", "Product ID not found.")
        else:
            messagebox.showinfo("Success", "Product deleted successfully!")
        conn.commit()
        conn.close()
        clear_fields()
        view_products()
    except ValueError:
        messagebox.showerror("Error", "Invalid ID. Must be an integer.")

# Function to search products
def search_product():
    search_term = search_entry.get()
    if not search_term:
        messagebox.showerror("Error", "Enter a search term.")
        return
    
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE name LIKE ? OR category LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
    rows = cursor.fetchall()
    conn.close()
    
    # Clear the treeview
    for item in tree.get_children():
        tree.delete(item)
    
    # Insert search results
    for row in rows:
        tree.insert('', 'end', values=row)

# Function to view all products
def view_products():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    
    # Clear the treeview
    for item in tree.get_children():
        tree.delete(item)
    
    # Insert all products
    for row in rows:
        tree.insert('', 'end', values=row)

# Function to clear input fields
def clear_fields():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    search_entry.delete(0, tk.END)

# GUI setup
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("800x600")

# Create database table on startup
create_table()

# Input fields
tk.Label(root, text="Product ID:").grid(row=0, column=0, padx=10, pady=5)
id_entry = tk.Entry(root)
id_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Name:").grid(row=1, column=0, padx=10, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Category:").grid(row=2, column=0, padx=10, pady=5)
category_entry = tk.Entry(root)
category_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Quantity:").grid(row=3, column=0, padx=10, pady=5)
quantity_entry = tk.Entry(root)
quantity_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Price:").grid(row=4, column=0, padx=10, pady=5)
price_entry = tk.Entry(root)
price_entry.grid(row=4, column=1, padx=10, pady=5)

# Buttons
tk.Button(root, text="Add Product", command=add_product).grid(row=5, column=0, padx=10, pady=10)
tk.Button(root, text="Update Product", command=update_product).grid(row=5, column=1, padx=10, pady=10)
tk.Button(root, text="Delete Product", command=delete_product).grid(row=6, column=0, padx=10, pady=10)
tk.Button(root, text="Clear Fields", command=clear_fields).grid(row=6, column=1, padx=10, pady=10)

# Search section
tk.Label(root, text="Search (Name/Category):").grid(row=7, column=0, padx=10, pady=5)
search_entry = tk.Entry(root)
search_entry.grid(row=7, column=1, padx=10, pady=5)
tk.Button(root, text="Search", command=search_product).grid(row=7, column=2, padx=10, pady=5)
tk.Button(root, text="View All", command=view_products).grid(row=8, column=1, padx=10, pady=5)

# Treeview for displaying products
columns = ('ID', 'Name', 'Category', 'Quantity', 'Price')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.grid(row=9, column=0, columnspan=3, padx=10, pady=10)

# Load all products on startup
view_products()

root.mainloop()

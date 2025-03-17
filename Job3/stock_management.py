import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import csv
import matplotlib.pyplot as plt
import os

# MySQL connection
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="######",  
        database="store"
    )
    cursor = conn.cursor()
    print("✅ MySQL connection successful!")
except mysql.connector.Error as err:
    messagebox.showerror("Connection Error", f"MySQL Error: {err}")
    exit()

# Function to load products
def load_products():
    cursor.execute("""
        SELECT product.id, product.name, product.description, product.price, 
               product.quantity, category.name 
        FROM product 
        JOIN category ON product.id_category = category.id
    """)
    rows = cursor.fetchall()
    product_tree.delete(*product_tree.get_children())  
    for row in rows:
        product_tree.insert("", tk.END, values=row)

# Function to open a new window for adding a product
def open_add_product_window():
    # New window for adding a product
    add_window = tk.Toplevel(root)
    add_window.title("Add Product")
    add_window.geometry("400x400")

    # Product Name
    tk.Label(add_window, text="Name:").pack(pady=5)
    name_entry = tk.Entry(add_window)
    name_entry.pack(pady=5)

    # Description
    tk.Label(add_window, text="Description:").pack(pady=5)
    desc_entry = tk.Entry(add_window)
    desc_entry.pack(pady=5)

    # Price
    tk.Label(add_window, text="Price:").pack(pady=5)
    price_entry = tk.Entry(add_window)
    price_entry.pack(pady=5)

    # Quantity
    tk.Label(add_window, text="Quantity:").pack(pady=5)
    quantity_entry = tk.Entry(add_window)
    quantity_entry.pack(pady=5)

    # Category
    tk.Label(add_window, text="Category:").pack(pady=5)
    cursor.execute("SELECT name FROM category")
    categories = [row[0] for row in cursor.fetchall()]
    category_combobox = ttk.Combobox(add_window, values=categories)
    category_combobox.pack(pady=5)

    # Function to add a product to the database from the add window
    def add_product():
        name = name_entry.get()
        description = desc_entry.get()
        price = price_entry.get()
        quantity = quantity_entry.get()
        category = category_combobox.get()

        if not name or not price or not quantity or not category:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        cursor.execute("SELECT id FROM category WHERE name = %s", (category,))
        category_id = cursor.fetchone()[0]

        cursor.execute("INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)", 
                       (name, description, price, quantity, category_id))
        conn.commit()
        load_products()  
        add_window.destroy()  
        messagebox.showinfo("Success", "Product added successfully.")

    # Button to add the product
    tk.Button(add_window, text="Add", command=add_product).pack(pady=10)
    tk.Button(add_window, text="Cancel", command=add_window.destroy).pack(pady=5)

# Function to delete a product
def delete_product():
    selected_item = product_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a product to delete.")
        return

    product_id = product_tree.item(selected_item, "values")[0]
    cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))
    conn.commit()
    load_products()
    messagebox.showinfo("Success", "Product deleted.")

# Function to update a product
def update_product():
    selected_item = product_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a product to update.")
        return

    # Retrieve the selected product details
    product_id = product_tree.item(selected_item, "values")[0]
    product_name = product_tree.item(selected_item, "values")[1]
    product_desc = product_tree.item(selected_item, "values")[2]
    product_price = product_tree.item(selected_item, "values")[3]
    product_quantity = product_tree.item(selected_item, "values")[4]
    product_category = product_tree.item(selected_item, "values")[5]

    # New window for editing
    update_window = tk.Toplevel(root)
    update_window.title("Edit Product")
    update_window.geometry("400x400")

    # Editing fields
    tk.Label(update_window, text="Name:").pack(pady=5)
    name_entry = tk.Entry(update_window)
    name_entry.insert(0, product_name)
    name_entry.pack(pady=5)

    tk.Label(update_window, text="Description:").pack(pady=5)
    desc_entry = tk.Entry(update_window)
    desc_entry.insert(0, product_desc)
    desc_entry.pack(pady=5)

    tk.Label(update_window, text="Price:").pack(pady=5)
    price_entry = tk.Entry(update_window)
    price_entry.insert(0, product_price)
    price_entry.pack(pady=5)

    tk.Label(update_window, text="Quantity:").pack(pady=5)
    quantity_entry = tk.Entry(update_window)
    quantity_entry.insert(0, product_quantity)
    quantity_entry.pack(pady=5)

    tk.Label(update_window, text="Category:").pack(pady=5)
    cursor.execute("SELECT name FROM category")
    categories = [row[0] for row in cursor.fetchall()]
    category_combobox = ttk.Combobox(update_window, values=categories)
    category_combobox.set(product_category)
    category_combobox.pack(pady=5)

    # Function to save the updated product
    def save_update():
        updated_name = name_entry.get()
        updated_desc = desc_entry.get()
        updated_price = price_entry.get()
        updated_quantity = quantity_entry.get()
        updated_category = category_combobox.get()

        if not updated_name or not updated_price or not updated_quantity or not updated_category:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        cursor.execute("SELECT id FROM category WHERE name = %s", (updated_category,))
        category_id = cursor.fetchone()[0]

        cursor.execute("""
            UPDATE product 
            SET name = %s, description = %s, price = %s, quantity = %s, id_category = %s 
            WHERE id = %s
        """, (updated_name, updated_desc, updated_price, updated_quantity, category_id, product_id))
        conn.commit()
        load_products()  
        update_window.destroy()  
        messagebox.showinfo("Success", "Product updated.")

    # Button to save the changes
    tk.Button(update_window, text="Save", command=save_update).pack(pady=10)
    tk.Button(update_window, text="Cancel", command=update_window.destroy).pack(pady=5)

# Function to export to CSV
def export_csv():
    cursor.execute("SELECT * FROM product")
    rows = cursor.fetchall()

    # Get the current directory path
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, "stock.csv")

    # Save the CSV in the current directory
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Description", "Price", "Quantity", "Category ID"])
        writer.writerows(rows)
    
    messagebox.showinfo("Export", f"Products have been successfully exported to CSV. The file is saved at {file_path}.")

# Function to search for a product
def search_product():
    search_text = search_entry.get()
    cursor.execute("""
        SELECT product.id, product.name, product.description, product.price, 
               product.quantity, category.name 
        FROM product 
        JOIN category ON product.id_category = category.id 
        WHERE product.name LIKE %s
    """, ("%"+search_text+"%",))
    rows = cursor.fetchall()
    product_tree.delete(*product_tree.get_children())  
    for row in rows:
        product_tree.insert("", tk.END, values=row)

# Function to display a stock chart
def show_stock_chart():
    cursor.execute("SELECT name, quantity FROM product")
    data = cursor.fetchall()
    
    if not data:
        messagebox.showwarning("Data", "No products to display.")
        return

    names = [row[0] for row in data]
    quantities = [row[1] for row in data]

    plt.figure(figsize=(8, 5))
    plt.bar(names, quantities, color="skyblue")
    plt.xlabel("Products")
    plt.ylabel("Stock Quantity")
    plt.title("Product Stock")
    plt.xticks(rotation=45)
    plt.show()

# Tkinter interface with ttk.Style()
root = tk.Tk()
root.title("Stock Management")
root.geometry("900x600")

style = ttk.Style()
style.configure("Treeview", font=("Arial", 12), rowheight=25)
style.configure("Treeview.Heading", font=("Arial", 13, "bold"))

# Search bar
search_frame = tk.Frame(root)
search_frame.pack(pady=10)
tk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="Search", command=search_product).pack(side=tk.LEFT, padx=5)

# Product table
columns = ("ID", "Name", "Description", "Price", "Quantity", "Category")
product_tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    product_tree.heading(col, text=col)
    product_tree.column(col, anchor="center")
product_tree.pack(expand=True, fill="both", padx=10, pady=10)

# Action buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
tk.Button(button_frame, text="Add", command=open_add_product_window).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Edit", command=update_product).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Delete", command=delete_product).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Export CSV", command=export_csv).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Show Stock", command=show_stock_chart).pack(side=tk.LEFT, padx=10)

# Load products on startup
load_products()

root.mainloop()

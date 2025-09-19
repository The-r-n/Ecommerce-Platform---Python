# File: order_operation.py
# Creation Date: 23/04/2025
# Last Modified Date: 23/04/2025
# Description: This file contains the OrderOperation class.

import os
import random
import time
import math
import pandas as pd
import matplotlib.pyplot as plt
from order import Order
from customer_operation import CustomerOperation
from product_operation import ProductOperation
from user_operation import UserOperation

class OrderOperation:
    """
    Contains all the operations related to the order.
    """
    orders_file_path = 'data/orders.txt'
    figure_path = 'data/figure'

    def _read_orders(self):
        """Helper method to read all orders from the orders.txt file."""
        if not os.path.exists(self.orders_file_path):
            os.makedirs(os.path.dirname(self.orders_file_path), exist_ok=True)
            return []
        
        with open(self.orders_file_path, 'r', encoding='utf-8') as f:
            orders = []
            for line in f:
                try:
                    orders.append(eval(line.strip()))
                except:
                    continue
            return orders

    def _write_orders(self, orders_list):
        """Helper method to write a list of orders back to the file."""
        os.makedirs(os.path.dirname(self.orders_file_path), exist_ok=True)
        with open(self.orders_file_path, 'w', encoding='utf-8') as f:
            for order in orders_list:
                f.write(str(order) + '\n')
    
    def generate_unique_order_id(self):
        """
        Generates a unique 5-digit order id starting with 'o_'.
        """
        orders = self._read_orders()
        existing_ids = {order.get('order_id') for order in orders}
        
        while True:
            new_id = f"o_{random.randint(0, 99999):05d}"
            if new_id not in existing_ids:
                return new_id

    def create_an_order(self, customer_id, product_id, create_time=None):
        """
        Creates a new order and saves it to the database.
        """
        if create_time is None:
            create_time = time.strftime("%d-%m-%Y_%H:%M:%S")
            
        new_order = Order(
            order_id=self.generate_unique_order_id(),
            user_id=customer_id,
            pro_id=product_id,
            order_time=create_time
        )
        
        with open(self.orders_file_path, 'a', encoding='utf-8') as f:
            f.write(str(new_order) + '\n')
        return True

    def delete_order(self, order_id):
        """
        Deletes an order from data/orders.txt based on the order_id.
        """
        all_orders = self._read_orders()
        original_count = len(all_orders)
        
        orders_after_deletion = [o for o in all_orders if o.get('order_id') != order_id]
        
        if len(orders_after_deletion) < original_count:
            self._write_orders([Order(**o) for o in orders_after_deletion])
            return True
        return False

    def get_order_list(self, customer_id, page_number):
        """
        Retrieves one page of orders for a given customer.
        """
        all_orders = self._read_orders()
        customer_orders_data = [o for o in all_orders if o.get('user_id') == customer_id]
        
        items_per_page = 10
        total_pages = math.ceil(len(customer_orders_data) / items_per_page)
        
        if page_number < 1 or (page_number > total_pages and total_pages > 0):
            return ([], page_number, total_pages)

        start_index = (page_number - 1) * items_per_page
        end_index = start_index + items_per_page
        
        page_orders_data = customer_orders_data[start_index:end_index]
        order_objects = [Order(**data) for data in page_orders_data]

        return (order_objects, page_number, total_pages)
        
    def generate_test_order_data(self):
        """
        Generates test data: 10 customers and 50-200 orders for each.
        """
        cust_op = CustomerOperation()
        prod_op = ProductOperation()
        
        all_products_data = prod_op._read_products()
        if not all_products_data:
            print("Cannot generate test orders: No products found in data/products.txt.")
            return

        product_ids = [p['pro_id'] for p in all_products_data]

        new_customer_ids = []
        for i in range(10):
            # Ensure unique username for test users
            username = f'testuser_{int(time.time())}_{i}'
            if not UserOperation().check_username_exist(username):
                cust_op.register_customer(
                    username,
                    'Password123',
                    f'{username}@test.com',
                    f'04{random.randint(10000000, 99999999)}'
                )
                user_obj = UserOperation().login(username, 'Password123')
                if user_obj:
                    new_customer_ids.append(user_obj.user_id)

        for user_id in new_customer_ids:
            num_orders = random.randint(50, 200)
            for _ in range(num_orders):
                random_product_id = random.choice(product_ids)
                now = time.time()
                random_past_time = now - random.uniform(0, 365 * 24 * 60 * 60)
                random_time_str = time.strftime("%d-%m-%Y_%H:%M:%S", time.localtime(random_past_time))
                self.create_an_order(user_id, random_product_id, random_time_str)

    def _get_orders_with_product_details(self):
        """Helper to create a merged DataFrame of orders and product prices."""
        orders_df = pd.DataFrame(self._read_orders())
        products_df = pd.DataFrame(ProductOperation()._read_products())

        if orders_df.empty or products_df.empty:
            return pd.DataFrame()
        
        products_df['pro_current_price'] = pd.to_numeric(products_df['pro_current_price'], errors='coerce')
        merged_df = pd.merge(orders_df, products_df[['pro_id', 'pro_current_price', 'pro_name']], on='pro_id', how='left')
        merged_df['order_time'] = pd.to_datetime(merged_df['order_time'], format='%d-%m-%Y_%H:%M:%S', errors='coerce')
        merged_df.dropna(subset=['order_time', 'pro_current_price'], inplace=True)
        
        return merged_df

    def generate_single_customer_consumption_figure(self, customer_id):
        """
        Generates a bar chart of a single customer's monthly consumption.
        """
        df = self._get_orders_with_product_details()
        if df.empty: return
        
        customer_df = df[df['user_id'] == customer_id]
        if customer_df.empty: return

        customer_df['month'] = customer_df['order_time'].dt.month
        monthly_consumption = customer_df.groupby('month')['pro_current_price'].sum().reindex(range(1, 13), fill_value=0)
        
        plt.figure(figsize=(10, 6))
        monthly_consumption.plot(kind='bar')
        plt.title(f'Monthly Consumption for Customer: {customer_id}')
        plt.xlabel('Month')
        plt.ylabel('Total Consumption ($)')
        plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
        plt.tight_layout()
        
        os.makedirs(self.figure_path, exist_ok=True)
        plt.savefig(os.path.join(self.figure_path, f'single_customer_consumption_{customer_id}.png'))
        plt.close()

    def generate_all_customers_consumption_figure(self):
        """
        Generates a line chart of all customers' combined monthly consumption.
        """
        df = self._get_orders_with_product_details()
        if df.empty: return

        df['month'] = df['order_time'].dt.month
        monthly_consumption = df.groupby('month')['pro_current_price'].sum().reindex(range(1, 13), fill_value=0)
        
        plt.figure(figsize=(10, 6))
        monthly_consumption.plot(kind='line', marker='o')
        plt.title('Total Monthly Consumption (All Customers)')
        plt.xlabel('Month')
        plt.ylabel('Total Consumption ($)')
        plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        plt.grid(True)
        plt.tight_layout()
        
        os.makedirs(self.figure_path, exist_ok=True)
        plt.savefig(os.path.join(self.figure_path, 'all_customers_consumption.png'))
        plt.close()

    def generate_all_top_10_best_sellers_figure(self):
        """
        Generates a bar chart of the top 10 best-selling products.
        """
        df = self._get_orders_with_product_details()
        if df.empty: return
        
        top_10 = df['pro_name'].value_counts().nlargest(10)
        
        plt.figure(figsize=(12, 8))
        top_10.sort_values(ascending=True).plot(kind='barh')
        plt.title('Top 10 Best-Selling Products')
        plt.xlabel('Number of Orders')
        plt.ylabel('Product Name')
        plt.tight_layout()
        
        os.makedirs(self.figure_path, exist_ok=True)
        plt.savefig(os.path.join(self.figure_path, 'all_top_10_best_sellers.png'))
        plt.close()

    def delete_all_orders(self):
        """
        Removes all order data from data/orders.txt.
        """
        if os.path.exists(self.orders_file_path):
            os.remove(self.orders_file_path)


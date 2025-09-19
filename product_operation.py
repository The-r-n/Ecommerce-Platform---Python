# File: product_operation.py
# Creation Date: 22/04/2025
# Last Modified Date: 22/04/2025
# Description: This file contains the ProductOperation class.

import os
import glob
import pandas as pd
import math
import matplotlib.pyplot as plt
from product import Product

class ProductOperation:
    """
    Contains all the operations related to the product.
    """
    products_file_path = 'data/products.txt'
    products_source_path = 'data/product/*.csv'
    figure_path = 'data/figure'

    def _read_products(self):
        """Helper method to read all products from the products.txt file."""
        if not os.path.exists(self.products_file_path):
            return []
        
        with open(self.products_file_path, 'r', encoding='utf-8') as f:
            products = []
            for line in f:
                try:
                    products.append(eval(line.strip()))
                except:
                    continue
            return products

    def _write_products(self, products_list):
        """Helper method to write a list of products back to the file."""
        os.makedirs(os.path.dirname(self.products_file_path), exist_ok=True)
        with open(self.products_file_path, 'w', encoding='utf-8') as f:
            for product in products_list:
                f.write(str(product) + '\n')

    def extract_products_from_files(self):
        """
        Extracts product information from source CSV files into data/products.txt.
        """
        csv_files = glob.glob(self.products_source_path)
        if not csv_files:
            return # No source files found

        all_products = []
        for file in csv_files:
            df = pd.read_csv(file)
            # Rename columns to match our Product class attributes
            # This requires knowing the structure of the source CSVs. We'll assume a mapping.
            # Example mapping: 'id'->'pro_id', 'name'->'pro_name', etc.
            # For this assignment, we will assume the columns are consistently named across files.
            df = df.rename(columns={
                'id': 'pro_id', 'model': 'pro_model', 'category': 'pro_category',
                'name': 'pro_name', 'current_price': 'pro_current_price',
                'raw_price': 'pro_raw_price', 'discount': 'pro_discount',
                'likes_count': 'pro_likes_count'
            })
            
            # Ensure all required columns exist, fill missing with defaults if necessary
            required_cols = ['pro_id', 'pro_model', 'pro_category', 'pro_name', 
                             'pro_current_price', 'pro_raw_price', 'pro_discount', 'pro_likes_count']
            for col in required_cols:
                if col not in df.columns:
                    df[col] = "" # or appropriate default like 0 for numbers

            all_products.append(df[required_cols])

        if not all_products:
            return

        combined_df = pd.concat(all_products, ignore_index=True)
        combined_df.drop_duplicates(subset=['pro_id'], inplace=True)
        
        product_objects = [Product(**row) for index, row in combined_df.iterrows()]
        self._write_products(product_objects)


    def get_product_list(self, page_number):
        """
        Retrieves one page of products from the database.
        """
        products_data = self._read_products()
        
        items_per_page = 10
        total_pages = math.ceil(len(products_data) / items_per_page)
        
        if page_number < 1 or page_number > total_pages:
            return ([], page_number, total_pages)

        start_index = (page_number - 1) * items_per_page
        end_index = start_index + items_per_page
        
        page_products_data = products_data[start_index:end_index]
        product_objects = [Product(**data) for data in page_products_data]

        return (product_objects, page_number, total_pages)

    def delete_product(self, product_id):
        """
        Deletes a product from data/products.txt based on product_id.
        """
        all_products = self._read_products()
        original_count = len(all_products)
        
        products_after_deletion = [p for p in all_products if p.get('pro_id') != product_id]
        
        if len(products_after_deletion) < original_count:
            self._write_products(products_after_deletion)
            return True
        return False

    def get_product_list_by_keyword(self, keyword):
        """
        Retrieves all products whose name contains the keyword (case insensitive).
        """
        all_products = self._read_products()
        
        matching_products_data = [
            p for p in all_products if keyword.lower() in p.get('pro_name', '').lower()
        ]
        
        product_objects = [Product(**data) for data in matching_products_data]
        return product_objects

    def get_product_by_id(self, product_id):
        """
        Returns one product object based on the given product_id.
        """
        all_products = self._read_products()
        for p_data in all_products:
            if p_data.get('pro_id') == product_id:
                return Product(**p_data)
        return None

    def _get_products_as_dataframe(self):
        """Helper to load products into a pandas DataFrame for analysis."""
        products_data = self._read_products()
        if not products_data:
            return pd.DataFrame()
        return pd.DataFrame(products_data)

    def generate_category_figure(self):
        """
        Generates a bar chart of product counts per category.
        """
        df = self._get_products_as_dataframe()
        if df.empty: return
        
        category_counts = df['pro_category'].value_counts().sort_values(ascending=False)
        
        plt.figure(figsize=(12, 8))
        category_counts.plot(kind='bar')
        plt.title('Total Number of Products per Category')
        plt.xlabel('Category')
        plt.ylabel('Number of Products')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        os.makedirs(self.figure_path, exist_ok=True)
        plt.savefig(os.path.join(self.figure_path, 'generate_category_figure.png'))
        plt.close()

    def generate_discount_figure(self):
        """
        Generates a pie chart of product discount proportions.
        """
        df = self._get_products_as_dataframe()
        if df.empty: return
        
        df['pro_discount'] = pd.to_numeric(df['pro_discount'], errors='coerce')
        
        bins = [-1, 29, 60, float('inf')]
        labels = ['< 30%', '30% - 60%', '> 60%']
        df['discount_group'] = pd.cut(df['pro_discount'], bins=bins, labels=labels, right=True)
        
        discount_counts = df['discount_group'].value_counts()
        
        plt.figure(figsize=(8, 8))
        plt.pie(discount_counts, labels=discount_counts.index, autopct='%1.1f%%', startangle=140)
        plt.title('Proportion of Products by Discount Range')
        plt.ylabel('') # Hide the y-label
        
        os.makedirs(self.figure_path, exist_ok=True)
        plt.savefig(os.path.join(self.figure_path, 'generate_discount_figure.png'))
        plt.close()


    def generate_likes_count_figure(self):
        """
        Generates a bar chart of total likes per category.
        """
        df = self._get_products_as_dataframe()
        if df.empty: return
        
        df['pro_likes_count'] = pd.to_numeric(df['pro_likes_count'], errors='coerce')
        likes_by_category = df.groupby('pro_category')['pro_likes_count'].sum().sort_values(ascending=True)
        
        plt.figure(figsize=(12, 8))
        likes_by_category.plot(kind='barh') # Horizontal bar chart is good for long labels
        plt.title("Sum of Product Likes per Category")
        plt.xlabel("Total Likes Count")
        plt.ylabel("Category")
        plt.tight_layout()

        os.makedirs(self.figure_path, exist_ok=True)
        plt.savefig(os.path.join(self.figure_path, 'generate_likes_count_figure.png'))
        plt.close()

    def generate_discount_likes_count_figure(self):
        """
        Generates a scatter chart showing relationship between likes and discount.
        """
        df = self._get_products_as_dataframe()
        if df.empty: return
        
        df['pro_likes_count'] = pd.to_numeric(df['pro_likes_count'], errors='coerce')
        df['pro_discount'] = pd.to_numeric(df['pro_discount'], errors='coerce')
        df.dropna(subset=['pro_likes_count', 'pro_discount'], inplace=True)

        plt.figure(figsize=(10, 6))
        plt.scatter(df['pro_discount'], df['pro_likes_count'], alpha=0.5)
        plt.title('Relationship between Discount and Likes Count')
        plt.xlabel('Discount (%)')
        plt.ylabel('Likes Count')
        plt.grid(True)
        
        os.makedirs(self.figure_path, exist_ok=True)
        plt.savefig(os.path.join(self.figure_path, 'generate_discount_likes_count_figure.png'))
        plt.close()

    def delete_all_products(self):
        """
        Removes all product data from data/products.txt.
        """
        if os.path.exists(self.products_file_path):
            os.remove(self.products_file_path)


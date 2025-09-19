# File: product.py
# Creation Date: 19/04/2025
# Last Modified Date: 19/04/2025
# Description: This file contains the Product class.

class Product:
    """
    Represents a product in the e-commerce system.
    """
    def __init__(self, pro_id="", pro_model="", pro_category="", pro_name="",
                 pro_current_price=0.0, pro_raw_price=0.0, pro_discount=0.0, pro_likes_count=0):
        """
        Constructs a Product object.

        Args:
            pro_id (str): The unique ID of the product.
            pro_model (str): The model of the product.
            pro_category (str): The category of the product.
            pro_name (str): The name of the product.
            pro_current_price (float): The current selling price.
            pro_raw_price (float): The original price.
            pro_discount (float): The discount percentage.
            pro_likes_count (int): The number of likes the product has.
        """
        self.pro_id = pro_id
        self.pro_model = pro_model
        self.pro_category = pro_category
        self.pro_name = pro_name
        self.pro_current_price = pro_current_price
        self.pro_raw_price = pro_raw_price
        self.pro_discount = pro_discount
        self.pro_likes_count = pro_likes_count

    def __str__(self):
        """
        Returns the product information as a formatted string dictionary.

        Returns:
            str: A string representation of the Product object.
        """
        return str({
            'pro_id': self.pro_id,
            'pro_model': self.pro_model,
            'pro_category': self.pro_category,
            'pro_name': self.pro_name,
            'pro_current_price': self.pro_current_price,
            'pro_raw_price': self.pro_raw_price,
            'pro_discount': self.pro_discount,
            'pro_likes_count': self.pro_likes_count
        })

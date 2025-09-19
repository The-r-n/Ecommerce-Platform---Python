# File: order.py
# Creation Date: 19/04/2025
# Last Modified Date: 19/04/2025
# Description: This file contains the Order class.

class Order:
    """
    Represents an order in the e-commerce system.
    """
    def __init__(self, order_id="", user_id="", pro_id="", order_time="00-00-0000_00:00:00"):
        """
        Constructs an Order object.

        Args:
            order_id (str): The unique ID of the order.
            user_id (str): The ID of the user who placed the order.
            pro_id (str): The ID of the product in the order.
            order_time (str): The time the order was placed.
        """
        self.order_id = order_id
        self.user_id = user_id
        self.pro_id = pro_id
        self.order_time = order_time

    def __str__(self):
        """
        Returns the order information as a formatted string dictionary.

        Returns:
            str: A string representation of the Order object.
        """
        return str({
            'order_id': self.order_id,
            'user_id': self.user_id,
            'pro_id': self.pro_id,
            'order_time': self.order_time
        })
